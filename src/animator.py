import json
import time
import random

class JsonToSphereAnimator:
    """
    Class to parse a JSON string and animate a SphereSimulator
    with random transitions for each key-value pair.
    """

    def __init__(self, sphere_simulator):
        """
        Initializes the animator with a SphereSimulator instance.

        Args:
            sphere_simulator (SphereSimulator): The sphere object to animate.
        """
        self.sphere_simulator = sphere_simulator

    def animate_from_json(self, json_string: str):
        """
        Parses a JSON string and triggers a random transition for each
        key-value pair, with a 2-second delay between transitions.

        Args:
            json_string (str): A JSON string with data to animate the sphere.
        """
        try:
            data = json.loads(json_string)
            if not isinstance(data, dict):
                print("Error: El JSON no es un objeto válido.")
                return

            print("Animación iniciada...")
            time.sleep(1)  # Initial pause before the first animation

            # Iterate through each key-value pair in the JSON
            for key, value in data.items():
                print(f"-> Procesando: '{key}': '{value}'")
                
                # Assign a random deformation mode (0 to 3)
                random_mode = random.randint(0, 3)
                print(f"   Transicionando a modo: {random_mode}")
                self._trigger_transition(random_mode)

                print("   Esperando 2 segundos...")
                time.sleep(2)  # Wait for 2 seconds between transitions

            print("Animación completada.")

        except json.JSONDecodeError:
            print("Error: Cadena JSON inválida.")
        except Exception as e:
            print(f"Ocurrió un error inesperado: {e}")

    def _trigger_transition(self, new_mode: int):
        """
        Programmatically triggers a transition in the SphereSimulator.
        
        Args:
            new_mode (int): The new deformation mode to transition to.
        """
        # We need to simulate the input from the _handle_input method
        # directly in the simulator's state.
        if new_mode != self.sphere_simulator.deform_mode_A and not self.sphere_simulator.is_transitioning:
            now = time.time()
            self.sphere_simulator.deform_mode_B = new_mode
            self.sphere_simulator.is_transitioning = True
            self.sphere_simulator.transition_start_time = now

            if new_mode == 3:
                self.sphere_simulator.hybrid_amnts_A = self.sphere_simulator.hybrid_amnts_B.copy()
                new_amnts = [random.uniform(0.0, 1.0) for _ in range(3)]
                total = sum(new_amnts)
                self.sphere_simulator.hybrid_amnts_B = [a / total for a in new_amnts]