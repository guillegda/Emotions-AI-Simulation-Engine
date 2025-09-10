from gemini_client import GeminiClient
import customtkinter as ctk
from tkinter import messagebox
import json

# Emotion parameter data, loaded directly as a string
# to avoid dependency on external files.
emotions_params_json_str = """
[
  { "Serenidad": { "color": [1.2, 0.90, 0.30], "velocidad": 5.15, "rugosidad": 3.25, "distorsion": 0.1, "wave_direction": 2 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.9, 0.0] } },
  { "Alegría": { "color": [1.30, 1.10, 0.30], "velocidad": 10.15, "rugosidad": 7.25, "distorsion": 0.1, "wave_direction": 2 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.9, 0.0] } },
  { "Éxtasis": { "color": [1.59, 1.25, 0.20], "velocidad": 12.15, "rugosidad": 10.25, "distorsion": 0.1, "wave_direction": 2 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.9, 0.05] } },
  
  { "Aceptación": { "color": [1.0, 1.30, 0.80], "velocidad": 2.15, "rugosidad": 5.25, "distorsion": 0.1, "wave_direction": 0 , "deform_mode": 3, "hybrid_amnts": [0.1, 0.9, 0.0] } },
  { "Confianza": { "color": [1.15, 1.50, 0.70], "velocidad": 3.15, "rugosidad": 8.25, "distorsion": 0.15, "wave_direction": 0 , "deform_mode": 3, "hybrid_amnts": [0.3, 0.9, 0.0] } },
  { "Admiración": { "color": [1.2, 1.60, 0.60], "velocidad": 4.15, "rugosidad": 8.25, "distorsion": 0.2, "wave_direction": 0 , "deform_mode": 3, "hybrid_amnts": [0.5, 0.9, 0.0] } },
  
  { "Aprensión": { "color": [0.4, 1.20, 0.70], "velocidad": 3.15, "rugosidad": 1.25, "distorsion": 0.1, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.5, 0.1, 0.5] } },
  { "Miedo": { "color": [0.4, 1.30, 0.60], "velocidad": 5.15, "rugosidad": 1.25, "distorsion": 0.2, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.5, 0.1, 0.7] } },
  { "Terror": { "color": [0.4, 1.50, 0.50], "velocidad": 7.15, "rugosidad": 1.25, "distorsion": 0.2, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.5, 0.1, 0.9] } },
  
  { "Distracción": { "color": [0.80, 1.30, 1.30], "velocidad": 3.15, "rugosidad": 5.25, "distorsion": 0.002, "wave_direction": 2 , "deform_mode": 3, "hybrid_amnts": [8.0, 0.0, 5.0] } },
  { "Sorpresa": { "color": [0.50, 1.30, 1.30], "velocidad": 5.15, "rugosidad": 5.25, "distorsion": 0.008, "wave_direction": 2 , "deform_mode": 3, "hybrid_amnts": [8.0, 0.0, 5.0] } },
  { "Asombro": { "color": [0.20, 1.50, 1.30], "velocidad": 7.15, "rugosidad": 5.25, "distorsion": 0.01, "wave_direction": 2 , "deform_mode": 3, "hybrid_amnts": [8.0, 0.0, 5.0] } },
  
  { "Melancolía": { "color": [0.80, 0.80, 1.50], "velocidad": 0.25, "rugosidad": 1.0, "distorsion": 0.01, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.0, 0.0, 5.0] } },
  { "Tristeza": { "color": [0.45, 0.45, 1.50], "velocidad": 0.5, "rugosidad":  1.5, "distorsion": 0.01, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.0, 0.0, 5.0] } },
  { "Pena": { "color": [0.10, 0.10, 1.50], "velocidad": 1.1, "rugosidad": 2.25, "distorsion": 0.01, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.0, 0.0, 5.0] } },
  
  { "Aburrimiento": { "color": [0.50, 0.40, 0.70], "velocidad": 1.15, "rugosidad": 10.25, "distorsion": 0.1, "wave_direction": 0 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.0, 0.0] } },
  { "Asco": { "color": [0.80, 0.25, 1.30], "velocidad": 2.15, "rugosidad": 10.25, "distorsion": 0.1, "wave_direction": 0 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.0, 0.5] } },
  { "Odio": { "color": [1.0, 0.10, 1.50], "velocidad": 5.15, "rugosidad": 10.25, "distorsion": 0.05, "wave_direction": 0 , "deform_mode": 3, "hybrid_amnts": [1.1, 0.0, 1.0] } },
  
  { "Enfado": { "color": [1.0, 0.30, 0.30], "velocidad": 5.15, "rugosidad": 5.25, "distorsion": 0.005, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.1, 5.0] } },
  { "Ira": { "color": [1.20, 0.30, 0.30], "velocidad": 7.15, "rugosidad": 5.25, "distorsion": 0.01, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.1, 5.0] } },
  { "Furia": { "color": [1.50, 0.20, 0.20], "velocidad": 10.15, "rugosidad": 5.25, "distorsion": 0.02, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.1, 5.0] } },
  
  { "Interés": { "color": [1.20, 0.70, 0.40], "velocidad": 5.15, "rugosidad": 10.25, "distorsion": 0.1, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.1, 0.0] } },
  { "Anticipación": { "color": [1.2, 0.70, 0.20], "velocidad": 7.15, "rugosidad": 10.25, "distorsion": 0.1, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.1, 0.0] } },
  { "Vigilancia": { "color": [1.2, 0.70, 0.05], "velocidad": 9.15, "rugosidad": 10.25, "distorsion": 0.1, "wave_direction": 1 , "deform_mode": 3, "hybrid_amnts": [0.9, 0.1, 0.05] } }
]
"""
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class InterfaceApp(ctk.CTk):
    """
    User interface class, responsible for calling the API
    and initiating the simulation with the obtained parameters.
    """
    def __init__(self):
        super().__init__()
        self.simulation_parameters_list = None
        
        try:
            self.client = GeminiClient()
        except ImportError as e:
            messagebox.showerror("Error", f"Missing module: {e}\nPlease install `google.generativeai` and `python-dotenv`.")
            self.client = None

        self.emotions_data = None
        try:
            # Corrected line: Use the function to transform the list into a dictionary
            self.emotions_data = load_emotions_from_json_string(emotions_params_json_str)
            if not self.emotions_data:
                raise ValueError("Emotion data is empty or malformed.")
        except (json.JSONDecodeError, IndexError, ValueError) as e:
            messagebox.showerror("Error", f"Error loading emotion data.\nDetails: {e}")
            self.destroy()

        self.title("Configuration Interface")
        self.geometry("600x500")
        self.minsize(400, 300)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.last_submitted_text = ""

        self.label = ctk.CTkLabel(self, text="Enter your text:", font=ctk.CTkFont(size=16))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.text_input = ctk.CTkTextbox(self, wrap="word", font=ctk.CTkFont(size=14))
        self.text_input.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")

        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_text)
        self.submit_button.grid(row=2, column=0, padx=20, pady=(0, 10))

    def _get_params_from_emotion(self, emotion_name: str) -> dict:
        """Looks for and returns the parameters of an emotion in the data dictionary."""
        return self.emotions_data.get(emotion_name, None)

    def submit_text(self):
        """
        Handles user input, calls the API, processes the response
        and calculates the parameters for the simulation.
        """
        user_text = self.text_input.get("1.0", "end").strip()
        if user_text and self.client and self.emotions_data:
            try:
                self.text_input.delete("1.0", "end")
                self.text_input.insert("end", "Consulting API...")
                self.text_input.update()
                
                json_response = self.client.consultar(user_text)
                print(f"[DEBUG] Raw JSON response from API:\n{json_response}")

                start_index = json_response.find('{')
                end_index = json_response.rfind('}')
                
                clean_json_string = "[" + json_response[start_index : end_index + 1].strip() + "]"
                clean_json_string = clean_json_string.replace('}{', '},{')
                clean_json_string = clean_json_string.replace(';', ',')

                print(f"[DEBUG] Clean JSON response:\n{clean_json_string}")
                
                json_response_list = json.loads(clean_json_string)

                if not json_response_list:
                    raise ValueError("Empty or invalid API response.")
                
                self.simulation_parameters_list = []
                for fragment_params in json_response_list:
                    intensity1 = fragment_params.get('intensidad1')
                    intensity2 = fragment_params.get('intensidad2')
                    matiz = fragment_params.get('matiz')

                    params1 = self._get_params_from_emotion(intensity1)
                    if not params1:
                        raise ValueError(f"Parameters for emotion '{intensity1}' not found.")
                    print(f"[DEBUG] Params1 for '{intensity1}': {params1}")
                    
                    params2 = None
                    if intensity2 and intensity2 != "None":
                        params2 = self._get_params_from_emotion(intensity2)
                    print(f"[DEBUG] Params2 for '{intensity2}': {params2}")

                    #TO DO: gestionar como se combinen las emociones y el matiz

                    final_params = {
                        'fragment': fragment_params.get('fragmento'),
                        'emocion1': intensity1,
                        'emocion2': intensity2 if intensity2 else "None",
                        'matiz': matiz if matiz else "None",
                        'velocidad': params1['velocidad'],
                        'rugosidad': params1['rugosidad'],
                        'distorsion': params1['distorsion'],
                        'wave_direction': params1['wave_direction'],
                        'color1': tuple(params1['color']),
                        'color2': tuple(params1['color']),
                        'deform_mode1': params1['deform_mode'],
                        'deform_mode2': params1['deform_mode']
                    }
                    
                    # Handling of combined emotions and matiz (tint)
                    if params2:
                        # Interpolate between params1 and params2
                        for key in ['velocidad', 'rugosidad', 'distorsion']:
                            final_params[key] = (params1[key] * 0.8) + (params2[key] * 0.2)
                        #No se si quiero hacer una media de color
                        # final_params['color'] = (
                        #     (tuple(params1['color'])[0] + tuple(params2['color'])[0]) / 2.0,
                        #     (tuple(params1['color'])[1] + tuple(params2['color'])[1]) / 2.0,
                        #     (tuple(params1['color'])[2] + tuple(params2['color'])[2]) / 2.0
                        # )
                        final_params['color2'] = tuple(params2['color'])
                        final_params['deform_mode2'] = params2['deform_mode']

                    
                    if matiz and matiz != "None":
                        matiz_params = self._get_params_from_emotion(matiz)
                        if matiz_params:
                            final_params['deform_mode'] = matiz_params.get('deform_mode', 0)
                            final_params['hybrid_amnts'] = matiz_params.get('hybrid_amnts', [0.0, 0.0, 0.0])
                    
                    self.simulation_parameters_list.append(final_params)
                    print(f"[DEBUG] Final params for fragment {final_params}")

                self.destroy()

            except (ValueError, TypeError, json.JSONDecodeError) as e:
                messagebox.showerror("Data Error", f"Could not process data from the API.\nDetails: {e}")
        else:
            if not user_text:
                messagebox.showwarning("Empty Field", "Please enter some text.")
            elif not self.client:
                messagebox.showwarning("Client not available", "Could not initialize the API client.")

def load_emotions_from_json_string(json_str: str) -> dict:
    """
    Carga y transforma los datos de emociones desde una cadena JSON a un
    diccionario de emociones.
    """
    try:
        data = json.loads(json_str)
        emotions_dict = {}
        # Iteramos a través de la lista de diccionarios
        for item in data:
            # Cada item es un diccionario con una sola clave (la emoción)
            for emotion, params in item.items():
                emotions_dict[emotion] = params
        return emotions_dict
    except json.JSONDecodeError as e:
        print(f"Error al decodificar el JSON: {e}")
        return {}

# Esto lo usaba antes porque tenia los colores como cadenas de texto en formato hex    
# def hex_to_rgb(hex_color):
#     """Converts a hex color string to an RGB tuple (0-1)."""
#     hex_color = hex_color.lstrip('#')
#     return tuple(round(int(hex_color[i:i+2], 16) / 255.0, 2) for i in (0, 2, 4))

