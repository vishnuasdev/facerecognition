from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import mysql.connector
import cv2
from config import asset_path

class Developer:

    ##################################--MAIN FUCNTION--##########################
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Developer")

        title_lbl = Label(self.root,text="DEVELOPED TEAM DETAILS",font=("times new roman",35,"bold"),bg="white",fg="darkgreen")
        title_lbl.place(x=0,y=0,width=1530,height=45)

        #left top image
        img3=Image.open(asset_path("dev.jpg"))
        img3=img3.resize((1530,720), Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img3)

        f_lbl=Label(self.root,image=self.photoimg_left)
        f_lbl.place(x=0,y=55,width=1530,height=720)

        
        

        #Frame
        main_frame=Frame(f_lbl,bd=5,bg="black")
        main_frame.place(x=1000,y=55,width=500,height=600)
        
        img3=Image.open(asset_path("vishnu.jpg"))
        img3=img3.resize((95,120), Image.LANCZOS)
        self.photoimg_lead = ImageTk.PhotoImage(img3)

        f_lb2=Label(main_frame,image=self.photoimg_lead)
        f_lb2.place(x=200,y=60,width=95,height=120)

        f_lb3=Label(main_frame,text="VISHNU V (TEAM LEADER)",font=("times new roman",12,"bold"),fg="white",bg="black")
        f_lb3.place(x=100,y=180,width=300,height=40)

        

        

        mem_frame=Frame(main_frame,bd=5,bg="white")
        mem_frame.place(x=0,y=250,width=490,height=340)

        mem_lbl = Label(mem_frame,text="TEAM MEMBERS",font=("times new roman",16,"bold"),bg="green",fg="white")
        mem_lbl.place(x=0,y=0,width=480,height=40)
        

        #mem1
        img4=Image.open(asset_path("sakthivel.jpg"))
        img4=img4.resize((95,120), Image.LANCZOS)
        self.photoimg_mem1 = ImageTk.PhotoImage(img4)

        f_lb2=Label(mem_frame,image=self.photoimg_mem1)
        f_lb2.place(x=40,y=50,width=95,height=120)

        f_lb3=Label(mem_frame,text="SAKTHIVEL",font=("times new roman",12,"bold"),fg="black",bg="white")
        f_lb3.place(x=40,y=165,width=100,height=40)

        #mem2
        img4=Image.open(asset_path("sakthivel.jpg"))
        img4=img4.resize((95,120), Image.LANCZOS)
        self.photoimg_mem1 = ImageTk.PhotoImage(img4)

        f_lb2=Label(mem_frame,image=self.photoimg_mem1)
        f_lb2.place(x=200,y=50,width=95,height=120)

        f_lb3=Label(mem_frame,text="VISHNU P",font=("times new roman",12,"bold"),fg="black",bg="white")
        f_lb3.place(x=200,y=165,width=100,height=40)

        #mem3
        img4=Image.open(asset_path("sakthivel.jpg"))
        img4=img4.resize((95,120), Image.LANCZOS)
        self.photoimg_mem1 = ImageTk.PhotoImage(img4)

        f_lb2=Label(mem_frame,image=self.photoimg_mem1)
        f_lb2.place(x=340,y=50,width=95,height=120)

        f_lb3=Label(mem_frame,text="SHAGUL",font=("times new roman",12,"bold"),fg="black",bg="white")
        f_lb3.place(x=340,y=165,width=100,height=40)


        



##########################--MAIN--######################
if __name__ == "__main__":
    root=Tk()
    obj = Developer(root) 
    root.mainloop()