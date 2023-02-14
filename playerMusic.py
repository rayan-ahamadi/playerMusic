from tkinter import *
import tkinter.ttk as ttk
from ttkthemes import ThemedTk
from pygame import mixer
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from tkinter import messagebox
import shutil
import pygame
import os

mixer.init()

repertoireMusic = os.listdir("music")
indexMusic = 0
adresseMusic = "music/" + repertoireMusic[indexMusic]
musique = mixer.music.load(adresseMusic)
volume = 0.9921875
isEnBoucle = False


#Informer le lecteur de mettre une musique en boucle avant le commancement de celle-ci
def enBoucle(): 
    global isEnBoucle
    isEnBoucle = True

#Informer le lecteur de ne plus mettre les musiques en boucle avant le commancement de celle-ci
def desacEnBoucle(): 
    global isEnBoucle
    isEnBoucle = False

#Fonction pour baisser le volume de 0,1
def moinsVolume():
    global textVolume
    global volume 

    if volume > 0 : 
        volume -= 0.1
        textVolume = "Niveau du volume :" + str(volume)
        nvVolume.config(text=textVolume)
        pygame.mixer.music.set_volume(volume)
    else:
        return 0

#Fonction pour augmenter le volume de 0,1
def plusVolume():
    global textVolume
    global volume 
    if volume < 1 : 
        volume += 0.1
        textVolume = "Niveau du volume :" + str(volume)
        nvVolume.config(text=textVolume)
        pygame.mixer.music.set_volume(volume)
    else : 
        return 0

#Logique pour le bouton selection
#Lance une autre musique dans la listbox après appuie sur le bouton "selectionner"
def selectSong(selected): 
    global indexMusic
    global adresseMusic
    global musique
    global repertoireMusic

    adresseMusic = "music/" + repertoireMusic[selected]
    musique = mixer.music.load(adresseMusic)
    playbutton.config(text="Pause")
    indexMusic = repertoireMusic.index(str(repertoireMusic[selected]))
    print(indexMusic)
    if isEnBoucle:
            mixer.music.play(-1)
    else:
            mixer.music.play()
            

       
    
#Logique pour le bouton Start/Pause/Resume(reprendre)
def playsong():
    if playbutton.cget('text') == "Start":
        if isEnBoucle:
            mixer.music.play(-1)
            playbutton.config(text="Pause")
        else:
            mixer.music.play()
            playbutton.config(text="Pause")
    elif playbutton.cget('text') == "Pause": 
        mixer.music.pause()
        playbutton.config(text="Resume")
    elif playbutton.cget('text') == "Resume":
        mixer.music.unpause()
        playbutton.config(text="Pause")



    
#Aller une musique en avant
def next():
    global indexMusic
    global adresseMusic
    global musique
    global isEnBoucle
    if indexMusic < len(repertoireMusic):
        indexMusic +=1
        adresseMusic = "music/" + repertoireMusic[indexMusic]
        musique = mixer.music.load(adresseMusic)
        if isEnBoucle : 
            mixer.music.play(-1)
        else:
            mixer.music.play()
        playbutton.config(text="Pause")
        playlist.select_clear(0,END)
        playlist.select_set(indexMusic) 
        print(indexMusic)
    else : 
        return 0

#Aller une musique en arrière
def previous():
    global indexMusic
    global adresseMusic
    global musique
    global isEnBoucle

    if indexMusic >= 0:
        indexMusic -=1
        adresseMusic = "music/" + repertoireMusic[indexMusic]
        musique = mixer.music.load(adresseMusic)
        if isEnBoucle : 
            mixer.music.play(-1)
        else:
            mixer.music.play()
        playbutton.config(text="Pause")
        playlist.select_clear(0,END)   
        playlist.select_set(indexMusic)  
        print(indexMusic)
    else: 
        return 0

 
    
#Fenêtre pour ajouter une musique 
def openFile(): 
    global playlist
    global repertoireMusic
    fichier = filedialog.askopenfile()
    source = fichier.name
    print(source)
    destination = "music/"
    shutil.copy(source,destination)
    repo = os.listdir("music")

    #supprime les items de la list box 
    #et remet les nouveaux éléments du dossier music
    playlist.delete(0,END)
    i=0
    for musique in repo:
        playlist.insert(i,musique)
        i+=1
    playlist.select_set(0)
    repertoireMusic = repo

#Fenêtre pour supprimer une musique 
def deleteMusique():
    global repertoireMusic
    deleteWindow = Toplevel(window)
    row = 0 
    
    def delMusic(musique): 
        print(repertoireMusic)
        msg="êtes-vous sûr de supprimer la musique : " + musique
        if messagebox.askyesno(title="Confirmation", message=msg):
            path = 'music\\' + str(musique) 
            os.remove(path)
            idx = repertoireMusic.index(musique)
            repertoireMusic.remove(musique)
            playlist.delete(idx)
            deleteWindow.destroy()
            deleteMusique()
        else:
            return 0

    for musique in repertoireMusic: 
        Label(deleteWindow,text=musique).grid(row=row,column=0,pady=10,padx=10)
        i= Button(deleteWindow,text="supprimer",command= lambda musique=musique: delMusic(musique)).grid(row=row,column=1,pady=10,padx=10)
        row+=1


#Paramètres de la fenêtre
window = ThemedTk(theme="equilux")
window.geometry('250x400')
window.configure(bg='lightgreen')
window.title('Musicplayer')
window.iconbitmap("logo.ico")
###########Contenu de la fenêtre############
playbutton=ttk.Button(window,text='Start',command=playsong)
playbutton.grid(column=1,row=0)

pistePrecedente = ttk.Button(window,text="<---",command=previous)
pistePrecedente.grid(column=0,row=0)

pisteSuivante = ttk.Button(window,text="--->",command=next)
pisteSuivante.grid(column=2,row=0)

playlist = Listbox(window)
playlist.grid(row=1,column=0,columnspan=3,ipady=20,ipadx=50)

select = ttk.Button(window,text="Selectionner",command= lambda : selectSong(playlist.curselection()[0]))
select.grid(row=2,column=1,pady=1)

volumeMoins = Button(window,text="-",command=moinsVolume) 
volumePlus = Button(window,text="+",command=plusVolume)
textVolume = "Niveau du volume :" + str(volume)
nvVolume = Label(window,text=textVolume,font=('Arial',6))

ttk.Label(window,text="Volume :").grid(row=3,column=0)
volumeMoins.grid(row=3,column=1,pady=5)
volumePlus.grid(row=3,column=2,pady=5) 
nvVolume.grid(row=4,column=0,pady=10,columnspan=2)

#Bouton pour lire en boucle 
#La fonction marche avant d'avoir choisi la musique 
yes = Radiobutton(window,text="Oui",indicatoron = 0,value=0,command= enBoucle)
no = Radiobutton(window,text="Non",indicatoron = 0,value=1,command=desacEnBoucle)
ttk.Label(window,text="En boucle :").grid(row=5,column=0)
yes.grid(row=5,column=1)
no.grid(row=5,column=2)

addFile = Button(window,text="Ajouter musiques",font=("arial",7),command=openFile)
deleteFile = Button(window,text="Supprimer musique",font=("arial",7),command=deleteMusique)
addFile.grid(row=6,column=0,pady=5,columnspan=2,padx=5)
deleteFile.grid(row=6,column=1,pady=5,columnspan=2,padx=5)


i=0
for musique in repertoireMusic:
    playlist.insert(i,musique)
    i+=1
playlist.select_set(0)



window.mainloop()




