#in this file, the data set is created so that we can directly access this in a tf environment
#currently, we only include images from the race 314
#these images are all in one file --> use cross-validation for training and/or split data later on
#change create_dataset to save the dataset

import matplotlib.pyplot as plt
import os
import cv2
import pickle
import re
#import Counter to figure out the occurences of the classes
##from collections import Counter

#name of the race(s)
race_name = '314'

#import labels of images
with open( 'C:\\ML\\nfsu2_data\\labels\\labels_one_list_' + race_name + '.data', 'rb' ) as f:
    labels_images = pickle.load(f)
number_total_images = len(labels_images)
#there are more images than labels since not all images are labeled -->only labeled up to number_total_images

#we used the index of these classes as labels:
classes = ["0","1","2","3","4","5","6","7","8","9", '+', '-', 'void', 'ewil', 'name']

#load images
DataDirectory = 'C:\\ML\\nfsu2_data\\race_' + race_name +'\\details'

#print the images if necessary:
##for i in range(1234,1234):
##    PathToExampleImage = os.listdir(DataDirectory)[i]
##    print(PathToExampleImage)
##    img_array = cv2.imread(os.path.join(DataDirectory,PathToExampleImage), cv2.IMREAD_GRAYSCALE)
####    print(img_array.shape)
##    plt.imshow(img_array, cmap="gray")
##    plt.show()

#rearrange os.listdir(DataDirectory) so that it is order by last number in the file name
def image_number(image):
    image = re.sub('^race_314_out', '', image)
    image = re.sub('.png$', '', image)
    return(int(image))

sorted_dir = sorted(os.listdir(DataDirectory), key = image_number)
##print(sorted_dir[:10])

#prepare to create dataset
training_data = []

def create_training_data():
    for i in range(number_total_images):
        PathToImage = sorted_dir[i]
##        print(Image)
        img_array = cv2.imread(os.path.join(DataDirectory,PathToImage), cv2.IMREAD_GRAYSCALE)
        training_data.append([img_array, labels_images[i]])

#change create_dataset to 1 if you want to create a dataset (and not delete it by accident)
create_dataset = 0
if create_dataset == 1:
    #create the dataset
    create_training_data()

    #save file
    with open( 'C:\\ML\\nfsu2_data\\data\\training_data_' + race_name + '.data', 'wb' ) as f:
        pickle.dump(training_data, f)
    print('training_data_{}.data saved succefully'.format(race_name))
    f.close()

       
