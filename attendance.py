from datetime import datetime
from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox, filedialog
import mysql.connector
from time import strftime
import cv2, os, csv
import numpy as np
from config import asset_path


mydata=[]
class Attendance:
    
    def fetchData(self,rows):
        self.AttendanceReportTable.delete(*self.AttendanceReportTable.get_children())
        for i in rows:
            self.AttendanceReportTable.insert("",END, values=i)

    def importCsv(self):
        global mydata
        mydata.clear()
        fln=filedialog.askopenfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*csv"),("All File","*.*")),parent=self.root)
        if not fln:
            return
        with open(fln) as myfile:
            csvread=csv.reader(myfile,delimiter=",")
            for i in csvread:
                mydata.append(i)
            self.fetchData(mydata)
    
    def exportCsv(self):
        try:
            if len(mydata)<1:
                messagebox.showerror("No Data","No Data found to export",parent=self.root)
                return False
            fln=filedialog.asksaveasfilename(initialdir=os.getcwd(),title="Open CSV",filetypes=(("CSV File","*csv"),("All File","*.*")),parent=self.root)
            with open(fln,mode="w",newline="") as myfile:
                exp_write=csv.writer(myfile, delimiter=",")
                for i in mydata:
                    exp_write.writerow(i)
                messagebox.showinfo("Data Export","Your data exported to "+ os.path.basename(fln)+" Successfully")
        except Exception as es:
            messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)


    def get_cursor(self,event=""):
        cursor_row=self.AttendanceReportTable.focus()
        content=self.AttendanceReportTable.item(cursor_row)
        rows=content['values']
        self.var_atten_id.set(rows[0])
        self.var_atten_roll.set(rows[1])
        self.var_atten_name.set(rows[2])
        self.var_atten_dep.set(rows[3])
        self.var_atten_time.set(rows[4])
        self.var_atten_date.set(rows[5])
        self.var_atten_attendance.set(rows[6])


    def reset_data(self):
        self.var_atten_id.set("")
        self.var_atten_roll.set("")
        self.var_atten_name.set("")
        self.var_atten_dep.set("")
        self.var_atten_time.set("")
        self.var_atten_date.set("")
        self.var_atten_attendance.set("")

    def update_data(self):
        """Update the selected in-memory CSV row and refresh the table."""
        selected = self.AttendanceReportTable.focus()
        if not selected:
            messagebox.showerror("Error", "Select an attendance record first", parent=self.root)
            return
        values = [
            self.var_atten_id.get(),
            self.var_atten_roll.get(),
            self.var_atten_name.get(),
            self.var_atten_dep.get(),
            self.var_atten_time.get(),
            self.var_atten_date.get(),
            self.var_atten_attendance.get(),
        ]
        index = self.AttendanceReportTable.index(selected)
        if index >= len(mydata):
            return
        mydata[index] = values
        self.fetchData(mydata)
        

        
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Attendance")


        ##############--VARIABLES--###################
        self.var_atten_id=StringVar()
        self.var_atten_roll=StringVar()
        self.var_atten_name=StringVar()
        self.var_atten_dep=StringVar()
        self.var_atten_time=StringVar()
        self.var_atten_date=StringVar()
        self.var_atten_attendance=StringVar()

        
        #first 
        img=Image.open(asset_path("h2.jpg"))
        img=img.resize((800,200), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=800,height=200)

        #second
        img1=Image.open(asset_path("h3.jpg"))
        img1=img1.resize((800,200), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lb2=Label(self.root,image=self.photoimg1)
        f_lb2.place(x=800,y=0,width=800,height=200)

        #bg image
        img2=Image.open(asset_path("tech.jpg"))
        img2=img2.resize((1530,710), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        bg_img=Label(self.root,image=self.photoimg2)
        bg_img.place(x=0,y=200,width=1535,height=710)

        title_lbl = Label(bg_img,text="STUDENT ATTENDANCE MANAGEMENT",font=("times new roman",35,"bold"),bg="white",fg="red")
        title_lbl.place(x=0,y=0,width=1530,height=50)

        #############--LEFT FRAME--#################
        Left_frame=LabelFrame(bg_img,bd=2,bg="white",relief=RIDGE,text="Student Attendance Details",font=("times new roman", 12,"bold"))
        Left_frame.place(x=5,y=55,width=745,height=530)

        img3=Image.open(asset_path("f1.jpeg"))
        img3=img3.resize((720,580), Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img3)

        f_lbl=Label(Left_frame,image=self.photoimg_left)
        f_lbl.place(x=5,y=0,width=730,height=130)

        left_inside_frame=Frame(Left_frame,bd=2,relief=RIDGE,bg="white")
        left_inside_frame.place(x=10,y=135,width=720,height=300)


        ######################--LABELAND ENTRY--#########################

        #attendance id
        attendanceId_label=Label(left_inside_frame,text='Attendance ID:',font=("times new roman", 12,"bold"),bg="white")
        attendanceId_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)
        
        attendanceId_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_id, font=("times new roman", 12,"bold"))
        attendanceId_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W) 

        #roll no
        rollNo_label=Label(left_inside_frame,text='Roll No:',font=("times new roman", 12,"bold"),bg="white")
        rollNo_label.grid(row=0,column=2,padx=10,pady=5,sticky=W)
        
        rollNo_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_name,font=("times new roman", 12,"bold"))
        rollNo_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W) 

        #Name
        name_label=Label(left_inside_frame,text='Name:',font=("times new roman", 12,"bold"),bg="white")
        name_label.grid(row=1,column=0,padx=10,pady=5,sticky=W)
        
        name_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_name, font=("times new roman", 12,"bold"))
        name_entry.grid(row=1, column=1, padx=10, pady=5, sticky=W) 

        #Department
        dept_label=Label(left_inside_frame,text='Department:',font=("times new roman", 12,"bold"),bg="white")
        dept_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)
        
        dept_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_dep,font=("times new roman", 12,"bold"))
        dept_entry.grid(row=1, column=3, padx=10, pady=5, sticky=W) 

        #Time
        time_label=Label(left_inside_frame,text='Time:',font=("times new roman", 12,"bold"),bg="white")
        time_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)
        
        time_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_time, font=("times new roman", 12,"bold"))
        time_entry.grid(row=2, column=1, padx=10, pady=5, sticky=W) 

        #Date
        date_label=Label(left_inside_frame,text='Date:',font=("times new roman", 12,"bold"),bg="white")
        date_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)
        
        date_entry=ttk.Entry(left_inside_frame,width=20,textvariable=self.var_atten_date,font=("times new roman", 12,"bold"))
        date_entry.grid(row=2, column=3, padx=10, pady=5, sticky=W) 

        #Attendance status
        atted_status_label=Label(left_inside_frame,text='Attendance Status:',font=("times new roman", 12,"bold"),bg="white")
        atted_status_label.grid(row=3,column=0,padx=1,pady=5,sticky=W)

        self.atted_status_combo=ttk.Combobox(left_inside_frame,textvariable=self.var_atten_attendance,font=("times new roman", 12,"bold"),state="readonly",width=18)
        self.atted_status_combo["values"]=("Present","Absent")
        self.atted_status_combo.current(0)
        self.atted_status_combo.grid(row=3,column=1,padx=10,pady=5,sticky=W)


        #Button frame and Buttons

        btn_frame=Frame(left_inside_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=2,y=210,width=720,height=35)

        importCsv_btn=Button(btn_frame,text="Import csv",command=self.importCsv,width=20,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        importCsv_btn.grid(row=0,column=0)

        ExportCsv_btn=Button(btn_frame,text="Export csv",command=self.exportCsv,width=20,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        ExportCsv_btn.grid(row=0,column=1)

        update_btn=Button(btn_frame,text="Update",command=self.update_data,width=18,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data,width=17,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)
 

        ##############--RIGHT FRAME--################
        Right_frame=LabelFrame(bg_img,bd=2,bg="white",relief=RIDGE,text="Attendance Details",font=("times new roman", 12,"bold"))
        Right_frame.place(x=760,y=55,width=760,height=530)

        table_frame=Frame(Right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=5,width=740,height=445)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.AttendanceReportTable=ttk.Treeview(table_frame,columns=("ID","ROLL NO","NAME","DEPARTMENT","TIME","DATE","ATTENDANCE"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT,fill=Y) 

        scroll_x.config(command=self.AttendanceReportTable.xview)
        scroll_y.config(command=self.AttendanceReportTable.yview)  

        self.AttendanceReportTable.heading("ID",text="ATTENDANCE ID")
        self.AttendanceReportTable.heading("ROLL NO",text="ROLL")
        self.AttendanceReportTable.heading("NAME",text="NAME")
        self.AttendanceReportTable.heading("DEPARTMENT",text="DEPARTMENT")
        self.AttendanceReportTable.heading("TIME",text="TIME")
        self.AttendanceReportTable.heading("DATE",text="DATE")
        self.AttendanceReportTable.heading("ATTENDANCE",text="ATTENDANCE")
        self.AttendanceReportTable["show"]="headings"

        self.AttendanceReportTable.column("ID",width=100)
        self.AttendanceReportTable.column("ROLL NO",width=100)
        self.AttendanceReportTable.column("NAME",width=100)
        self.AttendanceReportTable.column("DEPARTMENT",width=100)
        self.AttendanceReportTable.column("TIME",width=100)
        self.AttendanceReportTable.column("DATE",width=100)
        self.AttendanceReportTable.column("ATTENDANCE",width=100)
        
        self.AttendanceReportTable.pack(fill=BOTH,expand=1)
        self.AttendanceReportTable.bind("<ButtonRelease>",self.get_cursor)



if __name__ == "__main__":
    root=Tk()
    obj = Attendance(root) 
    root.mainloop()