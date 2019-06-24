#use the dataset(s) of the leads (images and labels) to train classifier for lead recognition

import pickle
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import time

#set up race name(s)
race_name = '314'

#load dataset
with open('C:\\ML\\nfsu2_data\\data\\training_data_' + race_name + '.data', 'rb') as f:
    dataset = pickle.load(f)

#we used the index of these classes as labels:
classes = ["0","1","2","3","4","5","6","7","8","9", '+', '-', 'void', 'ewil', 'name']

#create X and y, and flatten X beforehand
X = []
y = []

for features, label in dataset:
    X.append(features)
    y.append(label)

#get dimensions of data
height, width = X[0].shape
##print(height,width)

for i in range(len(X)):
    X[i] = X[i].flatten()

#split dataset into test and training sets, and normalize features to a range of [0,1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1, random_state = 42)
X_train, X_test, y_train, y_test = np.array(X_train)/255, np.array(X_test)/255., np.array(y_train), np.array(y_test)

#check if the images are correctly saved
def display(i):
    '''displays the i-th test image and its label'''
    img = X_test[i]
    plt.title('Example %d, Label: %d' % (i, y_test[i]))
    plt.imshow(img.reshape(height,width), cmap="gray")
    plt.show()

##for i in range(100,110):
##    display(i)

#do the training
model = keras.Sequential([
    keras.layers.Dense(height*width, input_shape=(height*width,)),
    ##keras.layers.Flatten(input_shape = (height*width,)),
    keras.layers.Dense(128, activation=tf.nn.relu),
    keras.layers.Dense(len(classes), activation=tf.nn.softmax)
])

model.compile(optimizer='adam', 
              loss='sparse_categorical_crossentropy',
              metrics=['accuracy'])

num_epochs = 5
model.fit(X_train, y_train, epochs = num_epochs)

#evaluate the model
test_loss, test_acc = model.evaluate(X_test, y_test)

print('Test accuracy:', test_acc)

#model.save('my_model.h5')
model.save('C:\\ML\\nfsu2_data\\models\\reward_classifier_epochs_' + str(num_epochs) + '.h5')
print('Saved model at C:\\ML\\nfsu2_data\\models\\reward_classifier_epochs_' + str(num_epochs) + '.h5')

##predictions = model.predict(X_test)

del model

#model = load_model('my_model.h5')
model = load_model('C:\\ML\\nfsu2_data\\models\\reward_classifier_epochs_' + str(num_epochs) + '.h5')












