from tkinter import*
from tkinter import ttk
from PIL import Image,ImageTk
from tkinter import messagebox
import cv2
from config import asset_path, connect_db, ensure_data_dir
from face_embeddings import create_detector, detect_faces


class Student:
    
    ###############################--ADD DATA TO DATABASE--###########################
    def add_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields ar required",parent=self.root)
        else:
            try:
                conn = connect_db()
                my_cursor=conn.cursor()
                my_cursor.execute(
                    """
                    INSERT INTO student
                        (Department, course, year, semester, Student_id, Name,
                         Division, roll, Gender, dob, email, phone,
                         address, teacher, photosample)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s)
                    """,
                    (
                                                                                        self.var_dep.get(),
                                                                                        self.var_course.get(),
                                                                                        self.var_year.get(),
                                                                                        self.var_semester.get(),
                                                                                        self.var_std_id.get(),
                                                                                        self.var_std_name.get(),
                                                                                        self.var_div.get(),
                                                                                        self.var_roll.get(),
                                                                                        self.var_gender.get(),
                                                                                        self.var_dob.get(),
                                                                                        self.var_email.get(),
                                                                                        self.var_phone.get(),
                                                                                        self.var_address.get(),
                                                                                        self.var_teacher.get(),
                                                                                        self.var_radio1.get()
                    ),
                )
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Success","Student details has been added Successfully",parent=self.root)

                
            except Exception as es:
                messagebox.showerror("Error",f"Due to: {str(es)}",parent=self.root) 




    #################################--FETCH DATA TO DATABASE--###################
    def fetch_data(self):
            conn = connect_db()
            my_cursor=conn.cursor()

            my_cursor.execute("select*from student")
            data=my_cursor.fetchall()

            if len(data)!=0:
                self.student_tab1.delete(*self.student_tab1.get_children())
                for i in data:
                    self.student_tab1.insert("",END,values=i)
                conn.commit()


    ################################--GET CURSOR--#############################
    def get_cursor(self,event=""):
        cursor_focus=self.student_tab1.focus()
        content=self.student_tab1.item(cursor_focus)
        data=content["values"]

        self.var_dep.set(data[0]),
        self.var_course.set(data[1]),
        self.var_year.set(data[2]),
        self.var_semester.set(data[3]),
        self.var_std_id.set(data[4]),
        self.var_std_name.set(data[5]),
        self.var_div.set(data[6]),
        self.var_roll.set(data[7]),
        self.var_gender.set(data[8]),
        self.var_dob.set(data[9]),
        self.var_email.set(data[10]),
        self.var_phone.set(data[11]),
        self.var_address.set(data[12]),
        self.var_teacher.set(data[13]),
        self.var_radio1.set(data[14])
    
    ###############--UPDATE FUNCTION--################
    def update_data(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields ar required",parent=self.root)
        
        else:
            try:
                Update=messagebox.askyesno("Update","Do you want to update this student details",parent=self.root)
                if Update>0:
                    conn = connect_db()
                    my_cursor=conn.cursor()
                    my_cursor.execute("update student set Department=%s, course=%s, year=%s, semester=%s, Name=%s, Division=%s, roll=%s, Gender=%s, dob=%s, email=%s, phone=%s, address=%s, teacher=%s, photosample=%s where Student_id=%s",(
                                                                                        self.var_dep.get(),
                                                                                        self.var_course.get(),
                                                                                        self.var_year.get(),
                                                                                        self.var_semester.get(),
                                                                                        self.var_std_name.get(),
                                                                                        self.var_div.get(),
                                                                                        self.var_roll.get(),
                                                                                        self.var_gender.get(),
                                                                                        self.var_dob.get(),
                                                                                        self.var_email.get(),
                                                                                        self.var_phone.get(),
                                                                                        self.var_address.get(),
                                                                                        self.var_teacher.get(),
                                                                                        self.var_radio1.get(),
                                                                                        self.var_std_id.get()
                                                                                        
                                                                                    ))
                else:
                    if not Update:
                        return 
                messagebox.showinfo("Success","Student details successfully update completed",parent=self.root)
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    ########################--DELETE DAT--###########################
    def delete_data(self):
        if self.var_std_id.get()=="":
            messagebox.showerror("Error","Student id must be required ", parent=self.root)
        else:
            try:
                delete=messagebox.askyesno("Student Delete Page", "Do you want to delete this student", parent=self.root)
                if delete>0:
                    conn = connect_db()
                    my_cursor=conn.cursor()
                    sql="delete from student where Student_id=%s"
                    val=(self.var_std_id.get(),)
                    my_cursor.execute(sql,val)
                else:
                    if not delete:
                        return
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()
                messagebox.showinfo("Delete","Successfully deleted student details", parent=self.root)

            except Exception as es:
                messagebox.showerror("Error",f"Due To:{str(es)}",parent=self.root)

    ######################--RESET FUNCTION--######################
    def reset_data(self):
        self.var_dep.set("Select Department"),
        self.var_course.set("Select Course"),
        self.var_year.set("Select Year"),
        self.var_semester.set("Select Semester"),
        self.var_std_id.set(""),
        self.var_std_name.set(""),
        self.var_div.set("Select Division"),
        self.var_roll.set(""),
        self.var_gender.set("Male"),
        self.var_dob.set(""),
        self.var_email.set(""),
        self.var_phone.set(""),
        self.var_address.set(""),
        self.var_teacher.set(""),
        self.var_radio1.set("")

    ########################--GENERATE DATA SET TAKE PHOTO SAMPLE--#################
    def generate_dataset(self):
        if self.var_dep.get()=="Select Department" or self.var_std_name.get()=="" or self.var_std_id.get()=="":
            messagebox.showerror("Error","All Fields ar required",parent=self.root)
        
        else:
            try:
                conn = connect_db()
                my_cursor=conn.cursor()
                my_cursor.execute("select*from student")
                myresult=my_cursor.fetchall()
                id=0
                for x in myresult:
                    id+=1
                my_cursor.execute("update student set Department=%s, course=%s, year=%s, semester=%s, Name=%s, Division=%s, roll=%s, Gender=%s, dob=%s, email=%s, phone=%s, address=%s, teacher=%s, photosample=%s where Student_id=%s",(
                                                                                        self.var_dep.get(),
                                                                                        self.var_course.get(),
                                                                                        self.var_year.get(),
                                                                                        self.var_semester.get(),
                                                                                        self.var_std_name.get(),
                                                                                        self.var_div.get(),
                                                                                        self.var_roll.get(),
                                                                                        self.var_gender.get(),
                                                                                        self.var_dob.get(),
                                                                                        self.var_email.get(),
                                                                                        self.var_phone.get(),
                                                                                        self.var_address.get(),
                                                                                        self.var_teacher.get(),
                                                                                        self.var_radio1.get(),
                                                                                        self.var_std_id.get()
                                                                                    ))
                id=self.var_std_id.get()
                conn.commit()
                self.fetch_data()
                self.reset_data()
                conn.close()

                ###############--LOAD PREDIFIEND DATA ON FACE FROM OPENCV--###########
                ensure_data_dir()
                def face_cropped(img):
                    faces = detect_faces(face_detector, img)
                    if len(faces) != 1:
                        return None
                    x, y, w, h = faces[0, :4].astype(int)
                    return img[max(y, 0):y + h, max(x, 0):x + w]
                    
                face_detector = create_detector()
                cap=cv2.VideoCapture(0)
                if not cap.isOpened():
                    raise RuntimeError("Unable to open the camera")
                img_id=0
                
                while True:
                    ret,my_frame=cap.read()
                    if not ret:
                        break
                    cropped_face = face_cropped(my_frame)
                    if cropped_face is not None:
                        img_id+=1
                        face=cv2.resize(cropped_face,(450,450))
                        face=cv2.cvtColor(face,cv2.COLOR_BGR2GRAY)
                        file_name_path="data/user."+str(id)+"."+str(img_id)+".jpg"
                        cv2.imwrite(file_name_path,face)
                        cv2.putText(face,str(img_id),(50,50),cv2.FONT_HERSHEY_COMPLEX,2,(0,255,0),2)
                        cv2.imshow("Croped Face", face)

                    if cv2.waitKey(1)==13 or int(img_id)==100:
                        break
                cap.release()
                cv2.destroyAllWindows()
                messagebox.showinfo("Result","Generating data sets completed!!!!!!!!!")

            except Exception as es:
                messagebox.showerror("Error",f"DONT SHAKE YOUR FACE WHILE CAPTURE. TRY AGAIN!:{str(es)}",parent=self.root)

    





    ##################################--MAIN FUCNTION--##########################
    def __init__(self,root):
        self.root=root
        self.root.geometry("1530x790+0+0")
        self.root.title("Face Recognition System")

        
        #*************Variables*****************

        self.var_dep=StringVar()
        self.var_course=StringVar()
        self.var_year=StringVar()
        self.var_semester=StringVar()
        self.var_std_id=StringVar()
        self.var_std_name=StringVar()
        self.var_div=StringVar()
        self.var_roll=StringVar()
        self.var_gender=StringVar()
        self.var_dob=StringVar()
        self.var_email=StringVar()
        self.var_phone=StringVar()
        self.var_address=StringVar()
        self.var_teacher=StringVar()


    
    
        
        #####################--IMAGES--#####################

        img=Image.open(asset_path("h1.jpg"))
        img=img.resize((500,130), Image.LANCZOS)
        self.photoimg = ImageTk.PhotoImage(img)

        f_lbl=Label(self.root,image=self.photoimg)
        f_lbl.place(x=0,y=0,width=500,height=130)

        #second image
        img1=Image.open(asset_path("h2.jpg"))
        img1=img1.resize((500,130), Image.LANCZOS)
        self.photoimg1 = ImageTk.PhotoImage(img1)

        f_lbl=Label(self.root,image=self.photoimg1)
        f_lbl.place(x=500,y=0,width=500,height=130)

        #Third image
        img2=Image.open(asset_path("h3.jpg"))
        img2=img2.resize((500,130), Image.LANCZOS)
        self.photoimg2 = ImageTk.PhotoImage(img2)

        f_lbl=Label(self.root,image=self.photoimg2)
        f_lbl.place(x=1000,y=0,width=500,height=130)


        #bg image
        img3=Image.open(asset_path("tech.jpg"))
        img3=img3.resize((1530,710), Image.LANCZOS)
        self.photoimg3 = ImageTk.PhotoImage(img3)

        bg_img=Label(self.root,image=self.photoimg3)
        bg_img.place(x=0,y=130,width=1530,height=710)



        ###################--HEADER--#########################
        title_lbl = Label(bg_img,text="STUDENT MANAGEMENT SYSTEM",font=("times new roman",35,"bold"),bg="white",fg="darkgreen")
        title_lbl.place(x=0,y=0,width=1530,height=50)


        ###################--MAIN FRAME--###########################
        main_frame=Frame(bg_img,bd=2,bg="white")
        main_frame.place(x=10,y=55,width=1500,height=650)


        ##################--LEFT FRAME--############################
        Left_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("times new roman", 12,"bold"))
        Left_frame.place(x=10,y=10,width=720,height=580)

        #left top image
        img3=Image.open(asset_path("f1.jpeg"))
        img3=img3.resize((720,580), Image.LANCZOS)
        self.photoimg_left = ImageTk.PhotoImage(img3)

        f_lbl=Label(Left_frame,image=self.photoimg_left)
        f_lbl.place(x=5,y=0,width=705,height=130)

        
        ###############--CURRENT COURSE FRAME--###################
        current_course_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Current Course Details",font=("times new roman", 12,"bold"))
        current_course_frame.place(x=15,y=140,width=708,height=130)


        # DEPARTMENT
        dep_label=Label(current_course_frame,text='Department',font=("times new roman", 12,"bold"),bg="white")
        dep_label.grid(row=0,column=0,padx=10)

        dep_combo=ttk.Combobox(current_course_frame,textvariable=self.var_dep,font=("times new roman", 12,"bold"),state="readonly",width=17)
        dep_combo["values"]=("Select Department", "CSE", "IT", "CIVIL", "MECH")
        dep_combo.current(0)
        dep_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)



        # COURSE
        course_label=Label(current_course_frame,text='Course',font=("times new roman", 12,"bold"),bg="white")
        course_label.grid(row=0,column=2,padx=10,sticky=W)

        course_combo=ttk.Combobox(current_course_frame,textvariable=self.var_course,font=("times new roman", 12,"bold"),state="readonly",width=17)
        course_combo["values"]=("Select Course","B.TECH", "BE")
        course_combo.current(0)
        course_combo.grid(row=0,column=3,padx=2,pady=10,sticky=W)



        # YEAR
        year_label=Label(current_course_frame,text='Year',font=("times new roman", 12,"bold"),bg="white")
        year_label.grid(row=1,column=0,padx=10,sticky=W)

        year_combo=ttk.Combobox(current_course_frame,textvariable=self.var_year,font=("times new roman", 12,"bold"),state="readonly",width=17)
        year_combo["values"]=("Select Year","I-YEAR","II-YEAR", "III-YEAR","IV-YEAR")
        year_combo.current(0)
        year_combo.grid(row=1,column=1,padx=2,pady=10,sticky=W)


        # SEMESTER
        sem_label=Label(current_course_frame,text='Semester',font=("times new roman", 12,"bold"),bg="white")
        sem_label.grid(row=1,column=2,padx=10,sticky=W)

        sem_combo=ttk.Combobox(current_course_frame,textvariable=self.var_semester,font=("times new roman", 12,"bold"),state="readonly",width=17)
        sem_combo["values"]=("Select Semester","semester-1","semester-2")
        sem_combo.current(0)
        sem_combo.grid(row=1,column=3,padx=2,pady=10,sticky=W)



        ###################--CLASS STUDENT FRAME--#####################
        class_student_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Class student information",font=("times new roman", 12,"bold"))
        class_student_frame.place(x=15,y=270,width=708,height=310)

        

        #STUDENT ID
        studentId_label=Label(class_student_frame,text='Student ID:',font=("times new roman", 12,"bold"),bg="white")
        studentId_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)
        
        studentID_entry=ttk.Entry(class_student_frame, textvariable=self.var_std_id, width=20, font=("times new roman", 12,"bold"))
        studentID_entry.grid(row=0, column=1, padx=10, pady=5, sticky=W) 


        #student name
        studname_label=Label(class_student_frame,text='Student Name:',font=("times new roman", 12,"bold"),bg="white")
        studname_label.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        studname_entry=ttk.Entry(class_student_frame, textvariable=self.var_std_name, width=20, font=("times new roman",  12, "bold"))
        studname_entry.grid(row=0, column=3, padx=10, pady=5, sticky=W)


        #Class Division
        classdiv_label=Label(class_student_frame,text='Class Division:',font=("times new roman", 12,"bold"),bg="white")
        classdiv_label.grid(row=1,column=0,padx=1,pady=5,sticky=W)

        classdiv_combo=ttk.Combobox(class_student_frame,textvariable=self.var_div,font=("times new roman", 12,"bold"),state="readonly",width=18)
        classdiv_combo["values"]=("A","B","C")
        classdiv_combo.current(0)
        classdiv_combo.grid(row=1,column=1,padx=10,pady=5,sticky=W)


        #Roll NO
        rollno_label=Label(class_student_frame,text='Roll NO:',font=("times new roman", 12,"bold"),bg="white")
        rollno_label.grid(row=1,column=2,padx=10,pady=5,sticky=W)

        rollno_entry=ttk.Entry(class_student_frame,textvariable=self.var_roll,width=20,font=("times new roman", 12,"bold"))
        rollno_entry.grid(row=1,column=3,padx=10,pady=5,sticky=W)


        #gender
        gender_label=Label(class_student_frame,text='Gender:',font=("times new roman", 12,"bold"),bg="white")
        gender_label.grid(row=2,column=0,padx=10,pady=5,sticky=W)

        gender_combo=ttk.Combobox(class_student_frame,textvariable=self.var_gender,font=("times new roman", 12,"bold"),state="readonly",width=18)
        gender_combo["values"]=("Male","Female","Other")
        gender_combo.current(0)
        gender_combo.grid(row=2,column=1,padx=10,pady=10,sticky=W)



        #date of birth
        dob_label=Label(class_student_frame,text='DOB:',font=("times new roman", 12,"bold"),bg="white")
        dob_label.grid(row=2,column=2,padx=10,pady=5,sticky=W)

        dob_entry=ttk.Entry(class_student_frame,textvariable=self.var_dob,width=20,font=("times new roman", 12,"bold"))
        dob_entry.grid(row=2,column=3,padx=10,pady=5,sticky=W)


        #email
        email_label=Label(class_student_frame,text='Email:',font=("times new roman", 12,"bold"),bg="white")
        email_label.grid(row=3,column=0,padx=10,pady=5,sticky=W)

        email_entry=ttk.Entry(class_student_frame,textvariable=self.var_email,width=20,font=("times new roman", 12,"bold"))
        email_entry.grid(row=3,column=1,padx=10,pady=5,sticky=W)


        #phone no
        phobe_label=Label(class_student_frame,text='Phone No:',font=("times new roman", 12,"bold"),bg="white")
        phobe_label.grid(row=3,column=2,padx=10,pady=5,sticky=W)

        phobe_entry=ttk.Entry(class_student_frame,textvariable=self.var_phone,width=20,font=("times new roman", 12,"bold"))
        phobe_entry.grid(row=3,column=3,padx=10,pady=5,sticky=W)


        #address
        address_label=Label(class_student_frame,text='Address:',font=("times new roman", 12,"bold"),bg="white")
        address_label.grid(row=4,column=0,padx=10,pady=5,sticky=W)

        address_entry=ttk.Entry(class_student_frame,textvariable=self.var_address,width=20,font=("times new roman", 12,"bold"))
        address_entry.grid(row=4,column=1,padx=10,pady=5,sticky=W)


        #teacher name
        teacher_label=Label(class_student_frame,text='Teacher Name:',font=("times new roman", 12,"bold"),bg="white")
        teacher_label.grid(row=4,column=2,padx=10,pady=5,sticky=W)

        teacher_entry=ttk.Entry(class_student_frame,textvariable=self.var_teacher,width=20,font=("times new roman", 12,"bold"))
        teacher_entry.grid(row=4,column=3,padx=10,pady=5,sticky=W)


        #radio Buttons
        self.var_radio1=StringVar()
        radiobtn1=ttk.Radiobutton(class_student_frame,variable=self.var_radio1,text="Take Photo sample",value="Yes")
        radiobtn1.grid(row=6,column=0)

        radiobtn2=ttk.Radiobutton(class_student_frame,variable=self.var_radio1,text="No Photo sample",value="No")
        radiobtn2.grid(row=6,column=1)


        #bbuttons frame
        btn_frame=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame.place(x=2,y=210,width=700,height=35)

        save_btn=Button(btn_frame,text="Save",command=self.add_data,width=18,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        save_btn.grid(row=0,column=0)

        update_btn=Button(btn_frame,text="Update",command=self.update_data,width=18,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        update_btn.grid(row=0,column=1)

        delete_btn=Button(btn_frame,command=self.delete_data,text="Delete",width=18,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        delete_btn.grid(row=0,column=2)

        reset_btn=Button(btn_frame,text="Reset",command=self.reset_data, width=19,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        reset_btn.grid(row=0,column=3)

        btn_frame1=Frame(class_student_frame,bd=2,relief=RIDGE,bg="white")
        btn_frame1.place(x=2,y=245,width=700,height=35)

        take_photo_sample=Button(btn_frame1,command=self.generate_dataset,text="Take Photo Sample",width=38,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        take_photo_sample.grid(row=0,column=0)

        update_photo_sample=Button(btn_frame1,text="Update Photo Sample",command=self.generate_dataset,width=38,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        update_photo_sample.grid(row=0,column=1)

       

        ##########################--RIGHT FRAME--########################
        Right_frame=LabelFrame(main_frame,bd=2,bg="white",relief=RIDGE,text="Student Details",font=("times new roman", 12,"bold"))
        Right_frame.place(x=740,y=10,width=735,height=580)

        img_right=Image.open(asset_path("student.jpg"))
        img_right=img_right.resize((720,580), Image.LANCZOS)
        self.photoimg_right = ImageTk.PhotoImage(img_right)

        f_lbl=Label(Right_frame,image=self.photoimg_right)
        f_lbl.place(x=5,y=0,width=720,height=130)

        

        ###################--SEARCH SYSTEM--#############################
        Search_frame=LabelFrame(Right_frame,bd=2,bg="white",relief=RIDGE,text="Search System",font=("times new roman", 12,"bold"))
        Search_frame.place(x=5,y=135,width=720,height=70)

        search_label=Label(Search_frame,text='Search By:',font=("times new roman", 12,"bold"),bg="red",fg="white")
        search_label.grid(row=0,column=0,padx=10,pady=5,sticky=W)

        search_combo=ttk.Combobox(Search_frame,font=("times new roman", 12,"bold"),state="readonly",width=17)
        search_combo["values"]=("Select","Roll_No","Phone_No")
        search_combo.current(0)
        search_combo.grid(row=0,column=1,padx=2,pady=10,sticky=W)

        search_entry=ttk.Entry(Search_frame,width=20,font=("times new roman", 12,"bold"))
        search_entry.grid(row=0,column=2,padx=10,pady=5,sticky=W)

        seach_btn=Button(Search_frame,text="Search",width=13,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        seach_btn.grid(row=0,column=3,padx=4)

        showAll_btn=Button(Search_frame,command=self.fetch_data,text="Show All",width=12,font=("times new roman", 12,"bold"),bg="blue",fg="white")
        showAll_btn.grid(row=0,column=4,padx=4)


        ####################--TABLE FRAME--#######################
        table_frame=Frame(Right_frame,bd=2,bg="white",relief=RIDGE)
        table_frame.place(x=5,y=210,width=720,height=340)

        scroll_x=ttk.Scrollbar(table_frame,orient=HORIZONTAL)
        scroll_y=ttk.Scrollbar(table_frame,orient=VERTICAL)

        self.student_tab1=ttk.Treeview(table_frame,columns=("dep","course","year","sem","id","name","div","roll","gender","dob","email","phone","address","teacher","photo"),xscrollcommand=scroll_x.set,yscrollcommand=scroll_y.set)

        scroll_x.pack(side=BOTTOM,fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)
        scroll_x.config(command=self.student_tab1.xview)
        scroll_y.config(command=self.student_tab1.yview)

        #######################--HEADINGS--####################
        self.student_tab1.heading("dep",text="Department")
        self.student_tab1.heading("course",text="Course")
        self.student_tab1.heading("year",text="Year")
        self.student_tab1.heading("sem",text="Semester")
        self.student_tab1.heading("id",text="StudentId")
        self.student_tab1.heading("name",text="Name")
        self.student_tab1.heading("div",text="Division")
        self.student_tab1.heading("roll",text="Roll No")
        self.student_tab1.heading("gender",text="Gender")
        self.student_tab1.heading("dob",text="DOB")
        self.student_tab1.heading("email",text="Email")
        self.student_tab1.heading("phone",text="Phone")
        self.student_tab1.heading("address",text="Address")
        self.student_tab1.heading("teacher",text="Teacher")
        self.student_tab1.heading("photo",text="PhotoSampleStatus")
        self.student_tab1["show"]="headings"

        self.student_tab1.column("dep",width=100)
        self.student_tab1.column("course",width=100)
        self.student_tab1.column("year",width=100)
        self.student_tab1.column("sem",width=100)
        self.student_tab1.column("id",width=100)
        self.student_tab1.column("name",width=100)
        self.student_tab1.column("div",width=100)
        self.student_tab1.column("roll",width=100)
        self.student_tab1.column("gender",width=100)
        self.student_tab1.column("dob",width=100)
        self.student_tab1.column("email",width=100)
        self.student_tab1.column("phone",width=100)
        self.student_tab1.column("address",width=100)
        self.student_tab1.column("teacher",width=100)
        self.student_tab1.column("photo",width=100)

        self.student_tab1.pack(fill=BOTH, expand=1)
        self.student_tab1.bind("<ButtonRelease>", self.get_cursor)
        self.fetch_data()
        

##########################--MAIN--######################
if __name__ == "__main__":
    root=Tk()
    obj = Student(root) 
    root.mainloop()