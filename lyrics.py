import cv2
import os
import numpy as np

def change(img1, img2):
    # Convert the images to the same color space
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Compute the difference between the two images
    diff = cv2.absdiff(img1, img2)

    # Threshold the difference image to create a binary mask
    _, mask = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY)

    # Calculate the percentage of difference
    percentage = 100.0 * np.count_nonzero(mask) / mask.size

    return percentage, mask

dir = os.path.join(os.getcwd(), 'videos')
filename = 'lavenderhaze'

delay = 3
frames = []
cap = cv2.VideoCapture(os.path.join(dir, filename+'.mp4'))
fps = 30
time_limit = 20 + delay
total_frames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
curr_frame_num = 0
root_frame = None

selected_lower = np.array([227,106,200])
selected_higher = np.array([223,104,204])
bg_color = np.array([34, 34, 34])

while cap.isOpened():
    
    curr_frame_num += 1
    if curr_frame_num % fps == 0:
        print(f"{int(curr_frame_num/fps)}s/{int(total_frames/fps)}s")

    ret, frame = cap.read()
    if curr_frame_num/fps > time_limit:
        break
    if ret:
        if curr_frame_num/fps > delay:

            if root_frame is None:
                root_frame = frame

            percentage, diff_mask = change(root_frame, frame)
            print(percentage)
            if percentage > 8:
                root_frame = frame
                cv2.imshow('no bg', cv2.resize(root_frame, (854,480), interpolation=cv2.INTER_AREA))
                cv2.waitKey(0)

            diff_img = cv2.bitwise_and(frame, frame, mask=diff_mask)

            
            # Color mask
            # Create a mask that includes all pixels that are not equal to the background color
            mask_no_bg = cv2.inRange(frame, bg_color + 1, np.array([255, 255, 255]))
            frame_no_background = cv2.bitwise_and(frame, frame, mask=mask_no_bg)

            selected_mask_range = cv2.inRange(frame, selected_lower, selected_higher)
            selected_mask = cv2.cvtColor(selected_mask_range, cv2.COLOR_GRAY2BGR)
            frame_selected = frame & selected_mask

            #cv2.imshow('diff', cv2.resize(diff_img, (854,480), interpolation=cv2.INTER_AREA))
            #cv2.imshow('selected', cv2.resize(frame_selected, (854,480), interpolation=cv2.INTER_AREA))
            #cv2.imshow('no bg', cv2.resize(frame_no_background, (854,480), interpolation=cv2.INTER_AREA))
            #cv2.waitKey(0)
            # Apply thresholding to convert the grayscale image to binary
            #_, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

            # # Find contours in the binary image
            # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # # Iterate over each contour found
            # counter = 0
            # for contour in contours:
            #     counter += 1
            #     # Get the bounding rectangle for the contour
            #     x, y, w, h = cv2.boundingRect(contour)
                
            #     # Crop the bounding rectangle to extract the word
            #     word = frame[y:y+h, x:x+w]
                
            #     # Downsize without aspect ratio
            #     word = cv2.resize(word, (1280,720), interpolation=cv2.INTER_AREA)
            #     print(f'{counter}/{len(contours)}')
            #     # Display the word
            #     cv2.imshow('word', word)
            #     cv2.waitKey(0)
        else:
            pass
    else:
        break

cap.release()