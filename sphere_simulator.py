import glfw
import moderngl
import numpy as np
import time
from pyrr import Matrix44
import cv2
import sys
import threading
import random  

class SphereSimulator:
    """
    Clase simulación de una esfera con deformaciones
    y postproceso usando ModernGL y GLFW.
    """
    
    def __init__(self, window, width: int = 800, height: int = 600, 
                 emotions_list: list = None):
        # ... (inicialización sin cambios)
        self.window = window
        self.width = width
        self.height = height
        self.ctx = None
        self.prog_sphere = None
        self.prog_post = None
        self.vao_sphere = None
        self.vao_post = None
        self.fbo = None
        self.projection = None
        self.view = None
        self.start_time = time.time()

        # Parámetros de la simulación
        self.blur_strength = 5.0

        # State for emotions transition
        self.emotions_list = emotions_list if emotions_list else []
        self.current_index = 0
        self.is_transitioning = False
        self.transition_start_time = 0.0
        self.transition_duration = 2.0
        
        # Current parameters (A) and next parameters (B) for transition
        self.params_A = {}
        self.params_B = {}
        
        if self.emotions_list:
            self.params_A = self.emotions_list[0].copy()
            self.params_B = self.emotions_list[0].copy()

        # parámetros de color para los shaders
        self.light_color1 = (1.0, 1.0, 1.0)
        self.light_color2 = (0.5, 0.5, 0.5)

        self._init_moderngl()
        self._load_shaders()
        self._load_mesh()
        self._setup_framebuffer()
        self._setup_matrices()

    def _init_moderngl(self):
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

    def _load_shaders(self):
        try:
            with open("shaders/sphere_vert.glsl", 'r') as f:
                vert_shader = f.read()
            with open("shaders/sphere_frag.glsl", 'r') as f:
                frag_shader = f.read()
            self.prog_sphere = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
            with open("shaders/post_vert.glsl", 'r') as f:
                post_vert_shader = f.read()
            with open("shaders/post_frag.glsl", 'r') as f:
                post_frag_shader = f.read()
            self.prog_post = self.ctx.program(vertex_shader=post_vert_shader, fragment_shader=post_frag_shader)
        except FileNotFoundError as e:
            print(f"Error: No se encontró el archivo de shader. Detalles: {e}")
            raise

    def _load_mesh(self):
        try:
            vertices = np.load("vertices_high_res.npy")
            indices = np.load("indices_high_res.npy")
            vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
            ibo = self.ctx.buffer(indices.astype('i4').tobytes())
            self.vao_sphere = self.ctx.simple_vertex_array(self.prog_sphere, vbo, 'in_position', index_buffer=ibo)
        except FileNotFoundError as e:
            print(f"Error: No se encontró el archivo de malla. Detalles: {e}")
            raise
        
        quad_vertices = np.array([-1, -1, 0, 0, 1, -1, 1, 0, -1, 1, 0, 1, 1, 1, 1, 1,], dtype='f4')
        quad_vbo = self.ctx.buffer(quad_vertices.tobytes())
        self.vao_post = self.ctx.simple_vertex_array(self.prog_post, quad_vbo, 'in_pos', 'in_uv')

    def _setup_framebuffer(self):
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.width, self.height), 4)],
            depth_attachment=self.ctx.depth_renderbuffer((self.width, self.height))
        )

    def _setup_matrices(self):
        self.projection = Matrix44.perspective_projection(45.0, self.width / self.height, 0.1, 100.0)
        self.view = Matrix44.look_at((0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))

    def start_next_transition(self):
        if self.current_index < len(self.emotions_list):
            self.params_A = self.params_B.copy()
            self.params_B = self.emotions_list[self.current_index].copy()
            
            # Obtenemos los parámetros de la emoción
            fragmento = self.params_B.get('fragment', 'N/A')
            emocion1 = self.params_B.get('emocion1', 'N/A')
            emocion2 = self.params_B.get('emocion2', 'N/A')
            matiz = self.params_B.get('matiz', 'N/A')
            
            # Iniciamos un nuevo hilo para la impresión animada
            # Pasamos los parámetros de la emoción a la función como argumentos
            print_thread = threading.Thread(
                target=animated_print, 
                args=(fragmento, emocion1, emocion2, matiz)
            )
            print_thread.start() # ¡Esto inicia el hilo de forma no bloqueante!
            
            # El resto del código de transición continúa inmediatamente
            self.is_transitioning = True
            self.transition_start_time = time.time()
            self.current_index += 1
            
            return False
        else:
            print("\n\n" + "🎉" * 10 + " ¡Fin de la simulación! " + "🎉" * 10)
            print("No dudes en seguir escribiendo y explorando tus emociones. 😊")
            return True

    def _update_transition(self, now):
        """Calcula el factor de mezcla para una transición suave."""
        if self.is_transitioning:
            elapsed_time = now - self.transition_start_time
            blend_factor = min(elapsed_time / self.transition_duration, 1.0)
            if blend_factor >= 1.0:
                self.is_transitioning = False
                self.params_A = self.params_B.copy()
            return blend_factor
        return 0.0

    def render(self, now):
        """Dibuja un solo fotograma de la simulación."""
        #Se va llamando en cada frame para animar la esfera
        simulation_time = now - self.start_time

        blend_factor = self._update_transition(now)
        self.fbo.use()
        self.ctx.clear(0.05, 0.05, 0.05)
        model = Matrix44.identity()

        def lerp(a, b, t):
            return a + (b - a) * t
        
        def lerp_vec3(a, b, t):
            if not isinstance(a, (tuple, list)) or not isinstance(b, (tuple, list)) or len(a) != len(b):
                return b
            return tuple(lerp(a[i], b[i], t) for i in range(len(a)))
        
        def get_param(param_name, default, is_vector=False):
            val_A = self.params_A.get(param_name, default)
            val_B = self.params_B.get(param_name, default)
            if is_vector:
                return lerp_vec3(val_A, val_B, blend_factor)
            if isinstance(val_A, (int, float)) and isinstance(val_B, (int, float)):
                return lerp(val_A, val_B, blend_factor)
            return val_B

        # Obtener los parámetros interpolados
        velocidad_current = get_param('velocidad', 5.0)
        rugosidad_current = get_param('rugosidad', 10.0)
        distorsion_current = get_param('distorsion', 0.1)
        wave_direction_current = get_param('wave_direction', 0)
        base_color_current = (0.5, 0.5, 0.5)#get_param('color1', (1.0, 1.0, 1.0), is_vector=True)
        contrast_color_current = get_param('color2', None, is_vector=True)
        hybrid_amnts_A = self.params_A.get('hybrid_amnts', [0.0, 0.0, 0.0])
        hybrid_amnts_B = self.params_B.get('hybrid_amnts', [0.0, 0.0, 0.0])
        
        # Enviar uniformes al shader de la esfera
        self.prog_sphere['time'].value = simulation_time  # ¡CAMBIO CLAVE AQUÍ!
        self.prog_sphere['velocidad'].value = velocidad_current
        self.prog_sphere['rugosidad'].value = rugosidad_current
        self.prog_sphere['distorsion'].value = distorsion_current
        self.prog_sphere['wave_direction'].value = int(round(wave_direction_current))
        self.prog_sphere['model'].write(model.astype('f4').tobytes())
        self.prog_sphere['view'].write(self.view.astype('f4').tobytes())
        self.prog_sphere['projection'].write(self.projection.astype('f4').tobytes())
        self.prog_sphere['base_color'].value = base_color_current
        self.prog_sphere['light_color1'].value = get_param('color1', self.light_color1, is_vector=True)
        self.prog_sphere['light_color2'].value = contrast_color_current if contrast_color_current else get_param('color1', self.light_color1, is_vector=True)
        self.prog_sphere['deform_mode_A'].value = int(self.params_A.get('deform_mode', 0))
        self.prog_sphere['deform_mode_B'].value = int(self.params_B.get('deform_mode', 0))
        self.prog_sphere['blend_factor'].value = blend_factor
        self.prog_sphere['effect1_amnt_A'].value = hybrid_amnts_A[0]
        self.prog_sphere['effect2_amnt_A'].value = hybrid_amnts_A[1]
        self.prog_sphere['effect3_amnt_A'].value = hybrid_amnts_A[2]
        self.prog_sphere['effect1_amnt_B'].value = hybrid_amnts_B[0]
        self.prog_sphere['effect2_amnt_B'].value = hybrid_amnts_B[1]
        self.prog_sphere['effect3_amnt_B'].value = hybrid_amnts_B[2]
        self.vao_sphere.render()

        # Postproceso
        self.ctx.screen.use()
        self.ctx.clear()
        self.fbo.color_attachments[0].use(location=0)
        self.prog_post['texture0'].value = 0
        self.prog_post['resolution'].value = (float(self.width), float(self.height))
        self.prog_post['blur_strength'].value = self.blur_strength
        self.vao_post.render(moderngl.TRIANGLE_STRIP)

    def terminate(self):
        """Limpia los recursos de GLFW."""
        self.ctx.release()
        self.fbo.release()
        self.prog_sphere.release()
        self.prog_post.release()
        self.vao_sphere.release()
        self.vao_post.release()


