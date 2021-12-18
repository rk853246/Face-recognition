# Libraries
from tkinter import *
from PIL import Image, ImageTk
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
import tkinter.ttk as ttk
import csv
import time

#function for Attendance sheet
def Attendance_sheet():
    root = Tk()
    root.title("Attendance Sheet")
    width = 570
    height = 400
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    root.geometry("%dx%d+%d+%d" % (width, height, x, y))
    root.resizable(0, 0)

    TableMargin = Frame(root, width=500)
    TableMargin.pack(side=TOP)
    scrollbarx = Scrollbar(TableMargin, orient=HORIZONTAL)
    scrollbary = Scrollbar(TableMargin, orient=VERTICAL)
    tree = ttk.Treeview(TableMargin, columns=("Name", "Time", "Date"), height=400, selectmode="extended",
                        yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Name', text="Name", anchor=W)
    tree.heading('Time', text="Time", anchor=W)
    tree.heading('Date', text="Date", anchor=W)
    tree.column('#0', stretch=NO, minwidth=0, width=0)
    tree.column('#1', stretch=NO, minwidth=0, width=200)
    tree.column('#2', stretch=NO, minwidth=0, width=200)
    tree.column('#3', stretch=NO, minwidth=0, width=300)
    tree.pack()

    with open('test.csv') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            S_name = row['Name']
            Time = row['Time']
            Date = row['Date']
            tree.insert("", 0, values=(S_name, Time, Date))


    if __name__ == '__main__':
        root.mainloop()

#function for Take attendance
def Take_attendace():
    Images_path = 'images'
    images = []
    studentName = []
    myList = os.listdir(Images_path)

    for current_image in myList:
        current_image_data = cv2.imread(f'{Images_path}/{current_image}')
        images.append(current_image_data)
        studentName.append(os.path.splitext(current_image)[0])
    print(studentName)

    def face_Encoding(images):
        encodeList = []
        for img in images:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        return encodeList

    def attendance(name):
        with open('test.csv', 'r+') as f:
            myDataList = f.readlines()
            nameList = []
            for line in myDataList:
                entry = line.split(',')
                nameList.append(entry[0])
            if name not in nameList:
                time_now = datetime.now()
                tStr = time_now.strftime('%H:%M:%S')
                dStr = time_now.strftime('%d/%m/%Y')
                f.writelines(f'\n{name},        {tStr},         {dStr}')

    encodeListKnown = face_Encoding(images)
    print("Complete all Encoding!!!")

    # For Camera Reading
    capture = cv2.VideoCapture(0)
    while True:
        ret, frame = capture.read()
        faces = cv2.resize(frame, None, (0, 0), 0.25, 0.25)
        faces = cv2.cvtColor(faces, cv2.COLOR_BGR2RGB)
        faces_current_frame = face_recognition.face_locations(faces)
        encode_current_frame = face_recognition.face_encodings(faces, faces_current_frame)

        for encodeface, faceLocation in zip(encode_current_frame, faces_current_frame):
            face_match = face_recognition.compare_faces(encodeListKnown, encodeface)
            face_distance = face_recognition.face_distance(encodeListKnown, encodeface)
            Match_Index = np.argmin(face_distance)

            if face_match[Match_Index]:
                name = studentName[Match_Index].upper()
                y1, x2, y2, x1 = faceLocation
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(frame, (x1, y2 - 34), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(frame, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
                attendance(name)

        cv2.imshow("Camera", frame)
        if cv2.waitKey(10) == 13:
            break

    capture.release()
    cv2.destroyAllWindows()

#Funtion For GUI

def GUI():
    root = Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.geometry("%dx%d" % (width, height))
    root.minsize(480, 480)
    root.title("FACE-RECOGNITION ATTENDANCE SYSTEM")
    img = Image.open('Bg.jpg')
    photo = ImageTk.PhotoImage(img)

    img_lable = Label(image=photo)
    img_lable.pack()

    def progress_bar():
        lable1 = Label(root, font="arist 17 bold", bg="#ffffff", )
        lable1.place(relx=0.31, rely=0.7, width=500)

        def start():
            for i in range(1, 101, 1):
                root.update_idletasks()
                lable1.config(text=str(i) + "%" + "Loading Web-Cam.....")
                time.sleep(0.11)

        start()

    frame1 = Frame(root, borderwidth=1, bg="grey", relief=SUNKEN)
    frame1.pack(pady=9)
    button1 = Button(frame1, fg="black",font="arist 12 bold", text="Take Attendance", command=lambda :[progress_bar(),Take_attendace()])
    button1.pack()

    frame2 = Frame(root, borderwidth=1, bg="grey", relief=SUNKEN)
    frame2.pack(pady=8)

    button2 = Button(frame2, fg="black",font="arist 12 bold", text="Attendance Sheet", command=Attendance_sheet)
    button2.pack()

    frame3 = Frame(root, borderwidth=1, bg="grey", relief=SUNKEN)
    frame3.pack(pady=9)

    button3 = Button(frame3, fg="black",font="arist 12 bold",text="Quit", command=root.destroy)
    button3.pack()

    root.mainloop()

GUI()





