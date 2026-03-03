import os
import google.generativeai as genai
from dotenv import load_dotenv
from interface import App

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY")

if not API_KEY:
    print("Error: La variable de entorno GOOGLE_API_KEY no está configurada.")
    print("Por favor, establece la variable en tu archivo .env o en el sistema.")
    exit()

genai.configure(api_key=API_KEY)

model_name = "gemini-1.5-flash-latest"


print(f"\nIntentando usar el modelo: {model_name}")
model = genai.GenerativeModel(model_name=model_name)

consulta = "Quien descubrio america"
try:
    response = model.generate_content(consulta)
    print("\nRespuesta de Gemini:")
    print(response.text)
except Exception as e:
    print(f"Ocurrió un error durante la generación de contenido: {e}")