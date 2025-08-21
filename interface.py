import customtkinter as ctk
from tkinter import messagebox
from gemini_client import GeminiClient

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class InterfaceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.client = GeminiClient()

        self.title("Text Submission InterfaceApp")
        self.geometry("600x500")
        self.minsize(400, 300)

        # Hacer la interfaz adaptable
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)  # Textbox
        self.grid_rowconfigure(4, weight=2)  # Canvas imagen

        self.last_submitted_text = ""

        # Etiqueta
        self.label = ctk.CTkLabel(self, text="Introduce tu texto:", font=ctk.CTkFont(size=16))
        self.label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        # Textbox multilínea escalable con scroll
        self.text_input = ctk.CTkTextbox(self, wrap="word", font=ctk.CTkFont(size=14))
        self.text_input.grid(row=2, column=0, padx=20, pady=(0, 10), sticky="nsew")

        # Botón Submit
        self.submit_button = ctk.CTkButton(self, text="Submit", command=self.submit_text)
        self.submit_button.grid(row=3, column=0, padx=20, pady=(0, 10))

        # Canvas como placeholder de imagen 2D
        # self.image_canvas = ctk.CTkCanvas(self, bg="black", highlightthickness=0)
        # self.image_canvas.grid(row=4, column=0, padx=20, pady=(0, 20), sticky="nsew")

    def submit_text(self):
        user_text = self.text_input.get("1.0", "end").strip()
        if user_text:
            self.last_submitted_text = user_text
            print(f"[DEBUG] Texto enviado:\n{self.last_submitted_text}")
            #messagebox.showinfo("Texto recibido", f"Has introducido:\n\n{self.last_submitted_text}")
            response = self.client.consultar(user_text) # Hace la consulta a la Api y obtiene un string en formato JSON
            print(f"[DEBUG] Respuesta:\n{response}")
            self.text_input.delete("1.0", "end")
        else:
            messagebox.showwarning("Campo vacío", "Por favor, introduce algún texto.")


if __name__ == "__main__":
    app = InterfaceApp()
    app.mainloop()
