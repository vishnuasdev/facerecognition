from tkinter import *
from tkinter import messagebox

from config import DATA_DIR
from face_embeddings import enroll_dataset


class Train:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System - Train Model")
        Label(
            self.root,
            text="TRAIN FACE EMBEDDINGS",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="darkgreen",
        ).pack(side=TOP, fill=X)
        Button(
            self.root,
            text="TRAIN DATA",
            command=self.train_classifier,
            font=("times new roman", 20, "bold"),
            bg="darkblue",
            fg="white",
        ).place(x=600, y=380, width=300, height=70)

    def train_classifier(self):
        if not DATA_DIR.exists():
            messagebox.showerror(
                "Error",
                "The data directory was not found. Capture student photos first.",
                parent=self.root,
            )
            return
        try:
            profiles, skipped = enroll_dataset(DATA_DIR)
        except (FileNotFoundError, ValueError, RuntimeError) as error:
            messagebox.showerror("Embedding training error", str(error), parent=self.root)
            return
        messagebox.showinfo(
            "Result",
            f"Embedding training completed for {len(profiles)} students. "
            f"Skipped {skipped} invalid or low-quality images.",
            parent=self.root,
        )


if __name__ == "__main__":
    root = Tk()
    Train(root)
    root.mainloop()
