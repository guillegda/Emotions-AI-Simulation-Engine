# emotion_detection_AI
Given information through live chatting with AI agent, particle effects are simulated after analyzing the emotion of that conversation using an API REST to interact with the AI agent.

Para activar el entorno virtual: .\venv\Scripts\Activate.ps1

Tutorial útil de python para la api de gemini: https://www.youtube.com/watch?v=LQrssQfFbUI


¿Por qué los archivos .npy?
El formato .npy es propio de NumPy y tiene ventajas claras cuando estás trabajando con datos numéricos en Python:

Ventajas:
Velocidad: leer y escribir .npy es muy rápido.

Precisión total: mantiene el tipo exacto (float32, int32, etc.) sin pérdidas.

Simplicidad en Python:

np.save() y np.load() son funciones directas y eficientes.

No necesitas hacer parsing manual como con .txt o .obj.

Compacto: más pequeño que CSV o texto plano para arrays grandes.

Seguro para estructuras grandes como mallas 3D.


Rugosidad: cuantas arrugas o deformaciones le salen
Distorsion: si esas arrugas son muy pronunciadas, si se contraen y expanden mucho