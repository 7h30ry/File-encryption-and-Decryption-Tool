from cryptography.fernet import Fernet
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter.font import Font

class EncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryption Tool")

        self.root.geometry("400x300")  # Set the window size

        self.background_color1 = "#FAD02E"  # Gradient start color
        self.background_color2 = "#E45E5E"  # Gradient end color
        self.button_color = "#5D9B9B"  # Button color
        self.text_color = "#FFFFFF"  # Text color

        self.root.configure(bg=self.background_color1)
        self.create_gradient_background()

        self.header_font = Font(family="Helvetica", size=16, weight="bold")
        self.button_font = Font(family="Helvetica", size=12)

        self.header_label = tk.Label(root, text="File Encryption Tool", font=self.header_font, fg=self.text_color, bg=self.background_color1)
        self.header_label.pack(pady=20)

        self.encrypt_button = tk.Button(root, text="Encrypt File", font=self.button_font, command=self.encrypt_file, bg=self.button_color, fg=self.text_color)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(root, text="Decrypt File", font=self.button_font, command=self.decrypt_file, bg=self.button_color, fg=self.text_color)
        self.decrypt_button.pack(pady=10)

        self.key = None

    def generate_key(self, password):
        self.key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(self.key)

    def load_key(self):
        self.key = open("key.key", "rb").read()

    def encrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")
        password = simpledialog.askstring("Password", "Enter a password:")
        if file_path and password:
            self.generate_key(password)
            self.load_key()

            cipher = Fernet(self.key)
            with open(file_path, "rb") as file:
                file_data = file.read()
            
            encrypted_data = cipher.encrypt(file_data)

            encrypted_filename = "encrypted_" + file_path.split("/")[-1]
            with open(encrypted_filename, "wb") as encrypted_file:
                encrypted_file.write(encrypted_data)

            messagebox.showinfo("Encryption", f"{file_path} has been encrypted.\nEncrypted file: {encrypted_filename}")

    def decrypt_file(self):
        encrypted_file_path = filedialog.askopenfilename(title="Select an encrypted file to decrypt")
        password = simpledialog.askstring("Password", "Enter the password:")
        if encrypted_file_path and password:
            self.load_key()

            cipher = Fernet(self.key)
            with open(encrypted_file_path, "rb") as encrypted_file:
                encrypted_data = encrypted_file.read()
            
            decrypted_data = cipher.decrypt(encrypted_data)

            decrypted_filename = "decrypted_" + encrypted_file_path.split("/")[-1]
            with open(decrypted_filename, "wb") as decrypted_file:
                decrypted_file.write(decrypted_data)

            messagebox.showinfo("Decryption", f"{encrypted_file_path} has been decrypted.\nDecrypted file: {decrypted_filename}")

    def create_gradient_background(self):
        canvas = tk.Canvas(self.root, width=400, height=300, highlightthickness=0)
        canvas.pack()
        
        gradient = tk.PhotoImage(width=1, height=1)
        for i in range(400):
            r = int(255 - (255 * i / 400))
            g = int(255 - (255 * i / 400))
            b = int(255 - (255 * i / 400))
            color = f"#{r:02x}{g:02x}{b:02x}"
            gradient.put(color, (i, 0))
        
        canvas.create_image(0, 0, anchor="nw", image=gradient, tags="gradient")

if __name__ == "__main__":
    root = tk.Tk()
    app = EncryptionApp(root)
    root.mainloop()
