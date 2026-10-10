from collections import defaultdict
from datetime import datetime
import csv
from tkinter import *
from tkinter import messagebox

import cv2

from config import ATTENDANCE_PATH, connect_db
from face_embeddings import (
    MATCH_THRESHOLD,
    create_detector,
    create_recognizer,
    detect_faces,
    embedding,
    load_profiles,
    match_embedding,
    quality_reason,
)

REQUIRED_STABLE_FRAMES = 7


class Face_Recognition:
    def __init__(self, root):
        self.root = root
        self.status_var = StringVar(value="Ready to recognize multiple faces")
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition Attendance System")
        Label(
            self.root,
            text="FACE RECOGNITION ATTENDANCE",
            font=("times new roman", 35, "bold"),
            bg="white",
            fg="green",
        ).pack(side=TOP, fill=X)
        Label(
            self.root,
            textvariable=self.status_var,
            font=("times new roman", 14, "bold"),
            bg="white",
            fg="darkblue",
        ).pack(side=TOP, fill=X)
        Button(
            self.root,
            text="Start Face Recognition",
            command=self.face_rec,
            font=("times new roman", 18, "bold"),
            bg="darkgreen",
            fg="white",
        ).place(x=600, y=350, width=300, height=60)
        Button(
            self.root,
            text="Back",
            command=self.back_to_home,
            font=("times new roman", 15, "bold"),
            bg="red",
            fg="white",
        ).place(x=650, y=450, width=200, height=40)

    def back_to_home(self):
        self.root.destroy()

    def mark_attendance(self, student_id, roll, name, department):
        filename = str(ATTENDANCE_PATH)
        headers = ["Student ID", "Roll No", "Name", "Department", "Time", "Date", "Status"]
        try:
            with open(filename, "a+", newline="", encoding="utf-8") as file:
                file.seek(0)
                rows = list(csv.reader(file))
                if not rows:
                    csv.writer(file).writerow(headers)
                    rows = [headers]
                today = datetime.now().strftime("%d/%m/%Y")
                if any(
                    len(row) >= 6 and row[0] == str(student_id) and row[5] == today
                    for row in rows[1:]
                ):
                    return False
                csv.writer(file).writerow(
                    [
                        student_id,
                        roll,
                        name,
                        department,
                        datetime.now().strftime("%H:%M:%S"),
                        today,
                        "Present",
                    ]
                )
                return True
        except OSError as error:
            print(f"Attendance file error: {error}")
            return False

    def face_rec(self):
        try:
            detector = create_detector()
            recognizer = create_recognizer()
            profiles = load_profiles()
        except (FileNotFoundError, RuntimeError, ValueError) as error:
            messagebox.showerror("Recognition setup error", str(error), parent=self.root)
            return

        try:
            connection = connect_db()
            cursor = connection.cursor()
            cursor.execute("SELECT roll, Name, Department, Student_id FROM student")
            students = {
                str(student_id): (roll, name, department, student_id)
                for roll, name, department, student_id in cursor.fetchall()
            }
        except Exception as error:
            messagebox.showerror("Database error", str(error), parent=self.root)
            return
        finally:
            try:
                cursor.close()
                connection.close()
            except (NameError, AttributeError):
                pass

        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            messagebox.showerror("Error", "Unable to open the camera.", parent=self.root)
            return

        stable_counts = defaultdict(int)
        last_identity = {}
        session_marked = set()
        try:
            while True:
                ret, frame = camera.read()
                if not ret:
                    break
                recognized_count = 0
                faces = detect_faces(detector, frame)
                for face in faces:
                    x, y, width, height = face[:4].astype(int)
                    x1, y1 = max(x, 0), max(y, 0)
                    face_crop = frame[y1:y1 + height, x1:x1 + width]
                    reason = quality_reason(face_crop)
                    identity, score = (None, 0.0)
                    if reason is None:
                        identity, score = match_embedding(embedding(recognizer, frame, face), profiles)
                    key = f"{x // 40}:{y // 40}"
                    if identity is not None:
                        if last_identity[key] == identity:
                            stable_counts[key] += 1
                        else:
                            stable_counts[key] = 1
                            last_identity[key] = identity
                        student = students.get(identity)
                        if student and stable_counts[key] >= REQUIRED_STABLE_FRAMES:
                            roll, name, department, student_id = student
                            recognized_count += 1
                            if identity not in session_marked:
                                self.mark_attendance(student_id, roll, name, department)
                                session_marked.add(identity)
                        label = f"{student[1]} {score:.2f}" if student else "Unknown"
                        color = (0, 255, 0) if student else (0, 0, 255)
                    else:
                        stable_counts[key] = 0
                        last_identity.pop(key, None)
                        label = reason or "Unknown"
                        color = (0, 165, 255) if reason else (0, 0, 255)
                    cv2.rectangle(frame, (x, y), (x + width, y + height), color, 2)
                    cv2.putText(frame, label, (x, max(y - 10, 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.65, color, 2)

                self.status_var.set(
                    f"Faces: {len(faces)} | Confirmed: {recognized_count} | "
                    f"Saved: {len(session_marked)} | Threshold: {MATCH_THRESHOLD:.2f}"
                )
                cv2.imshow("Smart Attendance - Embedding Recognition", frame)
                if cv2.waitKey(1) == 13:
                    break
        finally:
            camera.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    root = Tk()
    Face_Recognition(root)
    root.mainloop()
