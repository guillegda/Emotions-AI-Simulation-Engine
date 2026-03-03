# 🌐 Emotional Sphere Visualization Engine

A high-performance Python application that transforms text into real-time 3D emotional simulations. By leveraging the **Google Gemini API** for semantic analysis and **ModernGL** for GPU-accelerated rendering, the system generates a morphing sphere that represents human feelings through complex vertex displacement and lighting.

## 🚀 Overview

This project bridges the gap between Natural Language Processing (NLP) and Computer Graphics. It breaks down user input into emotional fragments based on **Plutchik's Wheel of Emotions**, mapping them to physical parameters like vibration, roughness, and color in a 3D environment.

## 🛠 Tech Stack

| Category | Tools |
| :--- | :--- |
| **Language** | Python 3.13.5, GLSL (OpenGL Shading Language) |
| **Graphics** | ModernGL, GLFW, PyRR (Matrices), NumPy |
| **AI / NLP** | Google Generative AI (Gemini Pro), python-dotenv |
| **UI / UX** | CustomTkinter |
| **Vision/Output** | OpenCV (MP4 Recording support) |

## 🏗 Architecture

The application follows a **Two-Stage Interaction Pipeline** to ensure stability between the event-driven UI and the high-frequency rendering loop:

1.  **Input Stage (UI):** Built with `CustomTkinter`, users input text and configure recording options.
2.  **Analysis Stage (Client):** The text is sent to the Gemini API with a strict system prompt. The AI returns a structured JSON-like response identifying primary/secondary emotions and their intensities.
3.  **Simulation Stage (GPU):** The system transitions to a `GLFW` window where `ModernGL` handles the rendering.
4.  **Interpolation Engine:** Emotions are not static; the system uses weighted linear interpolation to create smooth transitions between complex emotional states (e.g., blending "Joy" with "Anticipation").


## 🎨 Emotional Mapping Logic

The sphere's behavior is dictated by three main physical variables controlled via Vertex Shaders:

* **Speed:** Increases the frequency of the deformation wave (higher arousal).
* **Roughness:** Adds complexity and "peaks" to the surface (Perlin Noise frequency).
* **Distortion:** Defines the amplitude/size of the displacement.

### Emotional Color Palette & Dynamics
The system follows a logic where intensity equals saturation. 
* **Joy (Yellow):** Calm vertical movements.
* **Rage (Red):** High-frequency "spike" explosions via spherical Perlin noise.
* **Sadness (Blue):** Slow, descending wave patterns mimicking tears.
* **Fear (Green):** Shaking, constricted "clamped" movements.


## ⚡ Key Features

* **Complex Shaders:** Uses **Displacement Mapping** and **Phong Reflection Models** for realistic light interaction.
* **Hybrid Emotions:** Detects "Nuances" (Matices). For example, Joy + Acceptance = **Love**; Anger + Alertness = **Aggressiveness**.
* **Post-Processing:** Real-time Gaussian blur filters applied via Framebuffer Objects (FBO).
* **Recording:** Integrated OpenCV functionality to export the simulation as an MP4 file.

## 🔧 Installation & Setup

1. **Clone the repo:**
   ```bash
   git clone [https://github.com/youruser/emotional-sphere.git](https://github.com/youruser/emotional-sphere.git)
   cd emotional-sphere


2. **Install dependencies:**
   ```bash
   pip install moderngl glfw numpy pyrr opencv-python customtkinter google-generativeai python-dotenv

3. **Configure API Key:**
Create a .env file in the root directory:
   ```bash
   GOOGLE_API_KEY=your_gemini_api_key_here

4. **Run the application**
Create a .env file in the root directory:
   ```bash
   python main.py

## 🧠 System Prompting

The project uses a highly refined "Strict Output" prompt to ensure the LLM acts as a deterministic parser, returning specific intensity levels (1-3) and preventing technical conflicts during the JSON formatting phase.

Developed as an exploration of emotional representation through code.