def start_glfw_simulation(emotions_list, record_simulation: bool = False):
    """
    inicializa y ejecuta el bucle de simulación de la esfera.
    """
    if not glfw.init():
        return
    
    
    # Configurar las sugerencias de la ventana
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

    # Obtener el monitor principal y su modo de video
    monitor = glfw.get_primary_monitor()
    monitor_mode = glfw.get_video_mode(monitor)

    width, height = monitor_mode.size.width, monitor_mode.size.height//2

    # Crear la ventana
    window = glfw.create_window(width, height, "Emotions Visualization", None, None)
    if not window:
        glfw.terminate()
        exit()

    # Calcular las coordenadas para centrar la ventana en X y colocarla en la mitad superior en Y
    window_x = (monitor_mode.size.width - width) // 2
    window_y = 0

    # Establecer la posición de la ventana
    glfw.set_window_pos(window, window_x, window_y)

    glfw.make_context_current(window)

    simulator = SphereSimulator(window, width, height, emotions_list=emotions_list)

    # GRABACIÓN:
    video_writer = None
    if record_simulation:
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        output_filename = f"simulacion_emociones_{int(time.time())}.mp4"
        fps = 60 
        video_writer = cv2.VideoWriter(output_filename, fourcc, fps, (width, height))
        print(f"Iniciando grabación... guardando en '{output_filename}'")
    #
    
    #primera transición si hay emociones en la lista
    if emotions_list:
        simulator.start_next_transition()

    stop = False
    while not glfw.window_should_close(window):
        now = time.time()
        
        #input
        if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS and not simulator.is_transitioning:
            stop = simulator.start_next_transition()

        if stop:
            break

        simulator.render(now)

        #CAPTURA Y ESCRITURA DE CADA FOTOGRAMA:
        if video_writer:
            #píxeles del framebuffer
            #`self.ctx.screen` es el framebuffer principal
            frame_bytes = simulator.ctx.screen.read(components=3, dtype='f1')
            
            #array de NumPy
            frame_np = np.frombuffer(frame_bytes, dtype=np.uint8).reshape((height, width, 3))
            
            #píxeles se leen al revés (de abajo a arriba) y en RGB
            #OpenCV espera BGR y el orden normal
            frame_np = np.flip(frame_np, 0)
            frame_np = cv2.cvtColor(frame_np, cv2.COLOR_RGB2BGR)

            video_writer.write(frame_np)


        glfw.swap_buffers(window)
        glfw.poll_events()

    if video_writer:
        video_writer.release()
        print("Grabación finalizada. Archivo guardado.")

    simulator.terminate()
    glfw.terminate()


