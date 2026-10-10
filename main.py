from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from student import Student
import os
from tkinter import messagebox
from config import asset_path, DATA_DIR
from attendance import Attendance
from train import Train
from face_recognition import Face_Recognition
from dev import Developer

class Face_Recognition_System:

    def Student_details(self):
            self.new_window=Toplevel(self.root)
            self.app=Student(self.new_window)
    
    def open_img(self):
         os.startfile(str(DATA_DIR))

    def exit_app(self):
         self.root.destroy()

    def show_help(self):
         messagebox.showinfo(
             "Help",
             "Add a student, capture face samples, train the model, then start face recognition.",
             parent=self.root,
         )

    def Train_photo(self):
        self.new_window=Toplevel(self.root)
        self.app=Train(self.new_window)

    def face_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Face_Recognition(self.new_window)
    
    def attendance_data(self):
        self.new_window=Toplevel(self.root)
        self.app=Attendance(self.new_window)

    def developer(self):
            self.new_window=Toplevel(self.root)
            self.app=Developer(self.new_window)

    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")  

        img=Image.open(asset_path("Stanford.jpg"))
        img=img.resize((500,130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)

        #second image
        img1=Image.open(asset_path("facialrecognition.png"))
        img1=img1.resize((500,130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)

        #Third image
        img2=Image.open(asset_path("u.jpg"))
        img2=img2.resize((500,130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl=Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=550,height=130)


        #bg imag
        img3=Image.open(asset_path("tech.jpg"))
        img3=img3.resize((1530,710), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)

        title_lbl = Label(bg_img,text="FACE RECOGNITION ATTENDANCE SYSTEM SOFTWARE",font=("times new roman",35,"bold"),bg="green",fg="white")
        title_lbl.place(x=0,y=0,width=1530,height=50)

        


        
        #student button
        img4=Image.open(asset_path("student.jpg"))
        img4=img4.resize((220,220), Image.LANCZOS)
        self.photoimg4 = ImageTk.PhotoImage(img4)

        b1=Button(bg_img,image=self.photoimg4,command=self.Student_details,cursor="hand2")
        b1.place(x=200, y=100,width=220,height=220)

        b1_1=Button(bg_img,text="Student Details",command=self.Student_details,cursor="hand2",font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_1.place(x=200,y=300,width=220,height=40)

        #detect face button 
        img5=Image.open(asset_path("face_detector.jpg"))
        img5=img5.resize((220,220), Image.LANCZOS)
        self.photoimg5 = ImageTk.PhotoImage(img5)
        b2=Button(bg_img,image=self.photoimg5,command=self.face_data,cursor="hand2")
        b2.place(x=500, y=100,width=220,height=220)

        b1_2=Button(bg_img,text="Face Detector",command=self.face_data,cursor="hand2",font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_2.place(x=500,y=300,width=220,height=40)

        
        #Attendance
        img6=Image.open(asset_path("attendance.jpg"))
        img6=img6.resize((220,220), Image.LANCZOS)
        self.photoimg6 = ImageTk.PhotoImage(img6)

        b2=Button(bg_img,image=self.photoimg6,command=self.attendance_data,cursor="hand2")
        b2.place(x=800, y=100,width=220,height=220)

        b1_2=Button(bg_img,text="Attendance",command=self.attendance_data,cursor="hand2",font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_2.place(x=800,y=300,width=220,height=40)
       
        


        #Help face button
        img7=Image.open(asset_path("help.jpg"))
        img7=img7.resize((220,220), Image.LANCZOS)
        self.photoimg7 = ImageTk.PhotoImage(img7)

        b3=Button(bg_img,image=self.photoimg7,cursor="hand2",command=self.show_help)
        b3.place(x=1100, y=100,width=220,height=220)

        b1_3=Button(bg_img,text="Help Desk",cursor="hand2",command=self.show_help,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_3.place(x=1100,y=300,width=220,height=40)


        #train face button
        img8=Image.open(asset_path("Train.jpg"))
        img8=img8.resize((220,220), Image.LANCZOS)
        self.photoimg8 = ImageTk.PhotoImage(img8)

        b4=Button(bg_img,image=self.photoimg8,command=self.Train_photo,cursor="hand2")
        b4.place(x=200, y=400,width=220,height=220)

        b1_4=Button(bg_img,text="Train Photos",command=self.Train_photo,cursor="hand2",font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_4.place(x=200,y=600,width=220,height=40)


        #photos face button
        img9=Image.open(asset_path("photosBtn.jpg"))
        img9=img9.resize((220,220), Image.LANCZOS)
        self.photoimg9 = ImageTk.PhotoImage(img9)

        b5=Button(bg_img,image=self.photoimg9,cursor="hand2",command=self.open_img)
        b5.place(x=500, y=400,width=220,height=220)

        b1_5=Button(bg_img,text="Photo",cursor="hand2",command=self.open_img,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_5.place(x=500,y=600,width=220,height=40)


        #developer
        img10=Image.open(asset_path("developer.jpg"))
        img10=img10.resize((220,220), Image.LANCZOS)
        self.photoimg10 = ImageTk.PhotoImage(img10)

        b6=Button(bg_img,image=self.photoimg10,command=self.developer,cursor="hand2")
        b6.place(x=800, y=400,width=220,height=220)

        b1_6=Button(bg_img,text="Developer",command=self.developer,cursor="hand2",font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_6.place(x=800,y=600,width=220,height=40)



        #Exit face button
        img11=Image.open(asset_path("exit.jpg"))
        img11=img11.resize((220,220), Image.LANCZOS)
        self.photoimg11 = ImageTk.PhotoImage(img11)

        b7=Button(bg_img,image=self.photoimg11,cursor="hand2",command=self.exit_app)
        b7.place(x=1100, y=400,width=220,height=220)

        b1_7=Button(bg_img,text="Exit",cursor="hand2",command=self.exit_app,font=("times new roman",15,"bold"),bg="darkblue",fg="white")
        b1_7.place(x=1100,y=600,width=220,height=40)

        




if __name__ == "__main__":
    root=Tk()
    obj = Face_Recognition_System(root)
    root.mainloop()
