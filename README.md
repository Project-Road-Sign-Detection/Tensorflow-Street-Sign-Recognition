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

##### Zoom

##### Mirroring

##### Shearing

##### Contrast

##### Elastic Distortion



# 2. Neural Networks
Before

# 3. Using TensorFlow

# 4. Results

# 5. Outlook

# List of Refrences
[1]http://benchmark.ini.rub.de/?section=gtsdb&subsection=news
[2]https://github.com/tzutalin/labelImg
[3]https://augmentor.readthedocs.io


![img_3912](https://user-images.githubusercontent.com/34514578/48686015-afdf6180-ebf4-11e8-8d4f-e18202415dfc.JPG)
