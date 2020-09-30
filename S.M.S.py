from tkinter import *
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import pandas as pd
import matplotlib.pyplot as plt
from webdata import *
from datetime import *

l1 = [] ; l2 = [] ; l3 = []
rec = {'rno':l1,'name':l2,'marks':l3}

def bargraph(l1,l2,l3):
    rec = {'rno':l1,'name':l2,'marks':l3}
    df = pd.DataFrame(rec)
    df.to_csv('record.csv')
    print("data =",rec)

def rem():
    data = pd.read_csv("record.csv",index_col = "rno")
    data.drop(data["rno"],inplace = True)
    data.to_csv('record.csv')
    print(data)

def add_rec():
    root.withdraw()
    add.deiconify()
    ent_rno.delete(0,END)
    ent_name.delete(0,END)
    ent_marks.delete(0,END)

def update_rec():
    root.withdraw()
    update.deiconify()
    upd_entrno.delete(0,END)
    upd_entname.delete(0,END)
    upd_entmarks.delete(0,END)

def remove_rec():
    root.withdraw()
    rem.deiconify()
    rem_entrno.delete(0,END)
    
def add_stu():
    con = None
    exp = 0
    rn = ent_rno.get()
    name = ent_name.get()
    mrks = ent_marks.get()
    try:
        con = connect("student_record.db")              #database fil
        cursor = con.cursor()                           #vehicle
        if ent_rno.get() == '':
            showerror("ISSUE","Roll number should not be empty")
            con.rollback()
        else:
            if rn[0]!='-' and rn.isdigit()==False:
                exp = 1
                raise Exception
            else:
                rno = int(ent_rno.get())
                if rno <= 0:
                    showerror("ISSUE","Roll Number should contain positive integers only")
                    con.rollback()
                else:
                    if ent_name.get() == '':
                        showerror("ISSUE","name should not be empty")
                        con.rollback()
                    else:
                         if name.isalpha()==False:
                             exp = 2
                             raise Exception
                         else:
                             if len(name)<2:
                                 showerror("ISSUE","Name should contain atleast two alphabets")
                                 con.rollback()
                             else:
                                 if ent_marks.get()=='':
                                     showerror("ISSUE","Marks cannot be empty")
                                     con.rollback()
                                 else:
                                     if mrks[0]!='-' and mrks.isdigit()==False:
                                         exp = 3
                                         raise Exception
                                     else:
                                         marks = int(ent_marks.get())
                                         if marks < 0 or marks >100:
                                             showerror("ISSUE","Marks should be in between 0 to 100")
                                             con.rollback()
                                         else:
                                             sql = "insert into student_record values('%d','%s','%d')"
                                             args =(rno,name,marks)
                                             cursor.execute(sql %args)
                                             con.commit()
                                             showinfo("SUCCESS!","record inserted sucessfully")
                                             l1.append(rno)
                                             l2.append(name)
                                             l3.append(marks)
                                             bargraph(l1,l2,l3)
                                             
 
    except Exception:
        if exp == 1:
            showerror("ISSUE","Roll Number should contain digits only")
            con.rollback()
        elif exp == 2:
            showerror("ISSUE","Name should contain Alphabets only")
            con.rollback()
        elif exp == 3:
            showerror("ISSUE","Marks should contain digits only")
            con.rollback()        
                                             
    finally:
        if con is not None:
            con.close()        
        
    
def view_stu():
    root.withdraw()
    view.deiconify()
    vist_stdata.delete(1.0,END)
    con = None
    try:
        con = connect("Student_record.db")
        cursor =con.cursor()
        sql = "select * from student_record"       #select all columns from student_record
        cursor.execute(sql)    
        data = cursor.fetchall()                  #fetch all data frm table
        print(data)
        info = " "
        for d in data:
            info = info + "Roll No: "+ str(d[0]) + "  " +  "Name: "+ str(d[1]) + "   " + "Marks: "+ str(d[2]) + "\n"

        vist_stdata.insert(INSERT,info)            #to insert database file data in scrolled text window
  

    except Exception as e:
        print(e)

    finally:
        if con is not None:
            con.close()
            print("close")

