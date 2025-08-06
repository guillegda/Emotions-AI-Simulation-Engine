
import glfw
import moderngl
import numpy as np
import time
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
blur_strength = 3
deform_mode = 0

while not glfw.window_should_close(window):
    glfw.poll_events()
    now = time.time() - start

    # Control con teclas : No sé si me apetece ponerlo
    # if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
    #     blur_strength += 0.1
    # if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
    #     blur_strength = max(0.0, blur_strength - 0.1)

    # --- Control de modo de deformación con teclas ---
    if glfw.get_key(window, glfw.KEY_1) == glfw.PRESS:
        deform_mode = 0 # Ondas
    if glfw.get_key(window, glfw.KEY_2) == glfw.PRESS:
        deform_mode = 1 # Burbujas
    if glfw.get_key(window, glfw.KEY_3) == glfw.PRESS:
        deform_mode = 2 # Pinchos

    # Renderizado a framebuffer
    fbo.use()
    ctx.clear(0.1, 0.1, 0.15)
    #model = Matrix44.from_y_rotation(now * 0.4) # Si quiero que rote la matriz modelo en el eje y
    model = Matrix44.identity()

    prog_sphere['time'].value = now
    prog_sphere['model'].write(model.astype('f4').tobytes())
    prog_sphere['view'].write(view.astype('f4').tobytes())
    prog_sphere['projection'].write(projection.astype('f4').tobytes())
    prog_sphere['deform_mode'].value = deform_mode
    vao_sphere.render()

    # Postproceso
    ctx.screen.use()
    ctx.clear()
    fbo.color_attachments[0].use(location=0)
    #Damos valor a las variables de entrada de post_frag.glsl
    prog_post['texture0'].value = 0
    prog_post['resolution'].value = (800.0, 600.0)
    prog_post['blur_strength'].value = blur_strength
    vao_post.render(moderngl.TRIANGLE_STRIP)

    glfw.swap_buffers(window)

glfw.terminate()
