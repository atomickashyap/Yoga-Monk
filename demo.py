"""Quick demo."""
# video path: C:\Users\Ankit Yadav\Desktop\Toycathon\YogaMonk\Yoga_Monk\video\video.mp4


from video_processing import process_video
from sys import argv
from pathlib import Path
from tkinter import *
from tkinter.messagebox import showinfo
import time
import pygame
import pyttsx3
from PIL import ImageTk, Image


pygame.init()
pygame.mixer.init()
pygame.mixer.music.load("C:/Users/admin/Desktop/Yoga_Monk_Demo/Yoga_Monk_Day2testme/audio/OM.mp3")
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play()




ws = Tk()
ws.title("Yoga Monk")
ws.geometry('1000x800')
ws['bg'] = '#ffbf00'
Label(ws, text=f'Welcome to Yoga Monk', pady=20, bg='#ffbf00').pack(side = 'top')

canvas = Canvas(ws, width = 770, height = 433)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("yoga2.jpg"))  
canvas.create_image(0, 0, anchor=NW, image=img)


pname = "Aman"
pAge = 21
pProblem = "Back Pain"

def printValue():
    global pname, pAge, pProblem
    pname = player_name.get()
    pAge = player_age.get()
    pProblem = player_problem.get()
    print("Name: " + pname)
    print("Age: " + pAge)
    print("Medical Conditions: " + pProblem)
    Label(ws, text=f'{pname}, Registered!', pady=20, bg='#ffbf00').pack()
    if(pname != ''):
        time.sleep(1)
        ws.destroy()

Label(ws, text=f'Your Name: ', pady=0, bg='#ffbf00').pack()



player_name = Entry(ws)
player_name.pack(pady = 0)


Label(ws, text=f'Your Age: ', pady=0, bg='#ffbf00').pack()
player_age = Entry(ws)
player_age.pack(pady = 0)

Label(ws, text=f'Any Medical Condition (for e.g Back Pain): ', pady=0, bg='#ffbf00').pack()
player_problem = Entry(ws)
player_problem.pack(pady = 0)


Button(ws,text="", bg = '#ffbf00', padx=10, pady=5, highlightthickness=0, bd=0).pack()

Button(ws,text="Register Player", padx=10, pady=5,command=printValue).pack()


ws.mainloop()




top = Tk()
top.title("Yoga Monk")

width = 1000
height = 800

top['bg'] = '#ffbf00'

top.geometry(str(width) + "x" + str(height))

Label(top, text=f'Welcome to Yoga Monk', pady=20, bg='#ffbf00').pack(side = 'top')

canvas = Canvas(top, width = 770, height = 433)  
canvas.pack()  
img = ImageTk.PhotoImage(Image.open("yoga2.jpg"))  
canvas.create_image(0, 0, anchor=NW, image=img)


Label(top, text=f'Hello, {pname}', pady=20, bg='#ffbf00').pack(side = 'top')




def func1():
    top2 = Tk()
    top2.title("Yoga Monk")
    top2.geometry('600x400')
    top2['bg'] = '#ffbf00'


    Label(top2, text=f'Welcome to Yoga Monk', font=("Arial", 25), bg='#ffbf00').pack(side = 'top')

    str40 = "According to your age and medical conditions, \nThese are the recommended Asans for you: \n1) Easy Pose ( 15 seconds)\n2) Child Pose( 15 seconds)\n3) High Plank (15 seconds)\n4) Standing Forward Bend (15 seconds)\n5) Cobra Pose (15 seconds)\n6) Cat Pose (15 seconds)\n7) Cow Pose(15 seconds)\n8) High Plank (15 seconds)"
    str401 = "According to your age and medical conditions, \nThese are the recommended Asans for you: \n1) Easy Pose ( 15 seconds)\n2) Child Pose( 15 seconds)\n) "
    str39 = "According to your age and medical conditions, \nThese are the recommended Asans for you: \n1) Easy Pose ( 15 seconds)\n2) Happy Baby Pose ( 15 seconds)"

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')       #getting details of current voice
    engine.setProperty('voice', voices[1].id)   #changing index, changes voices. 1 for female


    if(int(pAge) < 40 and pProblem != "Back Pain"):
        Label(top2, text=f'{str40}', font=("Arial Italic", 18), anchor="w", bg='#ffbf00').pack(side= TOP)
        
        engine.say(str401)  
        #play the speech  
        engine.runAndWait()

    else:
        Label(top2, text=f'{str39}' , font=("Arial Italic", 18), anchor="w", bg='#ffbf00').pack(side= TOP)
        engine.say(str39)  
        #play the speech  
        engine.runAndWait()
        
    process_video(0, fps=3, model_choice='rf', show_video=True)
    top2.mainloop()

   

def func2():
    path = "C:/Users/admin/Desktop/Yoga_Monk_Demo/Yoga_Monk_Day2testme/Video/Video3.mp4"
    print("Path: " + path)
    filename = Path(path)
    # filename = Path(input("Specify video file path. "))
    process_video(str(filename.resolve()), fps=3, model_choice=model, show_video=True)



if __name__ == "__main__":
    print("Yoga Monk Demo.")
   
    if len(argv) == 1:
        model = "rf"

        b1 = Button(top, text="WebCam", command=func1, activeforeground="red",
            activebackground="pink", pady=10, padx=180)
        b2 = Button(top, text="Video", command=func2, activeforeground="blue",
            activebackground="pink", pady=10, padx=180)

        b1.place(x=50, y=550)
        b2.place(x=550, y =550)

        top.mainloop()
        # while model not in ["nn", "rf"]:
        #     model = input("Random forest [rf] or Forward-feeding NN [nn]? ")

        # method = ""
        # while method not in ["w", "v"]:
        #     method = input("[w]ebcam or [v]ideo file? ")
        # if method == "w":
        #     process_video(0, fps=3, model_choice=model, show_video=True)
        # elif method == "v":
        #     filename = Path(input("Specify video file path. "))
        #     if filename.exists():
        #         process_video(
        #             str(filename.resolve()), fps=3, model_choice=model, show_video=True
        #         )
        #     else:
        #         f"File {filename} does not exist."