def update_stu():
    con = None
    exp = 0
    rn = upd_entrno.get()
    name = upd_entname.get()
    marks = upd_entmarks.get()
    try:
        con = connect("student_record.db")              #database fil
        cursor = con.cursor()                           #vehicle        
        if upd_entrno.get() == '':
            showerror("ISSUE","Roll number cannot be empty")
            con.rollback()
        else:
            if rn[0]!='-' and rn.isdigit()==False:
                exp = 1
                raise Exception
            else:
                rno = int(upd_entrno.get())
                if rno <= 0:
                    showerror("ISSUE","Roll Number should contain positive integers only")
                    con.rollback()
                else:
                    if upd_entname.get() == '':
                        showerror("ISSUE","name cannot be empty")
                        con.rollback()
                    else:
                        if name.isalpha()==False:
                            exp = 2
                            raise Exception
                        else:
                            if len(name)<2:
                                showerror("ISSUE","Name should contain atleast two Alphabets")
                                con.rollback()
                            else:
                                sql = "update student_record set name = '%s' where rno ='%r'"
                                args = (name,rno)
                                cursor.execute(sql %args)
                                if cursor.rowcount >= 1:
                                    con.commit()
                                if upd_entmarks.get()=='':
                                    showerror("ISSUE","Marks cannot be empty")
                                    con.rollback()
                                else:
                                    if marks[0]!='-' and marks.isdigit()==False:
                                        exp = 3
                                        raise Exception
                                    else:
                                        marks = int(upd_entmarks.get())
                                        if marks < 0 or marks >100:
                                            showerror("ISSUE","Marks should range in between 0 to 100")
                                            con.rollback()
                                        else:
                                            sql = "update student_record set marks = '%d' where rno ='%r'"
                                            args = (marks,rno)
                                            cursor.execute(sql %args)
                                            if cursor.rowcount >= 1:
                                                con.commit()
                                                showinfo("SUCCESS!","record updated sucessfully")
                                                ind = l1.index(rno)
                                                l2[ind] = name
                                                l3[ind] = marks
                                                bargraph(l1,l2,l3)
                                            else:
                                                showerror("Warning!","Roll No does not exist!")
                                             
 
    except Exception:
        if exp == 1:
            showerror("ISSUE","Roll Number should contain digits only")
            con.rollback()
        elif exp == 2:
            showerror("ISSUE","Name should contain alphabets only")
            con.rollback()
        elif exp == 3:
            showerror("ISSUE","Marks should contain digits only")
            con.rollback()        
                                             
    finally:
        if con is not None:
            con.close()        

                    
def remove_stu():
    con = None
    exp = 0
    try:
        con = connect("student_record.db")
        cursor = con.cursor()
        rno = rem_entrno.get()
        if rem_entrno.get() == '':
            exp = 1
            raise Exception
        else:
            if rno[0]!='-' and rno.isdigit()==False:
                exp = 2
                raise Exception
            else:
                rno = int(rem_entrno.get())
                if rno <= 0:
                    exp = 3
                    raise Exception
                else:
                    sql = "delete from student_record where rno = '%r'"
                    args = (rno)
                    cursor.execute(sql %args)
                    if cursor.rowcount >= 1:
                        con.commit()
                        showinfo("SUCCESS!","Record Deleted Sucessfully")
                        rem()
                    else:
                        showerror("Warning!","Roll No does not exist!")
                                            
    except Exception:
        if exp == 1:
            showerror("ERROR","Roll Number should not be empty")
            con.rollback()
        if exp == 2:
            showerror("ERROR","Roll No. should contain digits only")
            con.rollback()
        if exp == 3:
            showerror("ERROR","Roll No. should contain positive integers only")
            con.rollback()

    finally:
        if con is not None:
            con.close()

def chart_stu():
    root.withdraw()
    data = pd.read_csv("record.csv")
    
    name = list(data['name'])
    marks = list(data['marks'])

    plt.bar(name , marks ,color = ["red",'blue','orange','green','cyan'])
    plt.title("Batch Information!")
    plt.xlabel("Student Name")
    plt.ylabel("Marks")
    plt.show()


def add_back():
    add.withdraw()
    root.deiconify()

def view_back():
    view.withdraw()
    root.deiconify()

def upd_back():
    update.withdraw()
    root.deiconify()

def remove_back():
    rem.withdraw()
    root.deiconify()

loc = str(loc())
temp = str(temp())
quote = str(quote())
dt = str(datetime.now())

root = Tk()

root.title("S.M.S")
root.geometry("900x620+400+100")
root.configure(background = "dark violet")

