import glfw
import moderngl
import numpy as np
import time
from pyrr import Matrix44

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
        """Inicia la transición al siguiente conjunto de parámetros de la lista de emociones."""
        if self.current_index < len(self.emotions_list):
            self.params_A = self.params_B.copy()
            self.params_B = self.emotions_list[self.current_index].copy()
            self.is_transitioning = True
            self.transition_start_time = time.time()
            print(f"[INFO] Iniciando transición a la emoción {self.current_index + 1}: {self.params_B.get('emocion1', 'N/A')}")
            self.current_index += 1
        else:
            print("[INFO] Se ha alcanzado el final de la lista de emociones.")
            self.terminate()

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


def start_glfw_simulation(emotions_list):
    """
    inicializa y ejecuta el bucle de simulación de la esfera.
    """
    if not glfw.init():
        return
    
    width, height = 1280, 720
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

    window = glfw.create_window(width, height, "Deformable Sphere Simulator", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)

    simulator = SphereSimulator(window, width, height, emotions_list=emotions_list)
    
    # Inicia la primera transición si hay emociones en la lista
    if emotions_list:
        simulator.start_next_transition()

    while not glfw.window_should_close(window):
        now = time.time()
        
        # Lógica de input
        if glfw.get_key(window, glfw.KEY_ENTER) == glfw.PRESS and not simulator.is_transitioning:
            simulator.start_next_transition()

        simulator.render(now)
        glfw.swap_buffers(window)
        glfw.poll_events()

    simulator.terminate()
    glfw.terminate()