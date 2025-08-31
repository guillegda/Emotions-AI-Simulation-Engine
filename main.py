from interface_app import InterfaceApp
from sphere_simulator import start_glfw_simulation
def main():
    """
    Main function that orchestrates the program's execution.
    """
    while True:
        # app = InterfaceApp()
        # app.mainloop()

        # if app.simulation_parameters_list:
        #     start_glfw_simulation(app.simulation_parameters_list)
        # else:
        #     print("No simulation parameters available. Exiting.")
        #     break

        example_emotions = [
            # {'fragment': 'Fragmento de Éxtasis'
            #  , 'emocion1': 'Éxtasis', 'emocion2': 'None', 'matiz': 'None', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.3, 'wave_direction': 0, 'color1': (0.0, 0.64, 0.90), 'color2': (0.1, 0.99, 0.1), 'deform_mode': 3, "hybrid_amnts": [0.5, 0.5, 0.0]},
            #{'emocion1': 'Confusión', 'color': (0.5, 0.5, 0.5), 'velocidad': 5.0, 'rugosidad': 10.0, 'distorsion': 0.1, 'wave_direction': 0, 'deform_mode': 3, 'hybrid_amnts': [0.5, 0.5, 0.0]},
            ##
            {'fragment': 'Fragmento de Serenidad'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Alegría'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Éxtasis'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
            ##
            {'fragment': 'Fragmento de Aceptación'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Confianza'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Admiración'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
            ##
            {'fragment': 'Fragmento de Aprensión'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Miedo'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Terror'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
            ##
            {'fragment': 'Fragmento de Distracción'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Sorpresa'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Asombro'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
            ##
            {'fragment': 'Fragmento de Melancolía'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Tristeza'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Pena'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
            {'fragment': 'Fragmento de Aburrimiento'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Asco'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Odio'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
            ##
            {'fragment': 'Fragmento de Enfado'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Ira'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Furia'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
            ##
            {'fragment': 'Fragmento de Interés'
             , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Anticipación'
             , 'emocion1': 'Alegría', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            {'fragment': 'Fragmento de Vigilancia'
             , 'emocion1': 'Éxtasis', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.80, 0.10, 0.10), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.5]},
            ##
        ]
        start_glfw_simulation(example_emotions)
        break

if __name__ == "__main__":
    simulator = None
    main()