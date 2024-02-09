from function import *
from sqlite3 import *
from colorama import *
from re import *
from time import *
from datetime import *
numOfpoint = 157
def descriptionpage(DB,conn,numOfpoint,isInput):
    clearTerminal()
    PrintPoints(numOfpoint)
    EndLine(1)
    print(Fore.GREEN+Style.BRIGHT+"TimeWarden".center(numOfpoint))
    EndLine(6)
    Space(4)
    print(Fore.LIGHTBLACK_EX+"Say goodbye to missed deadlines and forgotten tasks with our comprehensive solution.\n\t\t\t\tOur platform combines the convenience of a Reminder and the power of a To-Do List\n\t\t\t\tensuring you stay on top of your schedule and tasks effortlessly.")
    EndLine(1)
    Space(4)
    print(Fore.LIGHTBLACK_EX+"With our Reminder feature, never overlook important dates, meetings, or events again.\n\t\t\t\tSet up personalized reminders for birthdays, appointments, and recurring tasks. ")
    EndLine(1)
    Space(4)
    print(Fore.LIGHTBLACK_EX+"Meanwhile, our To-Do List functionality helps you manage your tasks effectively.\n\t\t\t\tCreate, prioritize, and track your to-do items with ease.\n\t\t\t\tSet deadlines, attach relevant files or notes, and collaborate seamlessly with your team.\n\t\t\t\tOur user-friendly interface allows you to organize tasks into categories, set reminders,\n\t\t\t\tand sync across all your devices for easy accessibility.")
    EndLine(6)
    Space(4)
    print(Fore.GREEN +"Login (L)\n\t\t\t\tDon't have an account? Register now (R)")
    EndLine(1)
    Space(4)
    if isInput == True :
        print("(L)(R):",end="")
    elif isInput == False :
        print(Fore.RED+"(L)(R):",end="")
    login_account =input()
    if login_account == "l" or login_account == "L":
        loginPage(DB,conn,numOfpoint)
    elif login_account == "r" or login_account == "R":
        signupPage(DB,conn,numOfpoint)
    else:
        descriptionpage(DB,conn,numOfpoint,False)
