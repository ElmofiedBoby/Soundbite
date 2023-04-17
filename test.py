import cv2
import os
import numpy as np
from pytesseract import pytesseract
from pytesseract import Output

pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
config="-c preserve_interword_spaces=1 -c tessedit_char_whitelist=01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
dir = os.path.join(os.getcwd(), 'videos')
impath = os.path.join(os.getcwd(), 'images', 'frame')
filename = 'lovestory'

im = cv2.imread(impath+'390.png')
height, width, c = im.shape

def letter_box(im):
    letter_boxes = pytesseract.image_to_boxes(im, config=config)

    for box in letter_boxes.splitlines():
        box = box.split()
        x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        cv2.rectangle(im, (x,height-y), (w,height-h), (0,0,255), 3)
        cv2.putText(im, box[0], (x,height-h+32), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)

    cv2.imshow('impath', cv2.resize(im, (854,480), interpolation=cv2.INTER_AREA))
    cv2.waitKey(0)

def word_box(im):
    image_data = pytesseract.image_to_data(im, output_type=Output.DICT, config=config)
    
    for i, word in enumerate(image_data['text']):
        if word != '':
            x,y,w,h = image_data['left'][i],image_data['top'][i],image_data['width'][i],image_data['height'][i]
            cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),3)
            cv2.putText(im,word,(x,y-16),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)

    cv2.imshow('impath', cv2.resize(im, (854,480), interpolation=cv2.INTER_AREA))
    cv2.waitKey(0)


word_box(im)