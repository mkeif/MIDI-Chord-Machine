import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import matplotlib
import cvzone
import midiwrapper

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.5)
keys = [["C", "C#", "D", "D#"],
        ["E", "F", "F#", "G"],
        ["G#", "A", "A#", "B"]]


NOTES = [['C', 'C#', 'D', 'Eb'], 
        ['E', 'F', 'F#', 'G'],
        ['Ab', 'A', 'Bb', 'B']]

def drawAll(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cvzone.cornerRect(img, (button.pos[0], button.pos[1], button.size[0], button.size[1]),
                          20, rt=0)
        cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 255), cv2.FILLED)
        cv2.putText(img, button.text, (x + 20, y + 65),
                    cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
    return img

class Button():
    def __init__(self, pos, text, size=[85, 85]):
        self.pos = pos
        self.size = size
        self.text = text


buttonList = []
for i in range(len(NOTES)):
    for j, key in enumerate(NOTES[i]):
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))

midi = midiwrapper.MIDIplayer()

while True:
    status, img = cap.read()
    img = cv2.flip(img, 1)
    
    
    
    hands, img = detector.findHands(img, draw=True, flipType=False)
    img = drawAll(img, buttonList)
    
    if hands:
        hand1 = hands[0]
        lmList = hand1["lmList"]
    
        if lmList:
            for button in buttonList:
                x, y = button.pos
                w, h = button.size
                
                if x < lmList[8][0] < x + w and y < lmList[8][1] < y + h:
                    cv2.rectangle(img, (x - 5, y - 5), (x + w + 5, y + h + 5), (175, 0, 175), cv2.FILLED)
                    cv2.putText(img, button.text, (x + 20, y + 65),
                                cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    if len(hands) == 2 and hands[1]:
                        
                        fingers = detector.fingersUp(hands[1])
                    #cv2.putText(img, len(fingers), (100, 1100),
                                    #cv2.FONT_HERSHEY_PLAIN, 4, (255, 255, 255), 4)
                    #print(fingers)
                        if fingers:
                            midi.play(button.text, sum(fingers))
                    else:
                        midi.play(button.text, 1)
    else:
        midi.offall()               
                    
                
                
                    #available_ports = midi_out.get_ports()
    
    cv2.imshow("camera preview", img)
    cv2.waitKey(1)