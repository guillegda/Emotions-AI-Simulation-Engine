import os
import google.generativeai as genai
from dotenv import load_dotenv
from interface import App

#Nota para mí: si quieres activar el entorno virtual, pon esto en la terminal: .\venv\Scripts\Activate.ps1
load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
    print("Por favor, establece la variable en tu archivo .env o en el sistema.")
    exit()

genai.configure(api_key=API_KEY)

# --- MODELO RECOMENDADO PARA TRABAJO UNIVERSITARIO ---
# Opción 1: Gemini 1.5 Flash (más común y robusto para free tier)
model_name = "gemini-1.5-flash-latest"

# Opción 2: Gemini 2.5 Flash Lite (más reciente y posiblemente más eficiente)
# model_name = "gemini-2.5-flash-lite" # O una de las versiones con "preview" si quieres lo ultimísimo.
# Por ejemplo, según tu lista: "models/gemini-2.5-flash-lite-preview-06-17" o "models/gemini-2.5-flash-lite"
# Te recomiendo empezar por "gemini-1.5-flash-latest" por su estabilidad en el free tier.


print(f"\nIntentando usar el modelo: {model_name}")
model = genai.GenerativeModel(model_name=model_name)

consulta = "Quien descubrio america"
try:
    response = model.generate_content(consulta)
    print("\nRespuesta de Gemini:")
    print(response.text)
except Exception as e:
    print(f"Ocurrió un error durante la generación de contenido: {e}")