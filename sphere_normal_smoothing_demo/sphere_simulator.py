
#sphere_simulator.py
import glfw
import moderngl
import numpy as np
import time
import random
from pyrr import Matrix44

# Cargar malla de esfera
# vertices = np.load("sphere_demo/vertices.npy")
# indices = np.load("sphere_demo/indices.npy")
vertices = np.load("vertices_high_res.npy")
indices = np.load("indices_high_res.npy")

# Inicializar ventana GLFW
if not glfw.init():
    raise Exception("No se pudo iniciar GLFW")

window = glfw.create_window(800, 600, "Suavizado simulado de normales", None, None)
if not window:
    glfw.terminate()
    raise Exception("No se pudo crear la ventana")

glfw.make_context_current(window)
ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST)

# Framebuffer de renderizado
fbo = ctx.framebuffer(
    color_attachments=[ctx.texture((800, 600), 4)],
    depth_attachment=ctx.depth_renderbuffer((800, 600))
)

# Shader para renderizar la esfera (con normales simuladas)
prog_sphere = ctx.program(
    vertex_shader=open("sphere_normal_smoothing_demo/sphere_vert.glsl").read(),
    fragment_shader=open("sphere_normal_smoothing_demo/sphere_frag.glsl").read()
)

# Shader de postproceso con detección de bordes y suavizado
prog_post = ctx.program(
    vertex_shader=open("sphere_normal_smoothing_demo/post_vert.glsl").read(),
    fragment_shader=open("sphere_normal_smoothing_demo/post_frag.glsl").read()
)

# VAO de la esfera
vbo = ctx.buffer(vertices.astype('f4').tobytes())
ibo = ctx.buffer(indices.astype('i4').tobytes())
vao_sphere = ctx.simple_vertex_array(prog_sphere, vbo, 'in_position', index_buffer=ibo)

# Cuadro de pantalla para postproceso
quad_vertices = np.array([
    -1, -1, 0, 0,
     1, -1, 1, 0,
    -1,  1, 0, 1,
     1,  1, 1, 1,
], dtype='f4')
quad_vbo = ctx.buffer(quad_vertices.tobytes())
vao_post = ctx.simple_vertex_array(prog_post, quad_vbo, 'in_pos', 'in_uv')

# Matrices de proyección y vista
projection = Matrix44.perspective_projection(45.0, 800 / 600, 0.1, 100.0)
view = Matrix44.look_at((0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))

start = time.time()
blur_strength = 5
deform_mode = 0
bloom_amount = 10.5

# Variables de control de la transición
deform_mode_A = 0
deform_mode_B = 0
blend_factor = 0.0
transition_duration = 0.5 # Duración de la transición en segundos
transition_start_time = 0.0
is_transitioning = False
hybrid_amnts_A = [0.0, 0.0, 0.0]
hybrid_amnts_B = [0.0, 0.0, 0.0]

while not glfw.window_should_close(window):
    glfw.poll_events()
    now = time.time() - start

    # Control con teclas : No sé si me apetece ponerlo
    # if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
    #     blur_strength += 0.1
    # if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
    #     blur_strength = max(0.0, blur_strength - 0.1)

    # --- Control de modo de deformación con teclas ---
    new_mode = -1
    if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS:
        new_mode = 0
    if glfw.get_key(window, glfw.KEY_2) == glfw.PRESS:
        new_mode = 1
    if glfw.get_key(window, glfw.KEY_3) == glfw.PRESS:
        new_mode = 2
    if glfw.get_key(window, glfw.KEY_4) == glfw.PRESS:
        new_mode = 3 # Modo Híbrido

    if new_mode != -1 and new_mode != deform_mode_A and not is_transitioning:
        deform_mode_B = new_mode
        is_transitioning = True
        transition_start_time = now

        # Si el nuevo modo es híbrido, generamos los nuevos porcentajes
        if new_mode == 3:
            # Los valores actuales (A) pasan a ser los futuros (B)
            hybrid_amnts_A = hybrid_amnts_B.copy()
            # Y generamos los nuevos valores para el modo B
            total = 0.0
            new_amnts = [0.0, 0.0, 0.0]
            for i in range(3):
                new_amnts[i] = random.uniform(0.0, 1.0)
                total += new_amnts[i]
            # Normalizamos para que la suma sea 1.0
            hybrid_amnts_B = [a / total for a in new_amnts]

    if is_transitioning:
        elapsed_time = now - transition_start_time
        blend_factor = min(elapsed_time / transition_duration, 1.0)
        if blend_factor >= 1.0:
            deform_mode_A = deform_mode_B
            is_transitioning = False
            blend_factor = 0.0
            if deform_mode_A == 3:
                hybrid_amnts_A = hybrid_amnts_B.copy()
            else:
                hybrid_amnts_A = [0.0, 0.0, 0.0]
    
    # Renderizado a framebuffer
    fbo.use()
    ctx.clear(0.05, 0.05, 0.05) # Color de fondo de la escena
    #model = Matrix44.from_y_rotation(now * 0.4) # Con rotación de la esfera
    model = Matrix44.identity() # Sin rotación de la esfera

    # Parámetros manipulables en tiempo real:
    prog_sphere['time'].value = now
    prog_sphere['velocidad'].value = 5.0
    prog_sphere['rugosidad'].value = 10.0
    prog_sphere['distorsion'].value = 0.1
    prog_sphere['wave_direction'].value = 0
    prog_sphere['model'].write(model.astype('f4').tobytes())
    prog_sphere['view'].write(view.astype('f4').tobytes())
    prog_sphere['projection'].write(projection.astype('f4').tobytes())
    
    # Enviamos los nuevos uniformes para la transición
    prog_sphere['deform_mode_A'].value = deform_mode_A
    prog_sphere['deform_mode_B'].value = deform_mode_B
    prog_sphere['blend_factor'].value = blend_factor

    # Enviamos valores para los efectos hibridos
    prog_sphere['effect1_amnt_A'].value = hybrid_amnts_A[0]
    prog_sphere['effect2_amnt_A'].value = hybrid_amnts_A[1]
    prog_sphere['effect3_amnt_A'].value = hybrid_amnts_A[2]
    prog_sphere['effect1_amnt_B'].value = hybrid_amnts_B[0]
    prog_sphere['effect2_amnt_B'].value = hybrid_amnts_B[1]
    prog_sphere['effect3_amnt_B'].value = hybrid_amnts_B[2]

    vao_sphere.render()

    # Postproceso
    ctx.screen.use()
    ctx.clear()
    fbo.color_attachments[0].use(location=0)
    #Damos valor a las variables de entrada de post_frag.glsl
    prog_post['texture0'].value = 0
    prog_post['resolution'].value = (800.0, 600.0)
    prog_post['blur_strength'].value = blur_strength # esto es manipulable en tiempo real también
    vao_post.render(moderngl.TRIANGLE_STRIP)

    glfw.swap_buffers(window)

glfw.terminate()
