# -*- coding: utf-8 -*-
# sequential_simulator_with_api.py

import glfw
import moderngl
import numpy as np
import time
import random
import json
import os
from pyrr import Matrix44
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk

# Importa la clase del cliente de la API de Gemini.
# NOTA: Asegúrate de que tu archivo `gemini_client.py` esté en la misma carpeta.
# También necesitarás el archivo `.env` con tu clave de API.
try:
    import google.generativeai as genai
    from dotenv import load_dotenv
    _has_gemini_client = True
except ImportError:
    _has_gemini_client = False
    print("Warning: `google.generativeai` or `python-dotenv` are not installed. API functionality will not be available.")

prefix_prompt = """
Este servicio está pensado para ayudar a las personas a que no haya buena comprensión de las emociones.
Procedimiento:
Desglosa el texto por secciones según las emociones detectadas en cada sección.
Esta clasificación se rige por la rueda de las emociones.
Tipos (elegir entre los siguientes):
{Alegría, Admiración, Miedo, Sorpresa, Tristeza, Animadversión, Ira, Alerta}
Cada tipo de emoción tiene un subtipo según la intensidad, por ejemplo: Emoción tipo alegría de intensidad nivel 3 = Extasis
Las clases de emociones disponibles, según una escala de intensidad (de menos intenso a más intensidad), son:
Tipo "Alegría"-> Subtipos elegibles: {intensidad 1 = "Serenidad", intensidad 2 = "Alegría", intensidad 3 = "Éxtasis"}
Tipo "Aceptación"-> Subtipos elegibles: {intensidad 1 "Aceptación", intensidad 2 = "Confianza", intensidad 3 = "Admiración"}
Tipo "Miedo"-> Subtipos elegibles: {intensidad 1 = "Aprensión", intensidad 2 = "Miedo", intensidad 3 = "Terror"}
Tipo "Sorpresa"-> Subtipos elegibles: {intensidad 1 = "Distracción", intensidad 2 = "Sorpresa", intensidad 3 = "Asombro"}
Tipo "Tristeza"-> Subtipos elegibles: {intensidad 1 = "Melancolía", intensidad 2 = "Tristeza", intensidad 3 = "Pena"}
Tipo "Animadversión"-> Subtipos elegibles: {intensidad 1 = "Aburrimiento", intensidad 2 = "Asco", intensidad 3 = "Odio"}
Tipo "Ira"-> Subtipos elegibles: {intensidad 1 = "Enfado", intensidad 2 = "Ira", intensidad 3 = "Furia"}
Tipo "Alerta"-> Subtipos elegibles: {intensidad 1 = "Interés", intensidad 2 = "Anticipación", intensidad 3 = "Vigilancia"}

SIEMPRE que haya 2 tipos de emociones a la vez en un fragmento se debe añadir el matiz
Matices: Como las emociones son abstractas sería interesante añadir matices:
Tipo "Alegría" + tipo "Aceptación" (o al reveés) = matiz "Amor". 
Tipo "Aceptación" + tipo "Miedo" (o al reveés) = matiz "Sumisión".
Tipo "Miedo" + tipo "Sorpresa" (o al reveés) = matiz "Pavor".
Tipo "Sorpresa" + tipo "Tristeza" (o al reveés) = matiz "Decepción". 
Tipo "Tristeza" + "Animadversión" = matiz "Remordimiento". 
Tipo "Animadversión" + "Ira" = matiz "Desprecio". 
Tipo "Ira" + tipo "Alerta" = matiz "Agresividad". 
Tipo "Alerta" + tipo "Alegría" = matiz "Optimismo".

Estilo de output que necesito que generes:
Quiero que sigas un formato de respuesta muy estricto, siguiendo un formato similar al de un archivo JSON.
{fragmento:"Estallé de risa tras su chiste,", tipo1:"Alegría", intensidad1:"Éxtasis", tipo2:"Alerta", intensidad2:"Interés", matiz:"Optimismo"};
{fragmento:"pero eso no hizo que bajase la guardia.", tipo1:"Alerta", intensidad1:"Anticipación", tipo2:"Ninguno", intensidad2:"Ninguno", matiz:"Ninguno"};
Siempre deben aparecer los campos: {fragmento, tipo1, intensidad1, tipo2, intensidad2, matiz} como formato de respuesta.
Si un fragmento tiene más de 2 tipos de emociones dividelo para que cada fragmento solo tenga 2 emociones a la vez como máximo.
\n
"""

