import cv2
import os, csv

with open(os.path.join(os.getcwd(),'FileSizes.csv'),'w', newline='') as out:
    writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_NONE)
    writer.writerow(['FileName', 'Height', 'Width', 'Channel'])

    for p, dirs, filenames in os.walk('PATH'):

        # read image
        for file in filenames:
            if file[-3:] == 'png':
                img = cv2.imread(file, cv2.IMREAD_UNCHANGED)

                # get dimensions of image
                dimensions = img.shape

                # height, width, number of channels in image
                height = img.shape[0]
                width = img.shape[1]
                channels = img.shape[2]

                writer.writerow([file,img.shape[0],img.shape[1],img.shape[2]])
