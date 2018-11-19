# Tensorflow-Street-Sign-Recognition (Automotive-Object-Detection)
Street Sign recognition using Tensorflows ObjectDetector
# Motivation
The motivation for this project lays both personal interest in a better understanding for object detection and academic research. The goal is to develop a foundation for a road-sign-detection (RSD) with the option to add further objects or functions to it. The ultimate goal is to have a useable object detection for the automotive sector.

# Table of Contents
1. Gathering and Analyzing Data 
2. Neural Networks
3. Using Tensorflow
4. Results
5. Outlook

# 1. Gathering and Analyzing Data

The first step to take was to define the road signs and objects for the database. The database builds up on the RUB ["German Traffic Sign Database"][1], therefore the objects in the database used in the repository are similar pictures of everyday traffic situations in Germany. In order to build the database that would be able to detect a larger amount of road signs it was necessary to label a much larger number of pictures. The goal was to distinguish between more than 150 road signs, traffic lights and more than 15 physical objects such as pedestrians, cars and motorcycles.

### Extracting Single Images from Videos

In the second step the pictures needed to be generated and labelled. In order to generate the pictures a simple command-line tool was developed that allows videos to be read in and extract those frame by frame. In the tool it is possible to alternate the number of frames taken. For highway footage every 5th frame was taken, while for urban footage the number of extracted frames was set to every 15th frame.

### Labeling Images

The Images were labeled with the open-source tool LabelImg for Windows [2]. In order to ensure that the images will be labeled correctly numbers were used as labels, these will be later translated back to describtions of the object. The use numbers reduces the likeliness of typos in the labeling process. 

### Analyzing the Labels

As real life traffic situations are used as input of the process the dataset needs to be reviewed and analyzed regularly. Therefore another tool was developed (DataSetCLI.py) to manage the large amounts of data. The tool offers multiple options for the database.

##### Export of Classes

This function allows the export of single or multiple classes from the database as a ZIP-file. It allows users to build models that either exceed a certain amount of Images in the database or to limit the database to certain kinds of objects. The function allows for example to extract only road signs with a speed limit but no other road signs or objects. During the export a CSV-file is generated and added within the ZIP-file to ensure the content of exported class is correct. The ZIP holds images as (PNG-files) as well as labels (XML-files)

##### Generate CSV-File for Dataset

Another function is the generation of CSV files 

##### Generate Diagram for Dataset

##### Genera

##### Remove Empty Images

### Data Augmentation

As not every class holds the same amount of objects it becomes necessary to implement a data augmentation process. With this existing pictures are alternated in such way that these can be used again in the learning process. For the augmentation the Python library "augmentor.py" [3] by the MIT is used. The tool has a large amount of functions implemented of which those useable for road sign detection are shown below. Some of these are only applayble to certain classes.

##### Rotating

Rotation is a simple function that allows to generate variance in the dataset. It needs to be ensured that the roatation is not to strong but somewhere between 10 and -10 degrees. Elsewise traffic signs may have a different meaning. This is also the reason why the rotate function of tensorflow can't be used as it only allows rotations at 90, 180 and 270 degrees.

<img width="1512" alt="bildschirmfoto 2018-11-19 um 12 35 27" src="https://user-images.githubusercontent.com/34514578/48686783-d2737980-ebf8-11e8-922f-c64c057fc0cb.png">

##### Zoom

The Zoom function is rather simple and lays focus on a different part of the picture. Yet the size of the image reamins the same. The main advantage lays in a variance of quality and the relative strong change of objects in the overall image. 

<img width="1555" alt="bildschirmfoto 2018-11-19 um 12 48 06" src="https://user-images.githubusercontent.com/34514578/48686910-9a206b00-ebf9-11e8-8268-483f30d155f4.png">


##### Mirroring

The mirroring function is needed if objects are either symmetric or a mirrored version exists. In the picture below for example the amount of blue signs with an arrow to the bottom-right is high in the dataset while the mirrored version with the arrow to the bottom-left is very low. Mirroring equalizes this in the entire dataset.

<img width="1554" alt="bildschirmfoto 2018-11-19 um 12 39 35" src="https://user-images.githubusercontent.com/34514578/48686793-e4551c80-ebf8-11e8-96bb-dccca2f8bc4a.png">

##### Shearing

Shearing 

<img width="1550" alt="bildschirmfoto 2018-11-19 um 12 40 54" src="https://user-images.githubusercontent.com/34514578/48686796-e7500d00-ebf8-11e8-84bc-b5a3cef1b912.png">

##### Contrast

<img width="1489" alt="bildschirmfoto 2018-11-19 um 12 37 33" src="https://user-images.githubusercontent.com/34514578/48686784-d69f9700-ebf8-11e8-9310-a25ff12050d3.png">

##### Elastic Distortion


<img width="1555" alt="bildschirmfoto 2018-11-19 um 12 38 58" src="https://user-images.githubusercontent.com/34514578/48686791-e15a2c00-ebf8-11e8-877b-895ef13dcaf5.png">

# 2. Neural Networks
Before

# 3. Using TensorFlow

# 4. Results

# 5. Outlook

# List of Refrences
[1]http://benchmark.ini.rub.de/?section=gtsdb&subsection=news
[2]https://github.com/tzutalin/labelImg
[3]https://augmentor.readthedocs.io