class GeminiClient:
    """
    Class that interacts with the Gemini API for emotion analysis.
    """
    def __init__(self, model_name: str = "gemini-1.5-flash-latest"):
        if not _has_gemini_client:
            raise ImportError("The necessary modules for GeminiClient are not installed.")
        
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            # In this execution environment, it may not be possible to read
            # environment variables. The key can be configured directly here.
            # api_key = "YOUR_API_KEY_HERE"
            # Or leave it empty so the Canvas environment provides it automatically.
            api_key = ""
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)

    def consultar(self, texto: str) -> str:
        try:
            texto_context = prefix_prompt + texto
            response = self.model.generate_content(texto_context)
            return response.text
        except Exception as e:
            return f"Error during content generation: {e}"

# Emotion parameter data, loaded directly as a string
# to avoid dependency on external files.
emotions_params_json_str = """
[
  {
    "Serenidad": 
      {
      "color": "#ADD8E6", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Alegría": 
      { "color": "#FFD700", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Éxtasis": 
      { "color": "#FF0392", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      },
    "Aceptación": 
      { "color": "#9ACD32", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Confianza": 
      { "color": "#4682B4", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Admiración": 
      { "color": "#f797f7", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      },
    "Aprensión": 
      { "color": "#abbd6b", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Miedo": 
      { "color": "#736785",
      "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Terror": 
      { "color": "#30223b", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      },
    "Distracción": 
      { "color": "#b1fce4", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Sorpresa": 
      { "color": "#FFFF00", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Asombro": 
      { "color": "#2ef2e8", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      },
    "Melancolía": 
      { "color": "#9ba4e8", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Tristeza": 
      { "color": "#435fba", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Pena": 
      { "color": "#202059", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      },
    "Aburrimiento": 
      { "color": "#9eaeb0", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Asco": 
      { "color": "#556B2F", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Odio": 
      { "color": "#57122e", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      },
    "Enfado": 
      { "color": "#DC143C", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Ira": 
      { "color": "#a60a0a", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Furia": 
      { "color": "#b00505", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      },
    "Interés": 
      { "color": "#20B2AA", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 0
      },
    "Anticipación": 
      { "color": "#FFA500", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 1
      },
    "Vigilancia": 
      { "color": "#ff8c00", "velocidad": 0.5, "rugosidad": 0.3, "distorsion": 0.2, "wave_direction": 2
      }
  }
]
"""

