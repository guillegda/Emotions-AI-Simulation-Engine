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
            # #
            # {'fragment': 'Fragmento de Serenidad'
            #  , 'emocion1': 'Serenidad', 'velocidad': 5.15, 'rugosidad': 3.25, 'distorsion': 0.1, 'wave_direction': 2, 'color1': (1.2, 0.90, 0.30), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.9, 0.0]},
            # {'fragment': 'Fragmento de Alegría'
            #  , 'emocion1': 'Alegría', 'velocidad': 10.15, 'rugosidad': 7.25, 'distorsion': 0.1, 'wave_direction': 2, 'color1': (1.30, 1.10, 0.30), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.9, 0.0]},
            # {'fragment': 'Fragmento de Éxtasis'
            #  , 'emocion1': 'Éxtasis', 'velocidad': 12.15, 'rugosidad': 10.25, 'distorsion': 0.1, 'wave_direction': 2, 'color1': (1.59, 1.25, 0.20), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.9, 0.05]},
            # #
            # #
            # {'fragment': 'Fragmento de Aceptación'
            #  , 'emocion1': 'Aceptación', 'velocidad': 2.15, 'rugosidad': 5.25, 'distorsion': 0.1, 'wave_direction': 0, 'color1': (1.0, 1.30, 0.80), 'deform_mode': 3, "hybrid_amnts": [0.1, 0.9, 0.0]},
            # {'fragment': 'Fragmento de Confianza'
            #  , 'emocion1': 'Confianza', 'velocidad': 3.15, 'rugosidad': 8.25, 'distorsion': 0.15, 'wave_direction': 0, 'color1': (1.15, 1.50, 0.70), 'deform_mode': 3, "hybrid_amnts": [0.3, 0.9, 0.0]},
            # {'fragment': 'Fragmento de Admiración'
            #  , 'emocion1': 'Admiración', 'velocidad': 4.15, 'rugosidad': 8.25, 'distorsion': 0.2, 'wave_direction': 0, 'color1': (1.2, 1.60, 0.60), 'deform_mode': 3, "hybrid_amnts": [0.5, 0.9, 0.0]},
            # ##
            ##
            # {'fragment': 'Fragmento de Aprensión'
            #  , 'emocion1': 'Aprensión', 'velocidad': 3.15, 'rugosidad': 1.25, 'distorsion': 0.1, 'wave_direction': 1, 'color1': (0.4, 1.20, 0.70), 'deform_mode': 3, "hybrid_amnts": [0.5, 0.1, 0.5]},
            # {'fragment': 'Fragmento de Miedo'
            #  , 'emocion1': 'Miedo', 'velocidad': 5.15, 'rugosidad': 1.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.4, 1.30, 0.60), 'deform_mode': 3, "hybrid_amnts": [0.5, 0.1, 0.7]},
            # {'fragment': 'Fragmento de Terror'
            #  , 'emocion1': 'Terror', 'velocidad': 7.15, 'rugosidad': 1.25, 'distorsion': 0.2, 'wave_direction': 1, 'color1': (0.4, 1.50, 0.50), 'deform_mode': 3, "hybrid_amnts": [0.5, 0.1, 0.9]},
            ##
            # ##
            # {'fragment': 'Fragmento de Distracción'
            #  , 'emocion1': 'Distracción', 'velocidad': 3.15, 'rugosidad': 5.25, 'distorsion': 0.002, 'wave_direction': 2, 'color1': (0.80, 1.30, 1.30), 'deform_mode': 3, "hybrid_amnts": [8.0, 0.0, 5.0]},
            # {'fragment': 'Fragmento de Sorpresa'
            #  , 'emocion1': 'Sorpresa', 'velocidad': 5.15, 'rugosidad': 5.25, 'distorsion': 0.008, 'wave_direction': 2, 'color1': (0.50, 1.30, 1.30), 'deform_mode': 3, "hybrid_amnts": [8.0, 0.0, 5.0]},
            # {'fragment': 'Fragmento de Asombro'
            #  , 'emocion1': 'Asombro', 'velocidad': 7.15, 'rugosidad': 5.25, 'distorsion': 0.01, 'wave_direction': 2, 'color1': (0.20, 1.50, 1.30), 'deform_mode': 3, "hybrid_amnts": [8.0, 0.0, 5.0]},
            # ##
            ##
            # {'fragment': 'Fragmento de Melancolía'
            #  , 'emocion1': 'Melancolía', 'velocidad': 0.25, 'rugosidad': 1.0, 'distorsion': 0.01, 'wave_direction': 1, 'color1': (0.80, 0.80, 1.50), 'deform_mode': 3, "hybrid_amnts": [0.0, 0.0, 5.0]},
            # {'fragment': 'Fragmento de Tristeza'
            #  , 'emocion1': 'Tristeza', 'velocidad': 0.5, 'rugosidad':  1.5, 'distorsion': 0.01, 'wave_direction': 1, 'color1': (0.45, 0.45, 1.50), 'deform_mode': 3, "hybrid_amnts": [0.0, 0.0, 5.0]},
            # {'fragment': 'Fragmento de Pena'
            #  , 'emocion1': 'Pena', 'velocidad': 1.1, 'rugosidad': 2.25, 'distorsion': 0.01, 'wave_direction': 1, 'color1': (0.10, 0.10, 1.50), 'deform_mode': 3, "hybrid_amnts": [0.0, 0.0, 5.0]},
            # ##
            # {'fragment': 'Fragmento de Aburrimiento'
            #  , 'emocion1': 'Aburrimiento', 'velocidad': 1.15, 'rugosidad': 10.25, 'distorsion': 0.1, 'wave_direction': 0, 'color1': (0.50, 0.40, 0.70), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.0, 0.0]},
            # {'fragment': 'Fragmento de Asco'
            #  , 'emocion1': 'Asco', 'velocidad': 2.15, 'rugosidad': 10.25, 'distorsion': 0.1, 'wave_direction': 0, 'color1': (0.80, 0.25, 1.30), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.0, 0.5]},
            # {'fragment': 'Fragmento de Odio'
            #  , 'emocion1': 'Odio', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.05, 'wave_direction': 0, 'color1': (1.0, 0.10, 1.50), 'deform_mode': 3, "hybrid_amnts": [1.1, 0.0, 1.0]},
            # ##
            # ##
            # {'fragment': 'Fragmento de Enfado'
            #  , 'emocion1': 'Enfado', 'velocidad': 5.15, 'rugosidad': 5.25, 'distorsion': 0.005, 'wave_direction': 1, 'color1': (1.0, 0.30, 0.30), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.1, 5.0]},
            # {'fragment': 'Fragmento de Ira'
            #  , 'emocion1': 'Ira', 'velocidad': 7.15, 'rugosidad': 5.25, 'distorsion': 0.01, 'wave_direction': 1, 'color1': (1.20, 0.30, 0.30), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.1, 5.0]},
            # {'fragment': 'Fragmento de Furia'
            #  , 'emocion1': 'Furia', 'velocidad': 10.15, 'rugosidad': 5.25, 'distorsion': 0.02, 'wave_direction': 1, 'color1': (1.50, 0.20, 0.20), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.1, 5.0]},
            # ##
            ##
            {'fragment': 'Fragmento de Interés'
             , 'emocion1': 'Interés', 'velocidad': 5.15, 'rugosidad': 10.25, 'distorsion': 0.1, 'wave_direction': 1, 'color1': (1.20, 0.70, 0.40), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.1, 0.0]},
            {'fragment': 'Fragmento de Anticipación'
             , 'emocion1': 'Anticipación', 'velocidad': 7.15, 'rugosidad': 10.25, 'distorsion': 0.1, 'wave_direction': 1, 'color1': (1.2, 0.70, 0.20), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.1, 0.0]},
            {'fragment': 'Fragmento de Vigilancia'
             , 'emocion1': 'Vigilancia', 'velocidad': 9.15, 'rugosidad': 10.25, 'distorsion': 0.1, 'wave_direction': 1, 'color1': (1.2, 0.70, 0.05), 'deform_mode': 3, "hybrid_amnts": [0.9, 0.1, 0.05]},
            ##
        ]
        start_glfw_simulation(example_emotions)
        break

if __name__ == "__main__":
    simulator = None
    main()