# !-----------------------------------
def signupPage(DB,conn,numOfpoint,testMail=True,Mailexists=True):
    clearTerminal()
    PrintPoints(numOfpoint)
    EndLine(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden".center(numOfpoint))
    EndLine(6)
    Space(4)
    print(Fore.LIGHTBLACK_EX+"Create New Account")
    EndLine(1)
    if not testMail:
        Space(4)
        print(Fore.RED+"Incorrect Mail or Password")
    elif not Mailexists :
        Space(4)
        print(Fore.RED+"Your Mail Not Associated with an Account ,Create Your Acount.")
    Space(4)
    Name=input(Fore.WHITE+"First Name : ")
    EndLine(2)
    Space(4)
    lName=input(Fore.WHITE+"Last Name : ")
    EndLine(2)
    Space(4)
    birth=input(Fore.WHITE+"Date of Birth (YYYY-MM-DD): ")
    EndLine(2)
    Space(4)
    mail=input(Fore.WHITE+"Email : ")
    EndLine(2)
    Space(4)
    Password=input(Fore.WHITE+"Password : ")
    DB.execute("SELECT COUNT(*) AS CountMail FROM person WHERE mail = ?",(mail,))
    CountMail = DB.fetchone()
    if not search(r"[A-z0-9]+@[A-z]+\.[com]", mail) or len(Password)<8:
        signupPage(DB,conn,numOfpoint,testMail=False)
    elif CountMail[0] != 0:
        loginPage(DB,conn,numOfpoint,alredyExists=True)
    if search(r"[A-z0-9]+@[A-z]+\.[com]", mail) and len(Password)>= 8 and CountMail[0] ==0 :
        DB.execute("INSERT INTO person(id,fname,lname,mail,password,datebirth) VALUES (?,?,?,?,?,?)",(IdGenerator(DB),Name,lName,mail,Password,birth))
        conn.commit()
        loginPage(DB,conn,numOfpoint,newAccount=True)
#!----------------------------
def loginPage(DB,conn,numOfpoint,newAccount=False,alredyExists = False,correctPassword=True):
    clearTerminal()
    PrintPoints(numOfpoint)
    EndLine(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden".center(numOfpoint))
    EndLine(4)
    Space(4)
    print(Fore.LIGHTBLACK_EX+"Login")
    if newAccount :
        EndLine(1)
        Space(4)
        print(Fore.GREEN+"Your Account Create Successfully ✔️")
    elif alredyExists :
        EndLine(1)
        Space(4)
        print(Fore.RED+"Your Mail Already Associated with an Account")
    elif not correctPassword:
        EndLine(1)
        Space(4)
        print(Fore.RED+"Your Password Incorrect")
    else:
        EndLine(2)
    Space(4)
    mail = input(Fore.WHITE+"Mail :")
    EndLine(1)
    Space(4)
    password = input(Fore.WHITE+"Password :")
    DB.execute("SELECT COUNT(*) AS countPersonMail FROM person WHERE mail = ? ",(mail,))
    countPersonMail = DB.fetchone()
    DB.execute("SELECT COUNT(*) AS countPerson FROM person WHERE mail = ? AND password = ?",(mail,password))
    countPerson = DB.fetchone()
    if countPersonMail[0] == 0 :
        signupPage(DB,conn,numOfpoint,Mailexists=False)
    elif countPerson[0] == 0:
        loginPage(DB,conn,numOfpoint,correctPassword=False)
    else:
        DB.execute("SELECT id FROM person WHERE mail = ? AND password = ?",(mail,password))
        id = DB.fetchone()
        Reminder(DB,conn,numOfpoint,id[0])
#!-----------------------------------------------------
def Reminder(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname , lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    DB.execute("SELECT list FROM reminder WHERE id=?",(id,))
    result= DB.fetchall()
    lists=[]
    lines = 2
    for i in range(len(set(result))):
        lists.append(list(set(result))[i][0])
    for ElemList in lists :
        DB.execute("SELECT title,description,date,hour FROM reminder WHERE id = ? AND list = ?",(id,ElemList))
        reminder = DB.fetchall()
        EndLine(1)
        lines+=2
        Space(1)
        today = 0
        for i in range(len(reminder)):
            if CompareDate(reminder[i][2]):
                today +=1
        if today!=0:
            print(Fore.CYAN+ElemList)
        for i in range(len(reminder)):
            if CompareDate(reminder[i][2]) and today!=0:
                Space(2)
                print(Fore.LIGHTBLACK_EX+reminder[i][0])
                Space(2)
                print(Fore.WHITE+reminder[i][2] ," ",reminder[i][3])
                result = create_paragraphs(reminder[i][1],120)
                lines+=(calculate_num_lines(''.join(result))+3)
                print(Fore.BLUE)
                for ele in result:
                    Space(2)
                    print(ele)

    _ , terminal_height = shutil.get_terminal_size()
    EndLine((terminal_height - lines - 9))
    PrintPoints(numOfpoint)
    print("N: NOTE | T:TO-DO | A: ADD REMINDER | L: LOG OUT")
    PrintPoints(numOfpoint)
    action = input(">")
    if(action=="A" or action =="a"):
        addreminder(DB,conn,numOfpoint,id)
    if(action=="L" or action =="l"):
        loginPage(DB,conn,numOfpoint)
    if(action=="N" or action =="n"):
        Note(DB,conn,numOfpoint,id)
    if(action=="T" or action =="t"):
        TodoPage(DB,conn,numOfpoint,id)
    
def addreminder(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname , lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    EndLine(3)
    Space(5)
    print(Fore.BLUE+"ADD NEW REMINDER")
    EndLine(1)
    Space(5)
    title=input(Fore.WHITE+"title :")
    EndLine(1)
    Space(5)
    liste=input("list :")
    EndLine(1)
    Space(5)
    description=input("description :")
    EndLine(1)
    Space(5)
    date=input("date :")
    EndLine(1)
    Space(5)
    hour=input("hour :")
    DB.execute("INSERT INTO reminder(id,title,description,list,date,hour) VALUES(?,?,?,?,?,?)",(id,title,description,liste,date,hour))
    conn.commit()
    Reminder(DB,conn,numOfpoint,id)
def Note(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname , lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    lines=2
    EndLine(3)
    lines+=4
    DB.execute("SELECT title, note, date FROM notes WHERE id=?", (id,))
    result = DB.fetchall()
    for i in range(len(result)):
        print("\n")
        lines+=1
        Space(4)
        print(Fore.LIGHTBLACK_EX+result[i][0],end='')
        lines+=1
        Space(10)
        print(Fore.YELLOW+result[i][2])
        lines+=1
        aligne = create_paragraphs(result[i][1],120)
        print(Fore.BLUE)
        lines+=(calculate_num_lines(''.join(aligne)))
        for ele in aligne:
            Space(5)
            print(ele)
    _ , terminal_height = shutil.get_terminal_size()
    EndLine((terminal_height - lines - 9))
    PrintPoints(numOfpoint)
    print("R: REMINDER | T:TO-DO | A: ADD NOTE | L: LOG OUT")
    PrintPoints(numOfpoint)
    action = input(">")
    if(action=="A" or action =="a"):
        addnote(DB,conn,numOfpoint,id)
    if(action=="L" or action =="l"):
        loginPage(DB,conn,numOfpoint)
    if(action=="R" or action =="r"):
        Reminder(DB,conn,numOfpoint,id)
    if(action=="T" or action =="t"):
        TodoPage(DB,conn,numOfpoint,id)
    else:
        Note(DB,conn,numOfpoint,id)
def addnote(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname , lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    EndLine(3)
    Space(5)
    print(Fore.BLUE+"ADD NEW NOTE")
    EndLine(1)
    Space(5)
    title=input(Fore.WHITE+"title : ")
    EndLine(1)
    Space(5)
    note=input("note : ")
    date = datetime.now().date()
    DB.execute("INSERT INTO notes(id, title, note, date) VALUES (?, ?, ?, ?)", (id, title, note, date))
    conn.commit()
    Note(DB,conn,numOfpoint,id)
def TodoPage(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname , lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    DB.execute("SELECT title,description FROM todo WHERE id=? AND completed=?",(id,"false"))
    result= DB.fetchall()
    EndLine(4)
    lines = 5
    for i in range(len(result)):
        Space(2)
        print(Fore.BLUE,"   ",result[i][0])
        text = create_paragraphs(result[i][1],120)
        lines+=(calculate_num_lines(''.join(text))+3)
        for ele in text:
            Space(3)
            print(Fore.WHITE+ele)
        EndLine(1)
        lines+=1
    _ , terminal_width = shutil.get_terminal_size()
    EndLine((terminal_width - lines - 9))
    PrintPoints(numOfpoint)
    print("  N:Notes | R:Reminder | A:Add ToDo | C:completed ToDo | D:Make it Done | L:Logout")
    PrintPoints(numOfpoint)
    action = input(">")
    if(action == 'L' or action == 'l'):
        descriptionpage(DB,conn,numOfpoint,True)
    elif(action == 'R' or action == 'r'):
        Reminder(DB,conn,numOfpoint,id)
    elif(action == 'A' or action == 'a'):
        addTodo(DB,conn,numOfpoint,id)
    elif(action == 'c' or action == 'C'):
        completedTodo(DB,conn,numOfpoint,id)
    elif(action == 'd' or action == 'D'):
        makeItDone(DB,conn,numOfpoint,id)
    elif(action == 'N' or action == 'n'):
        Note(DB,conn,numOfpoint,id)
    else:
        TodoPage(DB,conn,numOfpoint,id)
    
def makeItDone(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname,lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    Space(3)
    print(Fore.BLUE,"Make it done")
    EndLine(3)
    Space(3)
    print(Fore.WHITE,end="")
    title = input("Title :")
    DB.execute("UPDATE todo SET completed=? WHERE id = ? AND title = ?",('true',id,title))
    conn.commit()
    Reminder(DB,conn,numOfpoint,id)
def completedTodo(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname , lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    DB.execute("SELECT title,description FROM todo WHERE id=? AND completed=?",(id,"true"))
    result= DB.fetchall()
    EndLine(4)
    lines = 5
    for i in range(len(result)):
        Space(2)
        print(Fore.BLUE,"   ",result[i][0])
        text = create_paragraphs(result[i][1],120)
        lines+=(calculate_num_lines(''.join(text))+3)
        for ele in text:
            Space(3)
            print(Fore.WHITE+ele)
        EndLine(1)
        lines+=1
    _ , terminal_height = shutil.get_terminal_size()
    EndLine((terminal_height - lines - 9))
    PrintPoints(numOfpoint)
    print("  N:NOTE | R:REMINDER | A:ADD TO DO | C:TODO | L:LOG OUT")
    PrintPoints(numOfpoint)
    action = input(">")
    if(action == 'L' or action == 'l'):
        descriptionpage(DB,conn,numOfpoint,True)
    elif(action == 'R' or action == 'r'):
        Reminder(DB,conn,numOfpoint,id)
    elif(action == 'A' or action == 'a'):
        addTodo(DB,conn,numOfpoint,id)
    elif(action == 'c' or action == 'C'):
        TodoPage(DB,conn,numOfpoint,id)
    else:
        completedTodo(DB,conn,numOfpoint,id)
def addTodo(DB,conn,numOfpoint,id):
    clearTerminal()
    PrintPoints(numOfpoint)
    DB.execute("SELECT fname,lname FROM person WHERE id = ?",(id,))
    FullName = DB.fetchall()
    Space(1)
    print(Style.BRIGHT+Fore.GREEN+"TimeWarden",end="")
    Space(14)
    print(FullName[0][0],FullName[0][1])
    Space(3)
    print(Fore.BLUE,"Add New To-Do")
    EndLine(3)
    Space(3)
    print(Fore.WHITE,end="")
    title = input("Title :")
    EndLine(2)
    Space(3)
    description = input("Description :")
    DB.execute("INSERT INTO todo(id,title,description,completed) VALUES (?,?,?,?)",(id,title,description,'false'))
    conn.commit()
    Reminder(DB,conn,numOfpoint,id)
    
    
        
        



# ! ---------------------------------------------------
if __name__ == "__main__":
    conn = connect("database.db")
    DB = conn.cursor()
    DB.execute("CREATE TABLE IF NOT EXISTS person(id INTEGER,fname STRING,lname STRING,mail STRING ,password STRING ,datebirth DATE)")
    DB.execute("CREATE TABLE IF NOT EXISTS reminder(id INTEGER,title STRING,description STRING,list STRING ,date DATE ,hour STRING)")
    DB.execute("CREATE TABLE IF NOT EXISTS todo(id INTEGER,title STRING,description STRING,completed STRING )")
    DB.execute("CREATE TABLE IF NOT EXISTS notes(id INTEGER,title STRING,note STRING, date DATE)")
    delete(DB,conn)
    descriptionpage(DB,conn,numOfpoint,True)
   