def hex_to_rgb(hex_color):
    """Converts a hex color string to an RGB tuple (0-1)."""
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) / 255.0 for i in (0, 2, 4))

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class InterfaceApp(ctk.CTk):
    """
    User interface class, now responsible for calling the API
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
            data = json.loads(emotions_params_json_str)
            self.emotions_data = data[0] # The JSON is an array with a single object
        except (json.JSONDecodeError, IndexError) as e:
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

    def _get_params_from_emotion(self, emotion_name):
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
                    
                    params2 = None
                    if intensity2 and intensity2 != "None":
                        params2 = self._get_params_from_emotion(intensity2)

                    final_params = {
                        'fragment': fragment_params.get('fragment'),
                        'velocidad': params1['velocidad'],
                        'rugosidad': params1['rugosidad'],
                        'distorsion': params1['distorsion'],
                        'wave_direction': params1['wave_direction'],
                        'color': hex_to_rgb(params1['color']),
                        'deform_mode_A': 0, # Placeholder
                        'deform_mode_B': 0, # Placeholder
                    }
                    if matiz and matiz != "None":
                        final_params['deform_mode_A'] = 3
                        final_params['deform_mode_B'] = 3
                        final_params['hybrid_amnts_A'] = [
                            random.uniform(0.1, 0.5),
                            random.uniform(0.1, 0.5),
                            random.uniform(0.1, 0.5)
                        ]
                        final_params['hybrid_amnts_B'] = [
                            random.uniform(0.1, 0.5),
                            random.uniform(0.1, 0.5),
                            random.uniform(0.1, 0.5)
                        ]
                    
                    self.simulation_parameters_list.append(final_params)

                self.destroy()

            except (ValueError, TypeError, json.JSONDecodeError) as e:
                messagebox.showerror("Data Error", f"Could not process data from the API.\nDetails: {e}")
        else:
            if not user_text:
                messagebox.showwarning("Empty Field", "Please enter some text.")
            elif not self.client:
                messagebox.showwarning("Client not available", "Could not initialize the API client.")

class SphereSimulator:
    """
    Reusable class for simulating a sphere with deformations
    and post-processing using ModernGL and GLFW.
    """
    def __init__(self, window, width: int = 800, height: int = 600, 
                 emotions_list: list = None):
        """
        Initializes the ModernGL context, shaders, and sphere geometry.
        """
        self.window = window
        self.width = width
        self.height = height
        self.ctx = None
        self.prog_sphere = None
        self.prog_post = None
        self.vao_sphere = None
        self.vao_post = None
        self.fbo = None
        self.projection = None
        self.view = None
        self.start_time = time.time()
        
        # State for emotions transition
        self.emotions_list = emotions_list if emotions_list else []
        self.current_index = 0
        self.is_transitioning = False
        self.transition_start_time = 0.0
        self.transition_duration = 2.0
        
        # Current parameters (A) and next parameters (B) for transition
        self.params_A = {}
        self.params_B = {}
        
        if self.emotions_list:
            # Set the initial state
            self.params_A = self.emotions_list[0].copy()
            self.params_B = self.emotions_list[0].copy() # Initially, A and B are the same
        
        # Initialize rendering parameters
        self.blur_strength = 5.0
        self.light_color1 = (1.0, 1.0, 1.0)
        self.light_color2 = (0.5, 0.5, 0.5)
        
        self._init_moderngl()
        self._load_shaders()
        self._load_mesh()
        self._setup_framebuffer()
        self._setup_matrices()
        
    def _init_moderngl(self):
        """Creates the ModernGL context and sets up the initial state."""
        self.ctx = moderngl.create_context()
        self.ctx.enable(moderngl.DEPTH_TEST)

    def _load_shaders(self):
        """Loads and compiles the shaders."""
        try:
            with open("shaders/sphere_vert.glsl", 'r') as f:
                vert_shader = f.read()
            with open("shaders/sphere_frag.glsl", 'r') as f:
                frag_shader = f.read()
            self.prog_sphere = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)

            with open("shaders/post_vert.glsl", 'r') as f:
                post_vert_shader = f.read()
            with open("shaders/post_frag.glsl", 'r') as f:
                post_frag_shader = f.read()
            self.prog_post = self.ctx.program(vertex_shader=post_vert_shader, fragment_shader=post_frag_shader)
        except FileNotFoundError as e:
            print(f"Error: Shader file not found. Make sure the .glsl files are in the correct path. Details: {e}")
            raise

    def _load_mesh(self):
        """Loads the sphere mesh from .npy files and creates VAOs."""
        try:
            vertices = np.load("vertices_high_res.npy")
            indices = np.load("indices_high_res.npy")

            vbo = self.ctx.buffer(vertices.astype('f4').tobytes())
            ibo = self.ctx.buffer(indices.astype('i4').tobytes())
            self.vao_sphere = self.ctx.simple_vertex_array(self.prog_sphere, vbo, 'in_position', index_buffer=ibo)
        except FileNotFoundError as e:
            print(f"Error: Mesh file not found. Make sure the .npy files are in the correct path. Details: {e}")
            raise
        
        quad_vertices = np.array([
            -1, -1, 0, 0,
             1, -1, 1, 0,
            -1,  1, 0, 1,
             1,  1, 1, 1,
        ], dtype='f4')
        quad_vbo = self.ctx.buffer(quad_vertices.tobytes())
        self.vao_post = self.ctx.simple_vertex_array(self.prog_post, quad_vbo, 'in_pos', 'in_uv')

    def _setup_framebuffer(self):
        self.fbo = self.ctx.framebuffer(
            color_attachments=[self.ctx.texture((self.width, self.height), 4)],
            depth_attachment=self.ctx.depth_renderbuffer((self.width, self.height))
        )

    def _setup_matrices(self):
        self.projection = Matrix44.perspective_projection(45.0, self.width / self.height, 0.1, 100.0)
        self.view = Matrix44.look_at((0.0, 0.0, 3.0), (0.0, 0.0, 0.0), (0.0, 1.0, 0.0))

    def start_next_transition(self):
        """Starts the transition to the next set of parameters in the list."""
        if self.current_index < len(self.emotions_list) - 1:
            self.current_index += 1
            self.is_transitioning = True
            self.transition_start_time = time.time()
            self.params_A = self.emotions_list[self.current_index - 1].copy()
            self.params_B = self.emotions_list[self.current_index].copy()
            print(f"[INFO] Transitioning to fragment {self.current_index + 1}: {self.params_B.get('fragment', 'N/A')}")
        else:
            print("[INFO] Reached the end of the emotion fragments list.")

    def _update_transition(self, now):
        """Calculates the blend factor for a smooth transition."""
        if self.is_transitioning:
            elapsed_time = now - self.transition_start_time
            blend_factor = min(elapsed_time / self.transition_duration, 1.0)
            if blend_factor >= 1.0:
                self.is_transitioning = False
                self.params_A = self.params_B.copy()
            return blend_factor
        return 0.0

    def render(self, now):
        """Renders the sphere with the current or transitioning parameters."""
        blend_factor = self._update_transition(time.time())
        self.fbo.use()
        self.ctx.clear(0.05, 0.05, 0.05)
        model = Matrix44.identity()

        # Interpolate all parameters
        def lerp(a, b, t):
            return a + (b - a) * t
        
        def lerp_vec3(a, b, t):
            return tuple(lerp(a[i], b[i], t) for i in range(3))
        
        def get_param(param_name, default):
            val_A = self.params_A.get(param_name, default)
            val_B = self.params_B.get(param_name, default)
            return lerp(val_A, val_B, blend_factor)
        
        # Get parameters for the transition
        velocidad_current = get_param('velocidad', 5.0)
        rugosidad_current = get_param('rugosidad', 10.0)
        distorsion_current = get_param('distorsion', 0.1)
        wave_direction_current = get_param('wave_direction', 0)
        base_color_current = lerp_vec3(self.params_A.get('color', (1.0, 0.5, 0.2)), 
                                       self.params_B.get('color', (1.0, 0.5, 0.2)), blend_factor)

        # Update uniforms
        self.prog_sphere['time'].value = now
        self.prog_sphere['velocidad'].value = velocidad_current
        self.prog_sphere['rugosidad'].value = rugosidad_current
        self.prog_sphere['distorsion'].value = distorsion_current
        self.prog_sphere['wave_direction'].value = wave_direction_current
        self.prog_sphere['model'].write(model.astype('f4').tobytes())
        self.prog_sphere['view'].write(self.view.astype('f4').tobytes())
        self.prog_sphere['projection'].write(self.projection.astype('f4').tobytes())
        self.prog_sphere['base_color'].value = base_color_current
        self.prog_sphere['light_color1'].value = self.light_color1
        self.prog_sphere['light_color2'].value = self.light_color2
        
        self.prog_sphere['deform_mode_A'].value = self.params_A.get('deform_mode_A', 0)
        self.prog_sphere['deform_mode_B'].value = self.params_B.get('deform_mode_B', 0)
        self.prog_sphere['blend_factor'].value = blend_factor
        
        hybrid_amnts_A = self.params_A.get('hybrid_amnts_A', [0.0, 0.0, 0.0])
        hybrid_amnts_B = self.params_B.get('hybrid_amnts_B', [0.0, 0.0, 0.0])
        self.prog_sphere['effect1_amnt_A'].value = hybrid_amnts_A[0]
        self.prog_sphere['effect2_amnt_A'].value = hybrid_amnts_A[1]
        self.prog_sphere['effect3_amnt_A'].value = hybrid_amnts_A[2]
        self.prog_sphere['effect1_amnt_B'].value = hybrid_amnts_B[0]
        self.prog_sphere['effect2_amnt_B'].value = hybrid_amnts_B[1]
        self.prog_sphere['effect3_amnt_B'].value = hybrid_amnts_B[2]

        self.vao_sphere.render()

        self.ctx.screen.use()
        self.ctx.clear()
        self.fbo.color_attachments[0].use(location=0)
        self.prog_post['texture0'].value = 0
        self.prog_post['resolution'].value = (float(self.width), float(self.height))
        self.prog_post['blur_strength'].value = self.blur_strength
        self.vao_post.render(moderngl.TRIANGLE_STRIP)

    def terminate(self):
        """Releases all ModernGL resources."""
        self.ctx.release()
        self.fbo.release()
        self.prog_sphere.release()
        self.prog_post.release()
        self.vao_sphere.release()
        self.vao_post.release()

def key_callback(window, key, scancode, action, mods):
    """
    GLFW keyboard callback to handle user input.
    """
    if key == glfw.KEY_ENTER and action == glfw.PRESS:
        global simulator
        if simulator:
            simulator.start_next_transition()

def start_glfw_simulation(emotions_list):
    """
    Function that initializes and runs the sphere simulation loop.
    """
    if not glfw.init():
        return
    
    width, height = 1280, 720
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, glfw.TRUE)

    window = glfw.create_window(width, height, "Deformable Sphere Simulator", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)

    global simulator
    simulator = SphereSimulator(window, width, height, emotions_list=emotions_list)
    
    while not glfw.window_should_close(window):
        now = time.time()
        simulator.render(now)
        glfw.swap_buffers(window)
        glfw.poll_events()

    simulator.terminate()
    glfw.terminate()

def main():
    """
    Main function that orchestrates the program's execution.
    """
    app = InterfaceApp()
    app.mainloop()

    if app.simulation_parameters_list:
        start_glfw_simulation(app.simulation_parameters_list)

if __name__ == "__main__":
    simulator = None
    main()
