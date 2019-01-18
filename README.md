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

As real life traffic situations are used as input of the process the dataset needs to be reviewed and analyzed regularly. Therefore another tool was developed (DataSetCLI.py) to manage the large amounts of data. The tool offers multiple options for the database. All fuctions require a path to the root folder of your data, which should contain only images and xml-label files.

    .
    ├── root Data               #Root folder containing the data
        ├── images              #images location folder
        ├── labels              #xml location folder
        

##### Export of Classes

This function allows the export of single or multiple classes from the database as a ZIP-file. It allows users to build models that either exceed a certain amount of Images in the database or to limit the database to certain kinds of objects. The function allows for example to extract only road signs with a speed limit but no other road signs or objects. During the export a CSV-file is generated and added within the ZIP-file to ensure the content of exported class is correct. The ZIP holds images as (PNG-files) as well as labels (XML-files)

##### Generate CSV-File for Dataset

Another function is the generation of CSV files 

##### Generate Diagram for Dataset



##### Remove Empty Images
Validates if the dataset contains images without a corresponding xml label file to references it and deletes them. The ulterior motive is to remove images without any street sign or object present, that might have slipped through the labeling process.

### Data Augmentation

As not every class holds the same amount of objects it becomes necessary to implement a data augmentation process. With this existing pictures are alternated in such way that these can be used again in the learning process. For the augmentation the Python library "augmentor.py" [3] by the MIT is used. The tool has a large amount of functions implemented of which those useable for road sign detection are shown below. Some of these are only applayble to certain classes.

#### Rotating

Rotation is a simple function that allows to generate variance in the dataset. It needs to be ensured that the roatation is not to strong but somewhere between 10 and -10 degrees. Elsewise traffic signs may have a different meaning. This is also the reason why the rotate function of tensorflow can't be used as it only allows rotations at 90, 180 and 270 degrees.

<img width="1512" alt="bildschirmfoto 2018-11-19 um 12 35 27" src="https://user-images.githubusercontent.com/34514578/48686783-d2737980-ebf8-11e8-922f-c64c057fc0cb.png">

#### Zoom

The Zoom function is rather simple and lays focus on a different part of the picture. Yet the size of the image reamins the same. The main advantage lays in a variance of quality and the relative strong change of objects in the overall image. 

<img width="1555" alt="bildschirmfoto 2018-11-19 um 12 48 06" src="https://user-images.githubusercontent.com/34514578/48686910-9a206b00-ebf9-11e8-8268-483f30d155f4.png">


#### Mirroring

The mirroring function is needed if objects are either symmetric or a mirrored version exists. In the picture below for example the amount of blue signs with an arrow to the bottom-right is high in the dataset while the mirrored version with the arrow to the bottom-left is very low. Mirroring equalizes this in the entire dataset.

<img width="1554" alt="bildschirmfoto 2018-11-19 um 12 39 35" src="https://user-images.githubusercontent.com/34514578/48686793-e4551c80-ebf8-11e8-96bb-dccca2f8bc4a.png">

#### Shearing

Shearing is useable for many different directions. It includes horizontal and vertical shearing as well as shearing to each of the corners. The function augments the data in such way as it would result if another picture was taken seconds later. It also makes the trained model more robust towards different angles.

<img width="1550" alt="bildschirmfoto 2018-11-19 um 12 40 54" src="https://user-images.githubusercontent.com/34514578/48686796-e7500d00-ebf8-11e8-84bc-b5a3cef1b912.png">

#### Contrast

The function is very simple as it just alters the contrast of the image. The idea behind this is again improving the robustness of the trained model. Different contrasts occure usually in different lightning situations and the image quality of the used camera.

<img width="1489" alt="bildschirmfoto 2018-11-19 um 12 37 33" src="https://user-images.githubusercontent.com/34514578/48686784-d69f9700-ebf8-11e8-9310-a25ff12050d3.png">

