# sphere_simulator.py

import glfw
import moderngl
import numpy as np
import time
import random
from pyrr import Matrix44

class SphereSimulator:
    """
    Clase reutilizable para la simulación de una esfera con deformaciones
    y postproceso usando ModernGL y GLFW.

    Encapsula toda la lógica de inicialización y renderizado de un solo fotograma.
    """

    def __init__(self, window, width: int = 800, height: int = 600):
        """
        Inicializa el contexto de ModernGL, los shaders y la
        geometría de la esfera.

        Args:
            window (glfw.Window): La ventana de GLFW a la que se renderizará.
            width (int): Ancho de la ventana.
            height (int): Altura de la ventana.
        """
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

        # Parámetros de la simulación (ahora pueden ser manipulados desde fuera)
        self.blur_strength = 5.0
        self.deform_mode_A = 0
        self.deform_mode_B = 0
        self.blend_factor = 0.0
        self.transition_duration = 0.5
        self.transition_start_time = 0.0
        self.is_transitioning = False
        self.hybrid_amnts_A = [0.0, 0.0, 0.0]
        self.hybrid_amnts_B = [0.0, 0.0, 0.0]
        self.velocidad = 5.0
        self.rugosidad = 10.0
        self.distorsion = 0.1
        self.wave_direction = 0

        # parámetros de color para los shaders
        self.base_color = (1.0, 0.5, 0.2)
        self.light_color1 = (1.0, 1.0, 1.0)
        self.light_color2 = (0.5, 0.5, 0.5)

        self._init_moderngl()
        self._load_shaders()
        self._load_mesh()
        self._setup_framebuffer()
        self._setup_matrices()
    
    def _init_moderngl(self):
        """Crea el contexto de ModernGL y configura el estado inicial."""
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

    def _load_shaders(self):
        """Carga y compila los shaders desde archivos."""
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
            print(f"Error: No se encontró el archivo de shader. Asegúrate de que los archivos .glsl están en la ruta correcta. Detalles: {e}")
            raise

    def _load_mesh(self):
        """Carga la malla de la esfera desde archivos .npy y crea los VAOs."""
        try:
            vertices = np.load("vertices_high_res.npy")
            indices = np.load("indices_high_res.npy")

            vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
            ibo = self.ctx.buffer(indices.astype('i4').tobytes())
            self.vao_sphere = self.ctx.simple_vertex_array(self.prog_sphere, vbo, 'in_position', index_buffer=ibo)
        except FileNotFoundError as e:
            print(f"Error: No se encontró el archivo de malla. Asegúrate de que los archivos .npy están en la ruta correcta. Detalles: {e}")
            raise
        
        # Cuadro de pantalla para postproceso
        quad_vertices = np.array([
            -1, -1, 0, 0,
             1, -1, 1, 0,
            -1,  1, 0, 1,
             1,  1, 1, 1,
        ], dtype='f4')
        quad_vbo = self.ctx.buffer(quad_vertices.tobytes())
        self.vao_post = self.ctx.simple_vertex_array(self.prog_post, quad_vbo, 'in_pos', 'in_uv')

    def _setup_framebuffer(self):
        """Configura el framebuffer para renderizar fuera de pantalla."""
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.width, self.height), 4)],
            depth_attachment=self.ctx.depth_renderbuffer((self.width, self.height))
        )

    def _setup_matrices(self):
        """Configura las matrices de proyección y vista."""
        self.projection = Matrix44.perspective_projection(45.0, self.width / self.height, 0.1, 100.0)
        self.view = Matrix44.look_at((0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))

    def _handle_input(self, now):
        """Gestiona la entrada del teclado para cambiar modos de deformación."""
        new_mode = -1
        if glfw.get_key(self.window, glfw.KEY_1) == glfw.PRESS:
            new_mode = 0
        if glfw.get_key(self.window, glfw.KEY_2) == glfw.PRESS:
            new_mode = 1
        if glfw.get_key(self.window, glfw.KEY_3) == glfw.PRESS:
            new_mode = 2
        if glfw.get_key(self.window, glfw.KEY_4) == glfw.PRESS:
            new_mode = 3

        if new_mode != -1 and not self.is_transitioning:# and new_mode != self.deform_mode_A:
            print(f"Cambiando al modo de deformación {new_mode}")
            self.deform_mode_B = new_mode
            self.is_transitioning = True
            self.transition_start_time = now

            if new_mode == 3:
                self.hybrid_amnts_A = self.hybrid_amnts_B.copy()
                total = 0.0
                new_amnts = [random.uniform(0.0, 1.0) for _ in range(3)]
                total = sum(new_amnts)
                self.hybrid_amnts_B = [a / total for a in new_amnts]
        
    def _update_transition(self, now):
        """Actualiza el factor de mezcla de la transición entre modos."""
        if self.is_transitioning:
            elapsed_time = now - self.transition_start_time
            self.blend_factor = min(elapsed_time / self.transition_duration, 1.0)
            if self.blend_factor >= 1.0:
                self.deform_mode_A = self.deform_mode_B
                self.is_transitioning = False
                self.blend_factor = 0.0
                if self.deform_mode_A == 3:
                    self.hybrid_amnts_A = self.hybrid_amnts_B.copy()
                else:
                    self.hybrid_amnts_A = [0.0, 0.0, 0.0]

    def render(self, now):
        """
        Dibuja un solo fotograma de la simulación.
        
        Args:
            now (float): Tiempo actual de la simulación.
        """
        # Procesar entrada y transiciones antes de renderizar
        self._handle_input(now)
        self._update_transition(now)

        # Renderizado a framebuffer
        self.fbo.use()
        self.ctx.clear(0.05, 0.05, 0.05)
        model = Matrix44.identity()

        # Enviar uniformes al shader de la esfera
        self.prog_sphere['time'].value = now
        self.prog_sphere['velocidad'].value = self.velocidad
        self.prog_sphere['rugosidad'].value = self.rugosidad
        self.prog_sphere['distorsion'].value = self.distorsion
        self.prog_sphere['wave_direction'].value = self.wave_direction
        self.prog_sphere['model'].write(model.astype('f4').tobytes())
        self.prog_sphere['view'].write(self.view.astype('f4').tobytes())
        self.prog_sphere['projection'].write(self.projection.astype('f4').tobytes())

        # Enviar los nuevos uniformes de color al shader
        self.prog_sphere['base_color'].value = self.base_color
        self.prog_sphere['light_color1'].value = self.light_color1
        self.prog_sphere['light_color2'].value = self.light_color2
        
        # Enviar uniformes para la transición de modos
        self.prog_sphere['deform_mode_A'].value = self.deform_mode_A
        self.prog_sphere['deform_mode_B'].value = self.deform_mode_B
        self.prog_sphere['blend_factor'].value = self.blend_factor
        
        # Enviar valores para los efectos hibridos
        self.prog_sphere['effect1_amnt_A'].value = self.hybrid_amnts_A[0]
        self.prog_sphere['effect2_amnt_A'].value = self.hybrid_amnts_A[1]
        self.prog_sphere['effect3_amnt_A'].value = self.hybrid_amnts_A[2]
        self.prog_sphere['effect1_amnt_B'].value = self.hybrid_amnts_B[0]
        self.prog_sphere['effect2_amnt_B'].value = self.hybrid_amnts_B[1]
        self.prog_sphere['effect3_amnt_B'].value = self.hybrid_amnts_B[2]

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
        glfw.terminate()
