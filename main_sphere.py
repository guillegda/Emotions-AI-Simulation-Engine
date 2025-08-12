# main_sphere.py
import glfw
import time
from sphere_simulator import SphereSimulator

def main():
    """
    Función principal que utiliza la clase SphereSimulator y maneja el
    bucle de renderizado y la entrada del usuario.
    """
    try:
        # Inicializar GLFW
        if not glfw.init():
            raise Exception("No se pudo iniciar GLFW")

        width, height = 1200, 800
        window = glfw.create_window(width, height, "Simulación de Esfera", None, None)
        if not window:
            glfw.terminate()
            raise Exception("No se pudo crear la ventana")

        glfw.make_context_current(window)
        glfw.set_input_mode(window, glfw.STICKY_KEYS, glfw.TRUE)

        # Crea una instancia de la clase de simulación, asumiendo que ahora
        # recibe el contexto de renderizado y no tiene su propio bucle.
        sphere_sim = SphereSimulator(width=width, height=height, window=window)

        # Inicia el bucle principal de la aplicación
        start_time = time.time()
        while not glfw.window_should_close(window):
            glfw.poll_events()
            now = time.time() - start_time

            # --- Manipulación de parámetros en tiempo de ejecución ---
            #
            # Aumento/disminución de la velocidad
            if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
                sphere_sim.velocidad += 0.1
            if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
                sphere_sim.velocidad = max(0.0, sphere_sim.velocidad - 0.1)

            # Aumento/disminución de la rugosidad
            if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
                sphere_sim.rugosidad += 0.1
            if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
                sphere_sim.rugosidad = max(0.0, sphere_sim.rugosidad - 0.1)

            # Aumento/disminución de la distorsión
            if glfw.get_key(window, glfw.KEY_W) == glfw.PRESS:
                sphere_sim.distorsion += 0.01
            if glfw.get_key(window, glfw.KEY_S) == glfw.PRESS:
                sphere_sim.distorsion = max(0.0, sphere_sim.distorsion - 0.01)

            # Cambio de dirección de la onda
            if glfw.get_key(window, glfw.KEY_A) == glfw.PRESS:
                sphere_sim.wave_direction = 0
            if glfw.get_key(window, glfw.KEY_D) == glfw.PRESS:
                sphere_sim.wave_direction = 1

            # Renderiza un solo fotograma
            sphere_sim.render(now)

            # Intercambia los buffers de la ventana
            glfw.swap_buffers(window)

    except Exception as e:
        print(f"Ocurrió un error: {e}")
    finally:
        # Asegúrate de que el método de terminación se llame
        glfw.terminate()

if __name__ == "__main__":
    main()