def animated_print(fragmento, emocion1, emocion2, matiz):
    """
    Función que maneja la impresión animada en la terminal.
    Se ejecuta en un hilo separado para no bloquear la simulación.
    """
    # Puntos suspensivos animados para el "pensando..."
    sys.stdout.write("\nAnalizando el fragmento de texto.")
    sys.stdout.flush()
    for _ in range(3):
        time.sleep(0.5)
        sys.stdout.write(".")
        sys.stdout.flush()
    
    # Pausa antes de mostrar el resultado
    time.sleep(1) 
    
    # Listas de opciones de mensajes
    intro_options = [
        "✨ ¿Te da curiosidad ver la siguiente emoción? ✨",
        "✨ Nos llama la atención la próxima emoción✨",
        "✨ ¿Estás listo para cómo es la siguiente emoción del texto? ✨",
        "✨ ¡Visualizando una nueva emoción! 🚀"
    ]
    
    # Se ha corregido la lógica para que los mensajes usen la variable correcta
    emoji_list= [random.choice(EMOTION_EMOJIS.get(emocion1, 'None')),
                 random.choice(EMOTION_EMOJIS.get(emocion1, 'None')),
                 random.choice(EMOTION_EMOJIS.get(emocion1, 'None')),
                 random.choice(EMOTION_EMOJIS.get(emocion2, 'None')),
                 random.choice(EMOTION_EMOJIS.get(emocion2, 'None')),
                 random.choice(EMOTION_EMOJIS.get(emocion2, 'None'))]
    main_emotions_options = [
        f"{emoji_list[0]} Creemos que la emoción principal de tu texto es {emocion1}. {emoji_list[1]}",
        f"{emoji_list[0]} {emocion1} es lo primero que se nos viene a la mente al leerlo. {emoji_list[1]}",
        f"{emoji_list[0]} Posiblemente sientas bastante {emocion1}. {emoji_list[1]}",
        f"{emoji_list[0]} Principalmente {emocion1} es la emoción que se transmite. {emoji_list[1]}"
    ]

    secondary_emotions_options = [
        f"{emoji_list[3]} Con una pizca de {emocion2} {emoji_list[4]}",
        f"{emoji_list[3]} Mezclado con {emocion2} posiblemente {emoji_list[4]}",
        f"{emoji_list[3]} Pero también un poco de {emocion2} {emoji_list[4]}",
        f"{emoji_list[3]} Y un toque de {emocion2} {emoji_list[4]}"
    ]

    matiz_messages_options = [
        f"{emoji_list[2]} resultando en {matiz}{emoji_list[5]}",
        f"{emoji_list[2]} obteniendo un matiz {matiz}{emoji_list[5]}",
        f"{emoji_list[2]} según la rueda de las emociones, esta combinación es {matiz}{emoji_list[5]}",
        f"{emoji_list[2]} consiguiendo una nueva emoción compleja {matiz}{emoji_list[5]}"
    ]

    # Mensajes
    messages = [
        random.choice(intro_options),
        f"📖 En el fragmento de texto donde dices '{fragmento}'",
        random.choice(main_emotions_options)
    ]
    
    if emocion2 and emocion2.lower() not in ["none", "ninguno"]:
        messages.append(random.choice(secondary_emotions_options))
    
    if matiz and matiz.lower() not in ["none", "ninguno"]:
        messages.append(random.choice(matiz_messages_options))
        
    for msg in messages:
        for char in msg:
            sys.stdout.write(char)
            sys.stdout.flush()
            time.sleep(0.02)
        sys.stdout.write("\n")
    
    sys.stdout.write("✨" * 40 + "\n\n")
    sys.stdout.flush()

