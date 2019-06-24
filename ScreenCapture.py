#this script is responsible for the capturing the table with the leads and extracting the leads from it

import numpy as np

from PIL import ImageGrab, Image
import cv2
import time
from keras.models import load_model
import matplotlib.pyplot as plt
import time
from win32api import GetSystemMetrics



#load model
num_epochs = 5
model = load_model('C:\\ML\\nfsu2_data\\models\\reward_classifier_epochs_' + str(num_epochs) + '.h5')


#during testing, wait for 10 sec so that the screen is set up properly
start_in_sec = 10
print('Open window with nfsu2 now! You have {} seconds'.format(start_in_sec))
time.sleep(start_in_sec)
#input()

#now we calculate the relative distances of the table based on the initial cuts of the 1280 x 720 image
#the game has to be in full screen; else the calculations will be incorrect
#get initial dimensions of the screen
width_video = 1280
height_video = 720
width_screen = GetSystemMetrics(0)
height_screen = GetSystemMetrics(1)

leads_in_video = np.array((1159, 160, 1229, 280))
leads_on_screen = leads_in_video / np.array((width_video,height_video,width_video,height_video)) * np.array((width_screen,height_screen,width_screen,height_screen))
leads_on_screen = np.rint(leads_on_screen).astype(int)
leads_on_screen = tuple(leads_on_screen)
#use widths from video as screen_img gets scaled back immediately

table_width = leads_in_video[2] - leads_in_video[0]
table_height = leads_in_video[3] - leads_in_video[1]

#grab sample screen
screen_img =  np.array(ImageGrab.grab(bbox = leads_on_screen))
screen_img = cv2.resize(screen_img, dsize=(table_width,table_height), interpolation=cv2.INTER_CUBIC)
screen_img_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)/255
##plt.imshow(screen_img_gray*255, cmap = 'gray')
##plt.show()

#restate classes to check predictions
classes = ["0","1","2","3","4","5","6","7","8","9", '+', '-', 'void', 'ewil', 'name']

#save predictions in an array to reconstruct the current lead
leads_predicted_not_joined = np.empty((4,5), dtype='str')
leads_predicted = [0,0,0,0]



for y in range(4):
    for x in range(5):
        if x == 2:
            cropped_img = np.array([screen_img_gray[y*table_height//4: (y+1)*table_height//4, x*table_width//5 - 1: (x+1)*table_width//5 - 1].flatten()])
        elif x == 3:
            cropped_img = np.array([screen_img_gray[y*table_height//4: (y+1)*table_height//4, x*table_width//5 + 2: (x+1)*table_width//5 + 2].flatten()])
        else:
            cropped_img = np.array([screen_img_gray[y*table_height//4: (y+1)*table_height//4, x*table_width//5    : (x+1)*table_width//5].flatten()])
            
        prediction = classes[model.predict_classes(cropped_img)[0]]
        print('X = {}, y = {}, predicted label = {}'.format(x, y, prediction))
        
        if prediction in ['void','ewil','name']:
            leads_predicted_not_joined[y][x] = ''
        else:
            leads_predicted_not_joined[y][x] = prediction
    concatenated_lead = ''.join(leads_predicted_not_joined[y])
    #replace 'ewil' and 'name' by 0
    if concatenated_lead == '':
        concatenated_lead = 0
    leads_predicted[y] = int(concatenated_lead)
    
##        plt.imshow(cropped_img.reshape(30,14), cmap = 'gray')
##            plt.show()





def screen_record(): 
    last_time = time.time()
    
    while(True):
        screen_img =  np.array(ImageGrab.grab(bbox = leads_on_screen))
        screen_img_gray = cv2.cvtColor(screen_img, cv2.COLOR_BGR2GRAY)
        #get boxes
        for y in range(4):
            for x in range(5):
                if x == 2:
                    cropped_img = screen_img_gray[y*table_height//4: (y+1)*table_height//4][x*table_width//5 - 1: (x+1)*table_width//5 - 1]
                    plt.imshow(cropped_img, cmap = 'gray')
                    plt.show()
                elif x == 3:
                    cropped_img = screen_img_gray[y*table_height//4: (y+1)*table_height//4][x*table_width//5 + 2: (x+1)*table_width//5 + 2]
                else:
                    cropped_img = screen_img_gray[y*table_height//4: (y+1)*table_height//4][x*table_width//5    : (x+1)*table_width//5]

        print('loop took {} seconds'.format(time.time()-last_time))
        last_time = time.time()
        ##cv2.imshow('window',cv2.cvtColor(printscreen, cv2.COLOR_BGR2RGB))
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break
