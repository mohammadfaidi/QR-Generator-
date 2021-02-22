from tkinter import *
from tkinter import messagebox
import pyqrcode
import os
from tkinter import simpledialog
import mysql.connector
import cv2
import cryptography
from cryptography.fernet import Fernet

#import png
import png
from PIL import Image
#pip install qrcode[pil]
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="qrcode2"
)
mycursor = mydb.cursor()
window = Tk()
window.title("QR Code Generator")


key = Fernet.generate_key()
file = open('key.key', 'wb')  # Open the file as wb to write bytes
file.write(key)  # The key is type bytes still
file.close()


# coed generation
def generate():

    if len(Task.get()) != 0:
        global encToString
        global myQr
        file = open('key.key', 'rb')  # Open the file as wb to read bytes
        key2 = file.read()  # The key will be type bytes
        file.close()
        message=Task.get().encode()
        f = Fernet(key2)
        encrypted = f.encrypt(message)
        encToString = encrypted.decode()
        myQr = pyqrcode.create(encToString)
        print(encToString)

        qrImage = myQr.xbm(scale=6)
        global photo
        photo = BitmapImage(data=qrImage)
    else:
        messagebox.showinfo("Error!", "Please Enter The Task")
    try:
        showCode()
    except:
        pass


# code showing
def showCode():
    global photo
    notificationLabel.config(image=photo)
    #subLabel.config(text="Showing QR Code for: " + Task.get())
    subLabel.config(text="Showing QR Code for: " + encToString)

'''
def save():
    #if len(Task.get()) != 0:
        # qrImage = myQr.png(os.path.join(dir, Task.get() + ".png"), scale=6) # myQr.
        #myQr.save("qr.jpg")
      #  print("Entre image name to save")
       # n = "qrcode"
        #d = n + ".png"
        #myQr.show()
        #myQr.png(d, scale=6)
        qrImage = myQr.png((Task.get() + ".png"), scale=6)
        print("Done")
    # folder to save all the codes
    #dir = path1 = os.getcwd() + "\\QR Codes"

    # create a folder is it doesn't exist
    #if not os.path.exists(dir):
     #   os.makedirs(dir)

    #try:


     #   else:
      #      messagebox.showinfo("Error!", "File name can not be empty!")
    #except:
     #   messagebox.showinfo("Error!", "Please generate the code first")


'''


def save():
    # folder to save all the codes
    dir = path1 = os.getcwd() + "\\QR Codes"

    # create a folder is it doesn't exist
    if not os.path.exists(dir):
        os.makedirs(dir)

    try:
        if len(Task.get()) != 0:
            qrImage = myQr.png(os.path.join(dir, Task.get() + ".png"), scale=6)
        else:
            messagebox.showinfo("Error!", "File name can not be empty!")
    except:
        messagebox.showinfo("Error!", "Please generate the code first")


def bk():
    print("ID: %s\nTask: %s" % (ID.get(), encToString))
    # print(e1.get())
    # print(e2.get())
    sql = "INSERT INTO qr (ID, TASK) VALUES (%s, %s)"
    # num = int(input("Enter your Identical Number: "))
    # mesg = input("give him a task:")
    # generate_key()
    # enc = encrypt_message(mesg)
    val = (ID.get(), encToString)
    mycursor.execute(sql, val)

    mydb.commit()

def display():
    print("Hello")
    mycursor.execute("SELECT * FROM qr ")
    myresult = mycursor.fetchall()
    File = simpledialog.askstring(title="Test",
                                      prompt="Save file  ?:")
    f = open(File+""+".txt", "w")
    for x in myresult:
        # print(x[1])
        # Task=x[1]
        print(x)
        a,b,c=x
        #print(str(a))
        #print(b)
        #print(c)
        #array = []
        #for item in len(x):
         #   array.extend(item)

        #joined_string = "".join(x)
        f.write("Index: "+ " " + str(a) +"ID: "  +" "+ b + " Task:" + " " +c +"\n")

       #print(type(x))
    f.close()


def scan():
    file = open('key.key', 'rb')  # Open the file as wb to read bytes
    key2 = file.read()  # The key will be type bytes
    file.close()
    #d = cv2.QRCodeDetector()
    #val, points, straight_qrcode = d.detectAndDecode(cv2.imread("QR Codes/kill rashiq.png"))
    #print(val)
    USER_INP = simpledialog.askstring(title="Test",
                                      prompt="Name Qr Code  ?:")

    # check it out
    print("The decryption:", USER_INP)
    d = cv2.QRCodeDetector()
    #val, points, straight_qrcode = d.detectAndDecode(cv2.imread("QR Codes/"+USER_INP+".png"))
    val, points, straight_qrcode = d.detectAndDecode(cv2.imread("QR Codes/" + USER_INP))
    decryToByte = val.encode()
    f = Fernet(key2)
    decrypted = f.decrypt(decryToByte)
    print(decrypted)

#LABEL ID
lab1 = Label(window, text="ID", font=("Helvetica", 12))
lab1.grid(row=0, column=0, sticky=N + S + E + W)

#LABEL Task

lab2 = Label(window, text="Task", font=("Helvetica", 12))
lab2.grid(row=1, column=0, sticky=N + S + E + W)

#Entry ID
ID = StringVar()
idEntry = Entry(window, textvariable=ID, font=("Helvetica", 12))
idEntry.grid(row=0, column=1, sticky=N + S + E + W)

#Entry Task
Task = StringVar()
taskEntry = Entry(window, textvariable=Task, font=("Helvetica", 12))
taskEntry.grid(row=1, column=1, sticky=N + S + E + W)



createButton = Button(window, text="Create QR Code", font=("Helvetica", 12), width=15, command=generate)
createButton.grid(row=0, column=3, sticky=N + S + E + W)

notificationLabel = Label(window)
notificationLabel.grid(row=2, column=1, sticky=N + S + E + W)

subLabel = Label(window, text="")
subLabel.grid(row=3, column=1, sticky=N + S + E + W)

showButton = Button(window, text="BackUp", font=("Helvetica", 12), width=15, command=bk)
showButton.grid(row=1, column=3, sticky=N + S + E + W)

showButton = Button(window, text="SaveQR", font=("Helvetica", 12), width=15, command=save)
showButton.grid(row=3, column=3, sticky=N + S + E + W)

showButton = Button(window, text="ReadBackup", font=("Helvetica", 12), width=15, command=display)
showButton.grid(row=4, column=3, sticky=N + S + E + W)

showButton = Button(window, text="ScanQR", font=("Helvetica", 12), width=15, command=scan)
showButton.grid(row=5, column=3, sticky=N + S + E + W)

# Making responsive layout:
totalRows = 5
totalCols = 5

for row in range(totalRows + 1):
    window.grid_rowconfigure(row, weight=1)

for col in range(totalCols + 1):
    window.grid_columnconfigure(col, weight=1)

# looping the GUI
window.mainloop()