EMOTION_EMOJIS = {
    "Serenidad": ["😌", "🧘", "✨"],
    "Alegría": ["😄", "🥳", "🎉"],
    "Éxtasis": ["🤩", "💫", "💖"],
    "Aceptación": ["😊", "🤝", "👌"],
    "Confianza": ["💪", "💯", "🛡️"],
    "Admiración": ["😮", "👏", "🤩"],
    "Aprensión": ["😬", "😥", "😨"],
    "Miedo": ["😱", "😰", "👻"],
    "Terror": ["😨", "💀", "👹"],
    "Distracción": ["🤔", "🤨", "🤷"],
    "Sorpresa": ["😲", "😮", "😳"],
    "Asombro": ["🤯", "✨", "😮"],
    "Melancolía": ["😔", "🍂", "🌧️"],
    "Tristeza": ["😢", "😭", "💔"],
    "Pena": ["😥", "😔", "😢"],
    "Aburrimiento": ["🥱", "😑", "💤"],
    "Asco": ["🤢", "🤮", "😖"],
    "Odio": ["😡", "😠", "👿"],
    "Enfado": ["😤", "💢", "😡"],
    "Ira": ["🤬", "🔥", "💥"],
    "Furia": ["👹", "🌋", "🤯"],
    "Interés": ["🧐", "👀", "💡"],
    "Anticipación": ["⏳", "🔍", "👀"],
    "Vigilancia": ["🚨", "👀", "🕵️"],
    "None": ["❓", "❔", "❓"]
}