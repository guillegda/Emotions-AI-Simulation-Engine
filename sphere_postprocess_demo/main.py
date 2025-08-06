
import glfw
import moderngl
import numpy as np
import time
from pyrr import Matrix44

# Cargar la esfera
vertices = np.load("sphere_demo/vertices.npy")
indices = np.load("sphere_demo/indices.npy")

# Inicializar GLFW
if not glfw.init():
    raise Exception("No se pudo iniciar GLFW")

window = glfw.create_window(800, 600, "Esfera con Postproceso", None, None)
if not window:
    glfw.terminate()
    raise Exception("No se pudo crear la ventana")

glfw.make_context_current(window)
ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST) # type: ignore[attr-defined]

# Framebuffer para postproceso
fbo = ctx.framebuffer(
    color_attachments=[ctx.texture((800, 600), 4)],
    depth_attachment=ctx.depth_renderbuffer((800, 600))
)

# Shader para esfera
prog_sphere = ctx.program(
    vertex_shader=open("sphere_postprocess_demo/sphere_vert.glsl").read(),
    fragment_shader=open("sphere_postprocess_demo/sphere_frag.glsl").read()
)

# Shader para postproceso
prog_post = ctx.program(
    vertex_shader=open("sphere_postprocess_demo/post_vert.glsl").read(),
    fragment_shader=open("sphere_postprocess_demo/post_frag.glsl").read()
)

# Buffers de la esfera
vbo = ctx.buffer(vertices.astype('f4').tobytes())
ibo = ctx.buffer(indices.astype('i4').tobytes())
vao_sphere = ctx.simple_vertex_array(prog_sphere, vbo, 'in_position', index_buffer=ibo)

# Quad de pantalla para postproceso
quad_vertices = np.array([
    -1, -1, 0, 0,
     1, -1, 1, 0,
    -1,  1, 0, 1,
     1,  1, 1, 1,
], dtype='f4')

quad_vbo = ctx.buffer(quad_vertices.tobytes())
vao_post = ctx.simple_vertex_array(prog_post, quad_vbo, 'in_pos', 'in_uv')

projection = Matrix44.perspective_projection(45.0, 800 / 600, 0.1, 100.0)
view = Matrix44.look_at((0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))

start = time.time()

while not glfw.window_should_close(window):
    glfw.poll_events()
    now = time.time() - start

    # Renderizar la esfera al framebuffer
    fbo.use()
    ctx.clear(0.1, 0.1, 0.15)
    model = Matrix44.from_y_rotation(now * 0.5)

    prog_sphere['time'].value = now
    prog_sphere['model'].write(model.astype('f4').tobytes())
    prog_sphere['view'].write(view.astype('f4').tobytes())
    prog_sphere['projection'].write(projection.astype('f4').tobytes())
    vao_sphere.render()

    # Renderizar postproceso a pantalla
    ctx.screen.use()
    ctx.clear()
    fbo.color_attachments[0].use(location=0)
    prog_post['texture0'].value = 0
    prog_post['resolution'].value = (800.0, 600.0)
    vao_post.render(moderngl.TRIANGLE_STRIP) # type: ignore[attr-defined]

    glfw.swap_buffers(window)

glfw.terminate()