lbl_time = Label(root,text = "Date And Time: " + dt , font=('Bold Italic' , 18 ,'bold'))
lbl = Label(root , text = "Welcome To Student Management System!" , font=('Bold Italic' , 18 ,'bold'))
bt_add = Button(root , text = "ADD" , width = 10 , font=('Bold Italic' , 18 ,'bold'),command = add_rec)
bt_view = Button(root , text = "VIEW" , width = 10,font=('Bold Italic' , 18 ,'bold'),command = view_stu)
bt_update = Button(root , text = "UPDATE" , width = 10,font=('Bold Italic' , 18 ,'bold'),command = update_rec)
bt_rem = Button(root , text = "REMOVE" , width = 10,font=('Bold Italic' , 18 ,'bold'), command = remove_rec)
bt_chart = Button(root , text = "CHART" , width = 10,font=('Bold Italic' , 18 ,'bold'),command = chart_stu)
lbl_loctemp = Label(root ,text = "Location: "+loc + "  " + "Temperature: "+temp+" deg cel.",font=('Bold Italic' , 18 ,'bold'))
lbl_quote = Label(root , text = "QUOTE: "+quote, font=('Bold Italic' , 12 ,'bold'))


lbl_time.pack(pady = 10)
lbl.pack(pady = 10)
bt_add.pack(pady = 10)
bt_view.pack(pady = 10)
bt_update.pack(pady = 10)
bt_rem.pack(pady = 10)
bt_chart.pack(pady = 10)
lbl_loctemp.pack(pady = 10)
lbl_quote.pack(pady = 10)

#ADD
add = Toplevel(root)
add.title("ADD STUDENT")
add.geometry("500x400+400+100")

lbl_rno = Label(add , text = "Enter Roll No." , font=('Bold Italic' , 18 ,'bold'))
ent_rno= Entry(add , width = 50)
lbl_name = Label(add , text = "Enter Name" , font=('Bold Italic' , 18 ,'bold'))
ent_name = Entry(add , width = 50)
lbl_marks = Label(add , text = "Enter Marks" , font=('Bold Italic' , 18 ,'bold'))
ent_marks = Entry(add , width = 50)
bt_add = Button(add , text = "SAVE" , width = 10,font=('Bold Italic' , 18 ,'bold'),command = add_stu)
bt_back = Button(add , text = "BACK" , width = 10,font=('Bold Italic' , 18 ,'bold'),command = add_back)

lbl_rno.pack()
ent_rno.pack(pady = 10)
lbl_name.pack()
ent_name.pack(pady = 10)
lbl_marks.pack()
ent_marks.pack(pady = 10)
bt_add.pack(pady=20)
bt_back.pack()

add.withdraw()

#VIEW
view = Toplevel(root)
view.title("VIEW STUDENT")
view.geometry("600x500+400+100")

vist_stdata = ScrolledText(view,width=70,height=10,font=('arial',15,'bold'))
vist_btnback = Button(view,text="BACK",font=('arial',18,'bold'),command = view_back)

vist_stdata.pack()
vist_btnback.pack()

view.withdraw()

#UPDATE
update = Toplevel(root)
update.title("UPDATE STUDENT")
update.geometry("500x400+400+100")

upd_lblrno = Label(update , text = "Enter Roll No." , font=('Bold Italic' , 18 ,'bold'))
upd_entrno= Entry(update , width = 50)
upd_lblname = Label(update , text = "Enter Name" , font=('Bold Italic' , 18 ,'bold'))
upd_entname = Entry(update , width = 50)
upd_lblmarks = Label(update , text = "Enter Marks" , font=('Bold Italic' , 18 ,'bold'))
upd_entmarks = Entry(update , width = 50)
upd_btadd = Button(update , text = "SAVE" , width = 10,font=('Bold Italic' , 18 ,'bold'),command = update_stu)
upd_btback = Button(update , text = "BACK" , width = 10,font=('Bold Italic' , 18 ,'bold'),command = upd_back)

upd_lblrno.pack()
upd_entrno.pack(pady = 10)
upd_lblname.pack()
upd_entname.pack(pady = 10)
upd_lblmarks.pack()
upd_entmarks.pack(pady = 10)
upd_btadd.pack(pady=20)
upd_btback.pack()

update.withdraw()

#REMOVE

rem = Toplevel(root)
rem.title("REMOVE STUDENT")
rem.geometry("500x400+400+100")

rem_lblrno = Label(rem , text = "Enter Roll No:" , font = ("arial",18,"bold"))
rem_entrno = Entry(rem , width = 50)
rem_btremove = Button(rem , text = "REMOVE" , font = ("arial",18,"bold") , width = 10, command = remove_stu)
rem_btback = Button(rem , text = "BACK" , font = ("arial",18,"bold"), width = 10 , command = remove_back)

rem_lblrno.pack(pady=10)
rem_entrno.pack(pady=20)
rem_btremove.pack(pady=10)
rem_btback.pack(pady=10)

rem.withdraw()


root.mainloop()

