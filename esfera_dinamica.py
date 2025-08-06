import glfw
import moderngl
import numpy as np
import time
from pyrr import Matrix44

# Cargar la malla de esfera
vertices = np.load("sphere_demo/vertices.npy")
indices = np.load("sphere_demo/indices.npy")

# Inicializar GLFW
if not glfw.init():
    raise Exception("GLFW no se pudo inicializar")

window = glfw.create_window(800, 600, "Esfera Dinámica", None, None)
if not window:
    glfw.terminate()
    raise Exception("No se pudo crear la ventana")

glfw.make_context_current(window)

# Crear contexto moderngl
ctx = moderngl.create_context()
ctx.enable(moderngl.DEPTH_TEST) # type: ignore[attr-defined]

# Vertex & Fragment shaders
prog = ctx.program(
    vertex_shader="""
        #version 330
        in vec3 in_position;
        uniform float time;
        uniform mat4 model;
        uniform mat4 projection;
        uniform mat4 view;

        void main() {
            vec3 pos = in_position;
            float deform = sin(time * 3.0 + pos.y * 10.0) * 0.1;
            pos += normalize(pos) * deform;
            gl_Position = projection * view * model * vec4(pos, 1.0);
        }
    """,
    fragment_shader="""
        #version 330
        out vec4 f_color;
        uniform float time;

        void main() {
            float r = 0.6 + 0.4 * sin(time);
            float g = 0.5 + 0.5 * cos(time * 1.2);
            float b = 0.7 + 0.3 * sin(time * 0.8);

            float softness = 0.9;
            float brightness = 0.3 + 0.7 * abs(sin(time * 2.0));
            brightness = pow(brightness, softness); // curva suavizada

            f_color = vec4(r * brightness, g * brightness, b * brightness, 1.0);
        }
    """
)

# Buffers y Vertex Array Object
vbo = ctx.buffer(vertices.astype('f4').tobytes())
ibo = ctx.buffer(indices.astype('i4').tobytes())
vao = ctx.simple_vertex_array(prog, vbo, 'in_position', index_buffer=ibo)

# Matrices
projection = Matrix44.perspective_projection(45.0, 800 / 600, 0.1, 100.0)
view = Matrix44.look_at(
    eye=(0.0, 0.0, 3.0),
    target=(0.0, 0.0, 0.0),
    up=(0.0, 1.0, 0.0)
)

start_time = time.time()

# Bucle principal
while not glfw.window_should_close(window):
    glfw.poll_events()
    ctx.clear(0.05, 0.05, 0.1)
    
    current_time = time.time() - start_time
    model = Matrix44.from_y_rotation(current_time * 0.5)

    # Uniforms
    prog['time'].value = current_time
    prog['model'].write(model.astype('f4').tobytes())
    prog['view'].write(view.astype('f4').tobytes())
    prog['projection'].write(projection.astype('f4').tobytes())

    vao.render()

    glfw.swap_buffers(window)

glfw.terminate()
