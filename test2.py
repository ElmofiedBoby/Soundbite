import cv2
import os
import numpy as np
from pytesseract import pytesseract
from pytesseract import Output

def contourIntersect(original_image, contour1, contour2):
    # Two separate contours trying to check intersection on
    contours = [contour1, contour2]

    # Create image filled with zeros the same size of original image
    blank = np.zeros(original_image.shape[0:2])

    # Copy each contour into its own image and fill it with '1'
    image1 = cv2.drawContours(blank.copy(), contours, 0, 1)
    image2 = cv2.drawContours(blank.copy(), contours, 1, 1)
    
    # Use the logical AND operation on the two images
    # Since the two images had bitwise AND applied to it,
    # there should be a '1' or 'True' where there was intersection
    # and a '0' or 'False' where it didnt intersect
    intersection = np.logical_and(image1, image2)
    
    # Check if there was a '1' in the intersection array
    return intersection.any()

pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
config="-c tessedit_char_blacklist=|"
dir = os.path.join(os.getcwd(), 'videos')
impath = os.path.join(os.getcwd(), 'images', 'frame')
filename = 'lovestory'

img = cv2.imread(impath+'390.png')

# Convert the image to gray scale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Apply an adaptive threshold to the image
thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 11, 5)

# Find the contours in the image
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
words = []

# for c in range(len(contours)):
#     for comp in range(len(contours)):
#         if c is not comp and contourIntersect(img, contours[c], contours[comp]):
#             # intersection true - combine boxes
#             x1, y1, w1, h1 = cv2.boundingRect(contours[c])
#             x2, y2, w2, h2 = cv2.boundingRect(contours[comp])
#             x = min(x1, x2)
#             y = min(y1, y2)
#             w = max(x1 + w1, x2 + w2) - x
#             h = max(y1 + h1, y2 + h2) - y
#             words.append(x, y, w, h)
#             pass
#         else:
#             # intersection false
#             pass

#cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

print(contours[0])
cv2.imshow('impath', cv2.resize(img, (854,480), interpolation=cv2.INTER_AREA))
cv2.waitKey(0)