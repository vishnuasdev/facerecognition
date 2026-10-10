from tkinter import *
from tkinter import messagebox, ttk

from PIL import Image, ImageTk

from config import asset_path, connect_db


class Register:
    def __init__(self, root):
        self.root = root
        self.root.title("Register")
        self.root.geometry("1600x900+0+0")
        self.background = ImageTk.PhotoImage(file=asset_path("bgImage.jpg"))
        Label(root, image=self.background).place(relwidth=1, relheight=1)

        frame = Frame(root, bg="white")
        frame.place(x=370, y=100, width=800, height=550)
        Label(frame, text="REGISTER HERE", font=("times new roman", 20, "bold"), fg="green", bg="white").place(x=20, y=20)

        self.var_fname = StringVar()
        self.var_lname = StringVar()
        self.var_contact = StringVar()
        self.var_email = StringVar()
        self.var_sec_question = StringVar(value="Select")
        self.var_sec_answer = StringVar()
        self.var_password = StringVar()
        self.var_confirm_password = StringVar()
        self.var_terms = IntVar()

        fields = [
            ("First Name", self.var_fname, 50, 100),
            ("Last Name", self.var_lname, 370, 100),
            ("Contact", self.var_contact, 50, 180),
            ("Email", self.var_email, 370, 180),
            ("Security Answer", self.var_sec_answer, 370, 270),
            ("Password", self.var_password, 50, 350),
            ("Confirm Password", self.var_confirm_password, 370, 350),
        ]
        for label, variable, x, y in fields:
            Label(frame, text=label, font=("times new roman", 15, "bold"), bg="white").place(x=x, y=y)
            Entry(frame, textvariable=variable, show="*" if "Password" in label else None, font=("times new roman", 16)).place(x=x, y=y + 30, width=250)

        Label(frame, text="Select security question", font=("times new roman", 15, "bold"), bg="white").place(x=50, y=270)
        ttk.Combobox(
            frame,
            textvariable=self.var_sec_question,
            values=("Select", "Your Birth Place?", "Your Bestfriend name?", "Your Pet Name?"),
            state="readonly",
            font=("times new roman", 12, "bold"),
        ).place(x=50, y=300, width=250, height=37)
        Checkbutton(frame, text="I Agree the Terms & Conditions", variable=self.var_terms, bg="white").place(x=50, y=425)
        Button(frame, text="Register", command=self.register_data, bg="green", fg="white", font=("times new roman", 13, "bold")).place(x=70, y=465, width=200, height=40)

    def register_data(self):
        values = (
            self.var_fname.get().strip(),
            self.var_lname.get().strip(),
            self.var_contact.get().strip(),
            self.var_email.get().strip(),
            self.var_sec_question.get(),
            self.var_sec_answer.get().strip(),
            self.var_password.get(),
        )
        if not values[0] or not values[3] or values[4] == "Select":
            messagebox.showerror("Error", "First name, email, and security question are required", parent=self.root)
            return
        if values[6] != self.var_confirm_password.get():
            messagebox.showerror("Error", "Password and confirm password must be the same", parent=self.root)
            return
        if not self.var_terms.get():
            messagebox.showerror("Error", "Please agree to the terms and conditions", parent=self.root)
            return

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT 1 FROM register WHERE email=%s", (values[3],))
            if cursor.fetchone():
                messagebox.showerror("Error", "User already exists", parent=self.root)
                return
            cursor.execute(
                """
                INSERT INTO register
                    (fname, lname, contact, email, secQ, secA, `pass`)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                values,
            )
            connection.commit()
        except Exception as error:
            messagebox.showerror("Database error", str(error), parent=self.root)
            return
        finally:
            try:
                cursor.close()
                connection.close()
            except (NameError, AttributeError):
                pass
        messagebox.showinfo("Success", "Registration successful", parent=self.root)


if __name__ == "__main__":
    root = Tk()
    Register(root)
    root.mainloop()
