import os
import google.generativeai as genai
from dotenv import load_dotenv

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
    def __init__(self, model_name: str = "gemini-1.5-flash-latest"):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise EnvironmentError(
                "Error: La variable de entorno GOOGLE_API_KEY no está configurada.\n"
                "Por favor, establece la variable en tu archivo .env o en el sistema."
            )

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name=model_name)

    def consultar(self, texto: str) -> str:
        try:
            texto_context = prefix_prompt + texto
            response = self.model.generate_content(texto_context)
            return response.text
        except Exception as e:
            return f"Error durante la generación de contenido: {e}"

if __name__ == "__main__":
    cliente = GeminiClient()
    resultado = cliente.consultar("¿Quién descubrió América?")
    print("\nRespuesta de Gemini:")
    print(resultado)
