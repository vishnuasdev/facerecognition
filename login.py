from tkinter import *
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

from config import asset_path, connect_db
from main import Face_Recognition_System
from register import Register


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1550x800+0+0")
        self.background = ImageTk.PhotoImage(file=asset_path("bgImage.jpg"))
        Label(root, image=self.background).place(relwidth=1, relheight=1)

        frame = Frame(root, bg="black")
        frame.place(x=610, y=170, width=340, height=450)
        icon = Image.open(asset_path("logIcon.png")).resize((100, 100), Image.LANCZOS)
        self.icon = ImageTk.PhotoImage(icon)
        Label(frame, image=self.icon, bg="black").place(x=120, y=5, width=100, height=100)
        Label(frame, text="Get Started", font=("times new roman", 20, "bold"), fg="white", bg="black").place(x=95, y=100)
        Label(frame, text="Username", font=("times new roman", 15, "bold"), fg="white", bg="black").place(x=70, y=155)
        self.username = ttk.Entry(frame, font=("times new roman", 15, "bold"))
        self.username.place(x=40, y=180, width=270)
        Label(frame, text="Password", font=("times new roman", 15, "bold"), fg="white", bg="black").place(x=70, y=225)
        self.password = ttk.Entry(frame, show="*", font=("times new roman", 15, "bold"))
        self.password.place(x=40, y=250, width=270)
        Button(frame, text="Login", command=self.login, font=("times new roman", 15, "bold"), fg="white", bg="red").place(x=110, y=300, width=120, height=35)
        Button(frame, text="New User Register", command=self.register_window, fg="blue", bg="black").place(x=15, y=350, width=160)

    def register_window(self):
        Register(Toplevel(self.root))

    def login(self):
        username = self.username.get().strip()
        password = self.password.get()
        if not username or not password:
            messagebox.showerror("Error", "All fields are required", parent=self.root)
            return

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute(
                "SELECT 1 FROM register WHERE email=%s AND `pass`=%s",
                (username, password),
            )
            authenticated = cursor.fetchone() is not None
        except Exception as error:
            messagebox.showerror("Database error", str(error), parent=self.root)
            return
        finally:
            try:
                cursor.close()
                connection.close()
            except (NameError, AttributeError):
                pass

        if not authenticated:
            messagebox.showerror("Error", "Invalid username or password", parent=self.root)
            return
        window = Toplevel(self.root)
        Face_Recognition_System(window)


Login_window = LoginWindow


if __name__ == "__main__":
    root = Tk()
    LoginWindow(root)
    root.mainloop()
