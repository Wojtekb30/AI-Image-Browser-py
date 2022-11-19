from tkinter import *  
from PIL import ImageTk,Image
import PIL
import tkinter as tk #import tkinter, I do it under name tk because it's easier to type
global wysz
from tkinter import filedialog
from imageai.Classification import ImageClassification
import pathlib
from pathlib import Path
import os
import pickle
import hashlib
global root
global imgnum


def choosepath():

    masterpath = filedialog.askdirectory()
    file = open("masterpath.data", "w")
    file.write(masterpath)
    file.close()
    res = []
    plikitab = []
    shatab = []
    tagjeden = []
    tagdwa = []
    for path in os.listdir(masterpath):
    # check if current path is a file
        if os.path.isfile(os.path.join(masterpath, path)):
            res.append(path)
    n=0
    while n<len(res):
        rozszerzenie = pathlib.Path(masterpath+"/"+res[n]).suffix
        print(masterpath+"/"+res[n])
        if (str(rozszerzenie).lower()==".jpg" or str(rozszerzenie).lower()==".png"):
            print(res[n])
            plikitab.append(res[n])
            with open(masterpath+"/"+res[n],"rb") as fa: #sha generate
                filetosha = fa.read()
                resultsha = hashlib.sha256(filetosha)
                shatab.append(resultsha.hexdigest())
            with open('filenames.pkl', 'wb') as f: #savenames
                pickle.dump(plikitab, f)
                f.close()
            with open('sha.pkl', 'wb') as f: #saveshas
                pickle.dump(shatab, f)
                f.close()
            prediction = ImageClassification()
            prediction.setModelTypeAsInceptionV3()
            prediction.setModelPath("inception-ai-model.h5")
            prediction.loadModel()    
            predictions, percentage_probabilities = prediction.classifyImage(masterpath+"/"+res[n], result_count=5)
            if percentage_probabilities[0]>10:
                tagjeden.append(str(predictions[0]))
            else:
                tagjeden.append("picture")
            if percentage_probabilities[1]>10:
                tagdwa.append(str(predictions[1]))
            else:
                tagdwa.append("picture")
        n=n+1
    with open('tagjeden.pkl', 'wb') as f: #savenames
        pickle.dump(tagjeden, f)
        f.close()
    with open('tagdwa.pkl', 'wb') as f: #saveshas
        pickle.dump(tagdwa, f)
        f.close()
    print("done")
    
    
def rescan():
    print('a')
    
def nextpic():
    global wyszukiwarka
    wyszukiwaniee = wyszukiwarka.get("1.0",'end-1c') #Dodaj wyszukiwanie!!!!!!!!!!! 
    global imgnum                           #dodaj quick refresh!!!!!!!!!!
    global root
    filelist = []
    tagsuno = []
    tagsunow = []
    if wyszukiwaniee == "":
        with open('filenames.pkl', 'rb') as f:
            filelist = pickle.load(f)
            f.close()
        imgnum = imgnum + 1
        if imgnum+1>len(filelist):
            imgnum = 0
        print(imgnum)
    else:
        with open('tagjeden.pkl', 'rb') as f:
            tagsuno = pickle.load(f)
            f.close()
        for index in range(len(tagsuno)):
            if wyszukiwaniee.lower() in tagsuno[index].lower():
                imgnum = index
    root.destroy()
    mainwindow()
    
    

imgnum = 0
filenamelist = []


def mainwindow():
    global root
    global wysz
    root = tk.Tk() #create a window. You can call it however you want, but most programmers name it root
    root.title("AI Img") #set window title
    root.geometry('650x750') #set size of window
    buttonchoose = tk.Button(root, text="Choose photo folder and scan (resets everything)", command=choosepath) 
    buttonchoose.pack() #render it
    buttonscan = tk.Button(root, text="Quick rescan", command=rescan) 
    buttonscan.pack() #render it
    global wyszukiwarka
    wyszukiwarka = tk.Text(root, height = 1, width = 40)
    wyszukiwarka.pack()
    canvas = Canvas(root, width = 600, height = 600, background='black')
    print("i"+str(imgnum))
    try:
        f = open("masterpath.data", "r")
        mainsciezka = f.read()
        f.close()
        with open('filenames.pkl', 'rb') as f:
            filenamelist = pickle.load(f)
            f.close()
        img = Image.open(mainsciezka +"/"+filenamelist[imgnum])
        img.thumbnail(size=(550,550))
        realimage = ImageTk.PhotoImage(img)
        canvas.create_image(10, 10, anchor=NW, image=realimage)
    except:
        img = Image.open('sysinfo.png')
        img.thumbnail(size=(550,550))
        realimage = ImageTk.PhotoImage(img)
        canvas.create_image(10, 10, anchor=NW, image=realimage)
    canvas.pack()
    buttonnext = tk.Button(root, text="Search | Next", command=nextpic) 
    buttonnext.pack()
    root.mainloop()
    
mainwindow()