#### Elastic Distortion

Elastic distortion is a very interesting alteration of the pictures. As it can be seen on the right picture the object's corners, such as the large direction sign, are warped. This happens usually while driving when the car hits potholes or experiences other sudden and strong movements. Due to the image generation line by line the image gets distorted.

<img width="1555" alt="bildschirmfoto 2018-11-19 um 12 38 58" src="https://user-images.githubusercontent.com/34514578/48686791-e15a2c00-ebf8-11e8-877b-895ef13dcaf5.png">

### Database

With this a fairly large database was generated including 50.000 labels on approximatly 35.000 images. As the objects, that were to be labeled, changed later on, the amount of labels will keep growing rapidly. This will hapen though on the existing image database of 35.000 samples.An example of the database is presented below. ![datenbank](https://user-images.githubusercontent.com/34514578/51392416-e7747680-1b6f-11e9-9e9c-ab6787addda5.jpg)

# 2. Neural Networks

For this, two neural networks were taken into account. "Faster_R-CNN_Inception_V2_COCO" and "SSD_Mobilenet_COCO" both neural networks are pretrained on the COCO dataset that includes thousands of pictures with labels from everyday situations, such as humans, cars, trees, airplanes, etc. (http://cocodataset.org/#home)[6]. Yet both differ strongly.

## Faster R-CNN

The Faster R-CNN is an evolution of the convolutional neural network approach. In order to accelerate this, a focus was layed on the faster recognition of areas of interest in an image. This focus on the regions (that is what the "R" stands for in R-CNN) made it much easier to check a limited amount of objects in a picture. This was then acclerated with "Fast-" and "Faster R-CNN". For further reedings I recommend the papers of Ross Girshick as one of the main people behind it. Faster R-CNN is able to read data in basically every size which doesn't make it neccessary to crop the pictures before or in Tensorflow.

The advantage of this neural network is, that Faster R-CNN is pretty accurate als with small amounts of data. Yet it still takes about 50ms to analyze an image. Dpending on the use case this might be too slow, such as for live deployment in a car.

## SSD_Mobilenet_COCO

SSD_Mobilenet is focused stronger on fast image detection. This means, that the results are less reliable but it can be deployed on live feeds at 30fps and also has much lower hardware requirements. All in all the findings were fairly weak especially with small amounts of data it was almost impossible to generate reliable output.

For SSD_Mobilenet the file dimensions are limited to 300x300 images. If changes are made to this in Tensorflow, the model doesn't detect anything, which can be very frustrating. Though it is possible to use the same workflow as described before. Various tools allow to cut out the pixel within the bounding boxes of the labels. With this the 300x300 image size is not as much of a restiction anymore. 

For this project the Faster-RCNN was chosen as the goal was develop a road-sign detection that reliably analyses a large amount of existing video data in order to improve the database that comes with it. Hence, the focus layed more on quality than on speed.

# 3. Using TensorFlow

For the object detection model Google's tensorflow was used running on 2 GeForce GTX 1080Ti with each 11GB of Vram. The processor is an Intel 8700K and 32GB of Ram. For the installation and set-up of the environment the tutorial by EdjeElectronics [4] was used. The tutorial gives a great introduction and makes it easy to set up the anaconda environment and tensorflow itself. Furthermore it includes already all the necessary iformation on how to use your own dataset with TensorFlow. This includes generating the tf.record files, labelmap.pbtxt, ... 
For the training it is recommended to check the Tensorflow Model Zoo [5] on GitHub and apply the models to your own code. For this project Faster_RCNN_InceptionV2_COCO seemed to be the best fit. If everything was set up correctly the training is started by the following command in the anaconda prompt:

    python train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/faster_rcnn_inception_v2_coco_A.config --num_clones=2 --ps_tasks=1
    
It should be emphasised that the last two commands `--num_clones=2 --ps_tasks=1` are necessary for the use with multiple GPUs. The "num_clones" states the number of GPUs in use. If only one GPU is used the command for the anaconda prompt is 

    python train.py --logtostderr --train_dir=training/ --pipeline_config_path=training/faster_rcnn_inception_v2_coco_A.config
    
The time to train depends strongly on the model. In this case the training times took approximatly 10-12 days. In the chart it can be seen that after a strong decline in the beginning the loss maintained at a low level. The following image shows the training process of the road sign detetcion. ![graphsign](https://user-images.githubusercontent.com/34514578/51392448-ff4bfa80-1b6f-11e9-9ae7-4d1e097a1d3f.jpg)

All in all three models were trained. One for road sign detection, one for object detection and a combination of those two. The result can be seen below. The first image shows the result of the road sign detection, while the second image shows the outcome of the object detection. ![sign2](https://user-images.githubusercontent.com/34514578/51392471-15f25180-1b70-11e9-9564-4a990036e6eb.jpg) ![object1](https://user-images.githubusercontent.com/34514578/51392461-0bd05300-1b70-11e9-94ca-04511c1355e7.jpg)

# 4. Results

The results need to be distinguished in multiple ways. Such as accuracy and the kind of failures that occure. All in all we reached an accuracy of 85% of the road signs close to the sign. Which is well above the initial expectations for this research topic. The failures that occure in object-detection can be seperated into tour different modes. Those will be described quickly, as a starting point for further readings into the subject.

#### True-Positive

The object detector correctly identifies an object. Hence, this is the result we are seeking for and no failure occured. In the case of this object detection this result became more reliable the closer the road sign was. ![sign1](https://user-images.githubusercontent.com/34514578/51392469-1559bb00-1b70-11e9-8799-46f090e8c65e.jpg)


#### False-Positive

A false positive detection appears when a sign is marged incorrectly. Incorrectly maked signs usually occure when signs are too small, so for example in a large distance or an insufficient amount of labels are saved in the database. ![falsepositive](https://user-images.githubusercontent.com/34514578/51392446-fe1acd80-1b6f-11e9-8c5b-a344e45467b3.jpg). This is especially important, as completely wrong detections can be hard to understand and to solve in many cases and sometimes even relate to issues within the label-database. Luckily this model doesn't suffer much from it. Usually high thresholds also ensure the limitation of true-negative detections. 

#### True-Negative

True negative detections are by definition not very spectacular, yet important. In this case the detector correctly doesn't give out any kind of result.

#### False-Negative

The opposite to true-negative are false-negative detetcions. In this case a sign or object is just missed by the detector. Also often relating to low amounts of labels in the dataset. In this particular case we also see the limuts of the faster-RCNN as shown in the picture below. While the "stop"-sign on the right and the "bus-stop"-sign are detected correctly, the "stop"-sign at the upper edge of the image is missed by the object detector. In this case the stop-sign is not at a common place but at a very unsual space. The RCNN misses that due to its focus on common sizes and positions for the initial choice of regions to be analyzed afterwards.

![nostop](https://user-images.githubusercontent.com/34514578/51392458-0a068f80-1b70-11e9-8178-c0395abd82e1.jpg)

# 5. Outlook

The object-detection still needs further improvements in many cases. It is yet not accurate enough nor does the speed match our demands. As this was archived within a term-paper, it is still a strong start for further improvements. Those will include the database as well as tests with other neural networks such as YOLO.

For further questions please refer to our LinkedIn profiles (that you can find in our profiles), contact us here on Github or leave a comment. 

# List of Refrences
[1]http://benchmark.ini.rub.de/?section=gtsdb&subsection=news
[2]https://github.com/tzutalin/labelImg
[3]https://augmentor.readthedocs.io
[4]https://github.com/EdjeElectronics/TensorFlow-Object-Detection-API-Tutorial-Train-Multiple-Objects-Windows-10/blob/master/README.md
[5]https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md
[6] http://cocodataset.org/#home
