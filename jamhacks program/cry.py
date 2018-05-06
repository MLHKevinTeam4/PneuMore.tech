import tensorflow as tf, sys
import pygame
from tkinter import filedialog as fd
from tkinter import Tk
from tkinter import *

from socket import *
import time
ip="0.0.0.0"

userinfo=["Kevin","Wang","555798983"]

RED= (255,0,0)
BLACK=(0,0,0)
WHITE= (255,255,255)
GREEN= (0,255,0)
BLUE= (0,0,255)
SKYBLUE=(122,214,245)
BEIGE= (186,111,26)
PINK=(255,0,238)
ORANGE=(255,165,0)
PEACH= (232, 135, 78)
LIGHTGREEN= (177,233,111)
GREY= (52, 54, 58)
BROWN=(86,62,38)  #Color Constants'
pygame.init()
screen = pygame.display.set_mode((1000,700))
clock = pygame.time.Clock()
bigCalibri=pygame.font.SysFont ("Calibri",30)
smallCalibri=pygame.font.SysFont("Calibri",20)
mainMenu=pygame.image.load("mainMenu.png")
fileExplorer=pygame.image.load("fileExplorer.png")
resultPage=pygame.image.load("resultPage.png")
Tk().withdraw()
state="MAINMENU"

def getVal(tup):
    for i in range(3):
        if tup[i]==1:
            return i+1
    return 0

def retrieve_input():
    global ip
    ip=input ("Input your doctor's client address.")
    return ip

def askForFile(): #returns file path selected
    filename=fd.askopenfilename()
    return filename

def imageDataReturn(imagePath): #returns image data of PATH
    image_data=tf.gfile.FastGFile(imagePath, 'rb').read()
    return image_data

def drawMainMenu():
     screen.blit(mainMenu,(0,0,1000,700))

def mainMenuCollisions(x, y, mouseButton,state):
    mouseHitRect=pygame.Rect(x,y,1,1)
    actionList=[(0,485,500,215),(500,485,500,215)]
    collide=mouseHitRect.collidelist(actionList)
    if collide != -1 and mouseButton==1:
        if collide==0:
            state="UPLOAD"
        elif collide==1:
            state="SETTINGS"
    return state

def drawFileExplorerGUI():
    screen.blit(fileExplorer, (0,0,1000,7000))
    pygame.display.flip()



def communicateAppointments(userInfo):
    global ip
    host=ip # target computer
    port = 13000
    addr = (host, port)
    UDPSock = socket(AF_INET, SOCK_DGRAM)
    data=userInfo
    UDPSock.sendto(bytes(data, 'utf_8'), addr)
    time.sleep(3)
    UDPSock.close()

def drawAnalysisScreen():
    screen.blit(resultPage,(0,0,1000,700))
    pygame.display.flip()

def drawAnslysisInfo(diagList, scoreList):
    if scoreList[0]>scoreList[1]:
        bigger=0
        smaller=1
    else:
        bigger=1
        smaller=0
    drawList=[(23,268,80,62), (23,382,80,62)]
    pygame.draw.rect(screen, GREEN, (drawList[bigger]))
    pygame.draw.rect(screen, RED,(drawList[smaller]) )
    textObj1=str(diagList[0])
    scoreObj1=str(scoreList[0])
    textObj2=str(diagList[1])
    scoreObj2=str(scoreList[1])
    toBlit1=bigCalibri.render(textObj1, False, BLACK)
    toBlit2=bigCalibri.render(textObj2, False, BLACK)
    stringBlit1=bigCalibri.render(scoreObj1, False, BLACK)
    stringBlit2=bigCalibri.render(scoreObj2, False, BLACK)
    screen.blit(toBlit1,(200,300))
    screen.blit(toBlit2, (200,400))
    screen.blit(stringBlit1,(700,300))
    screen.blit(stringBlit2,(700,400))

    pygame.display.flip()
    #normal top, non bottom

def analysisCollisions(x, y, mouseButton,state):
    mouseHitRect=pygame.Rect(x,y,1,1)
    actionList=[(0,485,500,215),(500,485,500,215)]
    collide=mouseHitRect.collidelist(actionList)
    if collide != -1 and mouseButton==1:
        if collide==0:
            state="MAINMENU"
        elif collide==1:
            state="SENDDOCTOR"
    return state






label_lines= [line.rstrip() for line
              in tf.gfile.GFile("C:/tmp/output_labels.txt")]

with tf.gfile.FastGFile("C:/tmp/output_graph.pb", "rb") as f:
    graph_def=tf.GraphDef()
    graph_def.ParseFromString(f.read())
    _=tf.import_graph_def(graph_def, name='')

running=True
while running:
    print (state)
    button=0
    mx=-1
    my=-1
    for evnt in pygame.event.get():
        if evnt.type==pygame.QUIT:
            running=False
        elif evnt.type==pygame.MOUSEBUTTONDOWN:
            mx,my=evnt.pos
            button=evnt.button
        elif evnt.type==pygame.MOUSEMOTION:
            button = getVal(evnt.buttons)
            mx,my=evnt.pos
    if state=="MAINMENU":
        drawMainMenu()
        state= mainMenuCollisions(mx, my, button,state)
        filePath=""
    elif state=="UPLOAD":
        drawFileExplorerGUI()
        PATH=askForFile()
        print (PATH)
        image_data=imageDataReturn(PATH)
        drawAnalysisScreen()
        state="ANALYSIS"
    elif state=="SETTINGS":
        ip=retrieve_input()
        state="MAINMENU"


    elif state=="ANALYSIS":
        diagList=[]
        scoreList=[]
        predictionScore=None
        verdictFinal=None
        with tf.Session() as sess:
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            predictions = sess.run(softmax_tensor,
            {'DecodeJpeg/contents:0': image_data})
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            for node_id in top_k:
                diag = label_lines[node_id]
                score = predictions[0][node_id]
                diagList.append(diag)
                scoreList.append(score)
                print('%s (score = %.5f)' % (diag, score))
        drawAnalysisScreen()
        drawAnslysisInfo(diagList, scoreList)
        state=analysisCollisions(mx, my, button,state)
    elif state=="SENDDOCTOR":

        communicateAppointments(userInfo)
    pygame.display.flip()
