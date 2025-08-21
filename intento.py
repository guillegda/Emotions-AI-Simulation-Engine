import json
import time

class SimulationApp:
    """
    Clase para manejar la simulación de transiciones emocionales
    basadas en un JSON de fragmentos de texto.
    """

    def __init__(self):
        """
        Inicializa la aplicación cargando los datos y configurando el estado inicial.
        """
        self.json_data = [
            {
                "fragmento": "Una vez, hace como tres años, me pasó algo raro que todavía no sé bien cómo procesar.",
                "tipo1": "Sorpresa", "intensidad1": "Sorpresa",
                "tipo2": "Tristeza", "intensidad2": "Melancolía",
                "matiz": "Decepción"
            },
            {
                "fragmento": "Estaba en una reunión familiar, de esas donde hay demasiada comida, risas forzadas y gente que no ves desde hace siglos.",
                "tipo1": "Alegría", "intensidad1": "Alegría",
                "tipo2": "Animadversión", "intensidad2": "Aburrimiento",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Todo iba bien, bastante normal, hasta que apareció mi papá con su nueva pareja.",
                "tipo1": "Sorpresa", "intensidad1": "Sorpresa",
                "tipo2": "Ninguno", "intensidad2": "Ninguno",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Nadie nos había dicho nada.",
                "tipo1": "Sorpresa", "intensidad1": "Sorpresa",
                "tipo2": "Ninguno", "intensidad2": "Ninguno",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Fue un golpe raro. No porque no pudiera rehacer su vida, sino porque fue tan repentino… y justo ahí, sin previo aviso.",
                "tipo1": "Sorpresa", "intensidad1": "Asombro",
                "tipo2": "Ira", "intensidad2": "Enfado",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Sentí como una mezcla entre sorpresa, incomodidad, un poco de rabia y también una culpa que no sabía de dónde venía.",
                "tipo1": "Sorpresa", "intensidad1": "Sorpresa",
                "tipo2": "Ira", "intensidad2": "Ira",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Sentí como una mezcla entre sorpresa, incomodidad, un poco de rabia y también una culpa que no sabía de dónde venía.",
                "tipo1": "Tristeza", "intensidad1": "Tristeza",
                "tipo2": "Animadversión", "intensidad2": "Asco",
                "matiz": "Remordimiento"
            },
            {
                "fragmento": "Me vi sonriendo para ser amable, diciendo cosas como “un gusto” y “qué bueno verte bien”, mientras por dentro tenía un nudo en la garganta.",
                "tipo1": "Alegría", "intensidad1": "Alegría",
                "tipo2": "Tristeza", "intensidad2": "Tristeza",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Al mismo tiempo me sentía ridículo por reaccionar así, como si tuviera 12 años.",
                "tipo1": "Tristeza", "intensidad1": "Melancolía",
                "tipo2": "Ninguno", "intensidad2": "Ninguno",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Pero también me sentí fuera de lugar, como si no perteneciera a esa escena, como si todos hubieran avanzado y yo me hubiera quedado en pausa.",
                "tipo1": "Tristeza", "intensidad1": "Tristeza",
                "tipo2": "Miedo", "intensidad2": "Aprensión",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Después, mientras todos seguían charlando como si nada, me fui al patio con una copa de vino, solo.",
                "tipo1": "Tristeza", "intensidad1": "Tristeza",
                "tipo2": "Ninguno", "intensidad2": "Ninguno",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Y ahí me invadió una tristeza medio inesperada, no por él exactamente, sino porque me di cuenta de que algo se había terminado para siempre, aunque no supiera bien qué.",
                "tipo1": "Tristeza", "intensidad1": "Pena",
                "tipo2": "Ninguno", "intensidad2": "Ninguno",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Lo curioso es que también sentí un alivio, como si ver eso con mis propios ojos me sacara de una fantasía en la que seguía esperando que las cosas volvieran a ser como antes.",
                "tipo1": "Alegría", "intensidad1": "Serenidad",
                "tipo2": "Sorpresa", "intensidad2": "Sorpresa",
                "matiz": "Ninguno"
            },
            {
                "fragmento": "Fue duro, pero necesario, creo.",
                "tipo1": "Tristeza", "intensidad1": "Melancolía",
                "tipo2": "Aceptación", "intensidad2": "Aceptación",
                "matiz": "Ninguno"
            }
        ]
        self.current_fragment_index = 0
        self.current_params = None
        self.next_params = None
        
        # Diccionario de mapeo de intensidad a parámetros de simulación
        self.emotion_map = {
            "Sorpresa": {"color": (0.0, 0.5, 1.0), "velocidad": 0.8, "rugosidad": 0.5, "distorsion": 0.9, "wave_direction": 1.0},
            "Melancolía": {"color": (0.4, 0.4, 0.6), "velocidad": 0.2, "rugosidad": 0.8, "distorsion": 0.3, "wave_direction": -0.5},
            "Alegría": {"color": (1.0, 0.8, 0.0), "velocidad": 1.2, "rugosidad": 0.2, "distorsion": 0.1, "wave_direction": 1.5},
            "Aburrimiento": {"color": (0.6, 0.6, 0.6), "velocidad": 0.1, "rugosidad": 0.9, "distorsion": 0.2, "wave_direction": 0.0},
            "Asombro": {"color": (0.2, 0.8, 0.8), "velocidad": 1.0, "rugosidad": 0.4, "distorsion": 1.0, "wave_direction": 1.2},
            "Enfado": {"color": (1.0, 0.2, 0.2), "velocidad": 1.5, "rugosidad": 0.7, "distorsion": 0.8, "wave_direction": -1.0},
            "Ira": {"color": (1.0, 0.1, 0.1), "velocidad": 1.8, "rugosidad": 0.9, "distorsion": 1.2, "wave_direction": -1.5},
            "Tristeza": {"color": (0.2, 0.2, 0.8), "velocidad": 0.3, "rugosidad": 0.9, "distorsion": 0.4, "wave_direction": -0.8},
            "Asco": {"color": (0.5, 0.8, 0.2), "velocidad": 0.7, "rugosidad": 1.0, "distorsion": 0.6, "wave_direction": -0.2},
            "Aprensión": {"color": (0.8, 0.6, 0.2), "velocidad": 0.5, "rugosidad": 0.6, "distorsion": 0.5, "wave_direction": -0.3},
            "Pena": {"color": (0.3, 0.3, 0.9), "velocidad": 0.2, "rugosidad": 0.9, "distorsion": 0.3, "wave_direction": -0.7},
            "Serenidad": {"color": (0.2, 0.8, 0.2), "velocidad": 0.4, "rugosidad": 0.1, "distorsion": 0.1, "wave_direction": 0.5},
            "Aceptación": {"color": (0.8, 0.8, 0.8), "velocidad": 0.3, "rugosidad": 0.2, "distorsion": 0.2, "wave_direction": 0.1},
            "Ninguno": {"color": (0.5, 0.5, 0.5), "velocidad": 0.0, "rugosidad": 0.0, "distorsion": 0.0, "wave_direction": 0.0},
        }

    def _get_params_from_emotion(self, intensity):
        """
        Devuelve los parámetros de simulación para una intensidad de emoción dada.
        """
        return self.emotion_map.get(intensity, self.emotion_map["Ninguno"])

    def _calculate_parameters(self, fragment):
        """
        Calcula los parámetros de simulación basados en la intensidad del fragmento.
        Por ahora, solo usa 'intensidad1' como se solicitó.
        """
        intensity1 = fragment.get('intensidad1')
        params = self._get_params_from_emotion(intensity1)
        return {
            'color': params['color'],
            'velocidad': params['velocidad'],
            'rugosidad': params['rugosidad'],
            'distorsion': params['distorsion'],
            'wave_direction': params['wave_direction']
        }
        
    def _update_transition(self, now):
        """
        Función de ejemplo para gestionar la transición entre los parámetros.
        Aquí es donde conectarías con tu motor de simulación.
        
        Args:
            now: Un valor de tiempo que representa el progreso de la transición.
        """
        if self.current_params and self.next_params:
            # Lógica para interpolar entre self.current_params y self.next_params
            print(f"--- Transición iniciada en el tiempo {now:.2f} ---")
            print(f"  Parámetros actuales (A): {self.current_params}")
            print(f"  Parámetros siguientes (B): {self.next_params}")
            
            # Ejemplo de cómo se podrían usar los parámetros en tu simulación
            # Ejemplo de deform_mode_A y deform_mode_B
            deform_mode_A = self.current_params['distorsion']
            deform_mode_B = self.next_params['distorsion']
            
            print(f"  Ejemplo de transición: deform_mode_A={deform_mode_A}, deform_mode_B={deform_mode_B}")
            print("---------------------------------------")

    def handle_enter_key(self):
        """
        Maneja la acción de la tecla Enter para avanzar al siguiente fragmento.
        """
        # Procesar el fragmento actual
        if self.current_fragment_index < len(self.json_data):
            current_fragment = self.json_data[self.current_fragment_index]
            self.current_params = self._calculate_parameters(current_fragment)
            
            # Preparar los parámetros para el siguiente fragmento
            if self.current_fragment_index + 1 < len(self.json_data):
                next_fragment = self.json_data[self.current_fragment_index + 1]
                self.next_params = self._calculate_parameters(next_fragment)
            else:
                self.next_params = None  # No hay más fragmentos
            
            # Imprimir los parámetros para depuración
            print(f"\n--- Fragmento {self.current_fragment_index + 1} ---")
            print(f"Fragmento: '{current_fragment['fragmento']}'")
            print(f"Intensidad 1: {current_fragment['intensidad1']}")
            print(f"Parámetros calculados: {self.current_params}")
            if self.next_params:
                print(f"Próximos parámetros: {self.next_params}")
            else:
                print("Fin de la lista de fragmentos.")
                
            # Llamar a la función de transición
            self._update_transition(time.time())
            
            # Avanzar al siguiente fragmento
            self.current_fragment_index += 1
        else:
            print("\nTodos los fragmentos han sido procesados. Reiniciando la simulación.")
            self.current_fragment_index = 0
            self.current_params = None
            self.next_params = None
            self.handle_enter_key()


# --- Bloque principal para demostrar el uso ---
if __name__ == "__main__":
    app = SimulationApp()
    
    # Simular la pulsación de la tecla Enter
    print("Simulación iniciada. Pulsa la tecla Enter en la consola para avanzar de fragmento.")
    print("Para salir, cierra el programa.")
    
    while True:
        input_command = input("Pulsa 'Enter' para continuar: ")
        if input_command == "":
            app.handle_enter_key()
        else:
            print("Entrada no válida.")

