# -*- coding: utf-8 -*-
"""TraficSignRecognition.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tlkoCOfKMuoASvrv4Xu9q6OgDd5luz8H

**Traffic Sign Detection**

Constructing the Model in following four steps :
Explore the dataset
Build a CNN model
Train and validate the model
Test the model with test dataset

1.   Explore the dataset
2.   Build a CNN model
3.   Train and validate the model
4.   Test the model with test dataset

1. EXPLORE THE DATASET

Connecting the drive to colab file for accessing the data set
"""

from google.colab import drive
drive.mount('/content/drive')

# import the required libraries and modules
import pandas as pd
import numpy as np
import matplotlib.pyplot  as plt
import tensorflow as tf
from PIL import Image
import os
os.chdir("/content/drive/MyDrive/project")
from sklearn.model_selection import train_test_split
from tensorflow.keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Conv2D, MaxPool2D, Dense ,Flatten ,Dropout

Meta = "/content/drive/MyDrive/project/Meta"
Train = "/content/drive/MyDrive/project/Train"
Test = "/content/drive/MyDrive/project/Test"

data  = []
label = []
cur_path = os.getcwd()
for i in range(43):
  path = os.path.join(cur_path, Train , str(i))
  images = os.listdir(path) # it is list of path of train folders
  for a in images:
    try:
      image = Image.open(path + '//' + a)
      image = image.resize((30,30))
      image = np.array(image)
      data.append(image) # image is the list that have images of train
      label.append(i)
    except :
      print("OOPS!! Error in uploading image")
data = np.array(data) # array of images of train folder
label = np.array(label) # array of name of Subfolders in Train Folder

cur_path

data = np.array(data)
label = np.array(label)

data.shape

label.shape

# Now lets split the data in training and testing using sklearn library
X_train, X_test ,y_train, Y_test = train_test_split(data, label, test_size = 0.2, random_state= 42)
print(X_train.shape , X_test.shape , y_train.shape, Y_test.shape)
# one hot encoding of testing dataset
y_train = to_categorical(y_train ,43) 
y_test = to_categorical(Y_test, 43)

"""Build the CNN Model"""

# Now let's build cnn model using Keras
#Building the model
Model = Sequential()
# Adding First layer
Model.add(Conv2D(filters= 32 , kernel_size= (5,5), activation='relu', input_shape = X_train.shape[1:]))
Model.add(Conv2D(filters= 32 , kernel_size= (5,5), activation='relu'))
Model.add(MaxPool2D(pool_size=(2,2)))
Model.add(Dropout(rate = 0.25))
# Adding second layer
Model.add(Conv2D(filters= 64 , kernel_size= (3,3), activation='relu'))
Model.add(Conv2D(filters= 64 , kernel_size= (3,3), activation='relu'))
Model.add(MaxPool2D(pool_size=(2,2)))
Model.add(Dropout(rate = 0.25))
Model.add(Flatten())
# Adding Dense Layer
Model.add(Dense(256,activation= 'relu'))
Model.add(Dropout(rate = 0.5))
Model.add(Dense(43,activation = "softmax"))

"""Training and validation"""

# Lets compile our model now
Model.compile(loss = 'categorical_crossentropy' , optimizer = 'adam', metrics = ['accuracy'])

from tensorflow.keras.preprocessing.image import ImageDataGenerator
epochs = 15 # Now lets try our datset on the model we build 15 Times
x = ImageDataGenerator(
    rotation_range = 10,
    zoom_range = 0.15,
    width_shift_range = 0.1,
    height_shift_range = 0.1,
    shear_range = 0.15,
    horizontal_flip = False,
    vertical_flip = False,
    fill_mode = "nearest"
)
history  = Model.fit(x.flow(X_train, y_train , batch_size = 32), epochs = epochs, validation_data = (X_test, y_test) )

"""Visualisation"""

# Lets plot the graph using matplotlib
plt.figure(0)
plt.plot(history.history['accuracy'], label = 'Training accuracy')
plt.plot(history.history['val_accuracy'], label = 'Val accuracy')
plt.title("Accuracy")
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.figure(1)
plt.plot(history.history['loss'] , label = 'Training loss')
plt.plot(history.history['val_loss'], label = 'Val loss')
plt.title("Loss")
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()

"""Evaluation"""

# result 
result  = Model.evaluate(X_test , y_test , verbose = 0)
print('test score ' , result[0])
print('Test accuracy' , result[1])

y_pred = Model.predict(X_test)
y_test_class = np.argmax(y_test,axis=1)
y_pred_class = np.argmax(y_pred,axis=1)

from sklearn.metrics import accuracy_score
score=accuracy_score(y_pred_class,y_test_class)
score