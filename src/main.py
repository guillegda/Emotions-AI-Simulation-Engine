from src.interface_app import InterfaceApp
from src.sphere_simulator import start_glfw_simulation
def main():
    """
    Main function that orchestrates the program's execution.
    """
    while True:
        app = InterfaceApp()
        app.mainloop()

        if app.simulation_parameters_list:
            start_glfw_simulation(app.simulation_parameters_list, record_simulation=app.get_bool_record())
        else:
            print("No simulation parameters available. Exiting.")
            break

if __name__ == "__main__":
    simulator = None
    main()