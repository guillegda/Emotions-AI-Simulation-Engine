from interface_app import InterfaceApp
from sphere_simulator import start_glfw_simulation
def main():
    """
    Main function that orchestrates the program's execution.
    """
    while True:
        app = InterfaceApp()
        app.mainloop()

        if app.simulation_parameters_list:
            start_glfw_simulation(app.simulation_parameters_list)
        else:
            print("No simulation parameters available. Exiting.")
            break

        # example_emotions = [
        #     {'name': 'Calma', 'color': (0.2, 0.5, 1.0), 'velocidad': 1.0, 'rugosidad': 5.0, 'distorsion': 0.05, 'wave_direction': 0, 'deform_mode': 0},
        #     {'name': 'Alegría', 'color': (1.0, 0.8, 0.0), 'velocidad': 8.0, 'rugosidad': 15.0, 'distorsion': 0.2, 'wave_direction': 1, 'deform_mode': 1},
        #     {'name': 'Enojo', 'color': (1.0, 0.1, 0.1), 'velocidad': 12.0, 'rugosidad': 25.0, 'distorsion': 0.5, 'wave_direction': 2, 'deform_mode': 2},
        #     {'name': 'Confusión', 'color': (0.5, 0.5, 0.5), 'velocidad': 5.0, 'rugosidad': 10.0, 'distorsion': 0.1, 'wave_direction': 0, 'deform_mode': 3, 'hybrid_amnts': [0.5, 0.5, 0.0]},
        # ]
        # start_glfw_simulation(example_emotions)
        # break

if __name__ == "__main__":
    simulator = None
    main()