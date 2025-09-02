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

if __name__ == "__main__":
    simulator = None
    main()