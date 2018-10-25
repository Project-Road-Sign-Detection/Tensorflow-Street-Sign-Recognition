import xml.etree.ElementTree as ET
import os
import matplotlib.pyplot as plt
import numpy as np
import csv
import zipfile
import pandas as pd
from GuiLogger import GuiLogger
from random import shuffle

class Generator():

    def __init__(self, path, logger: GuiLogger,  classes=range(1, 156)):
        self.logger = logger
        self.classes = classes
        self.labelmap = {0: "speed limit 20 (prohibitory)",
                         1: "speed limit 30 (prohibitory)",
                         2: "speed limit 50 (prohibitory)",
                         3: "speed limit 60 (prohibitory)",
                         4: "speed limit 70 (prohibitory)",
                         5: "speed limit 80 (prohibitory)",
                         6: "restriction ends 80 (other)",
                         7: "speed limit 100 (prohibitory)",
                         8: "speed limit 120 (prohibitory)",
                         9: "no overtaking (prohibitory)",
                         10: "no overtaking (trucks) (prohibitory)",
                         11: "priority at next intersection (danger)",
                         12: "priority road (other)",
                         13: "give way (other)",
                         14: "stop (other)",
                         15: "no traffic both ways (prohibitory)",
                         16: "no trucks (prohibitory)",
                         17: "no entry (other)",
                         18: "danger (danger)",
                         19: "bend left (danger)",
                         20: "bend right (danger)",
                         21: "bend (danger)",
                         22: "uneven road (danger)",
                         23: "slippery road (danger)",
                         24: "road narrows (danger)",
                         25: "construction (danger)",
                         26: "traffic signal (danger)",
                         27: "pedestrian crossing (danger)",
                         28: "school crossing (danger)",
                         29: "cycles crossing (danger)",
                         30: "snow (danger)",
                         31: "animals (danger)",
                         32: "restriction ends (other)",
                         33: "go right (mandatory)",
                         34: "go left (mandatory)",
                         35: "go straight (mandatory)",
                         36: "go right or straight (mandatory)",
                         37: "go left or straight (mandatory)",
                         38: "keep right (mandatory)",
                         39: "keep left (mandatory)",
                         40: "roundabout (mandatory)",
                         41: "restriction ends (overtaking) (other)",
                         42: "restriction ends (overtaking (trucks)) (other)",
                         43: "restriction ends 60 (other)",
                         44: "restriction ends 70 (other)",
                         45: "speed limit 90 (prohibitory)",
                         46: "restriction ends 90 (other)",
                         47: "speed limit 110 (prohibitory)",
                         48: "restriction ends 110 (other)",
                         49: "restriction ends 120 (other)",
                         50: "speed limit 130 (prohibitory)",
                         51: "restriction ends 130 (other)",
                         52: "bend double right (danger)",
                         53: "highway turn (left) (other)",
                         54: "maximum width (prohibitory)",
                         55: "maximum height (prohibitory)",
                         56: "minimum truck distance (prohibitory)",
                         57: "highway exit 200 (other)",
                         58: "highway exit 100 (other)",
                         59: "right lane merging (other)",
                         60: "warning beacon roadwork (other)",
                         61: "speed limit 60 (digital) (prohibitory)",
                         62: "restriction ends 60 (digital) (other)",
                         63: "speed limit 70 (digital) (prohibitory)",
                         64: "restriction ends 70 (digital) (other)",
                         65: "speed limit 80 (digital) (prohibitory)",
                         66: "restriction ends 80 (digital) (other)",
                         67: "restriction ends 80 (digital) (other)",
                         68: "restriction ends 90 (digital) (other)",
                         69: "speed limit 100 (digital) (prohibitory)",
                         70: "restriction ends 100 (digital) (other)",
                         71: "speed limit 110 (digital) (prohibitory)",
                         72: "restriction ends 110 (digital) (other)",
                         73: "left lane merging (other)",
                         74: "speed limit 120 (digital) (prohibitory)",
                         75: "restriction ends 120 (digital) (other)",
                         76: "speed limit 130 (digital) (prohibitory)",
                         77: "restriction ends 130 (digital) (other)",
                         78: "no overtaking (digital) (prohibitory)",
                         79: "restriction ends 130 (digital) (other)",
                         80: "no overtaking (trucks) (digital) (prohibitory)",
                         81: "restriction ends (overtaking (trucks)) (other)",
                         82: "construction (digital) (danger)",
                         83: "traffic jam (digital) (danger)",
                         84: "highway exit (other)",
                         85: "traffic jam (other)",
                         86: "restriction distance (other)",
                         87: "restriction time (other)",
                         88: "highway exit 300m (other)",
                         89: "restriction ends 100 (other)",
                         90: "andreaskreuz (other)",
                         91: "one way street (left) (other)",
                         92: "one way street (right) (other)",
                         93: "beginning of highway (other)",
                         94: "end of highway (other)",
                         95: "busstop (other)",
                         96: "tunnel (other)",
                         97: "no cars (prohibitory)",
                         98: "train crossing (danger)",
                         99: "no bicycles (prohibitory)",
                         100: "no motorbikes (prohibitory)",
                         101: "no mopeds (prohibitory)",
                         102: "no horses (prohibitory)",
                         103: "no cars & motorbikes (prohibitory)",
                         104: "busses only (mandatory)",
                         105: "pedestrian zone (mandatory)",
                         106: "bicycle boulevard (mandatory)",
                         107: "end of bicycle boulevard (mandatory)",
                         108: "bicycle path (mandatory)",
                         109: "pedestrian path (mandatory)",
                         110: "pedestrian and bicycle path (mandatory)",
                         111: "separated path for bicycles and pedestrians (right) (mandatory)",
                         112: "separated path for bicycles and pedestrians (left) (mandatory)",
                         113: "play street (other)",
                         114: "end of play street (other)",
                         115: "beginning of motorway (other)",
                         116: "end of motorway (other)",
                         117: "crosswalk (zebra) (other)",
                         118: "dead-end street (other)",
                         119: "one way street (straight) (other)",
                         120: "priority road (other)",
                         121: "no stopping (prohibitory)",
                         122: "no stopping (beginning) (prohibitory)",
                         123: "no stopping (middle) (prohibitory)",
                         124: "no stopping (end) (prohibitory)",
                         125: "no parking (beginning) (prohibitory)",
                         126: "no parking (end) (prohibitory)",
                         127: "no parking (middle) (prohibitory)",
                         128: "no parking (prohibitory)",
                         129: "no parking zone (prohibitory)",
                         130: "end of no parking zone (prohibitory)",
                         131: "city limit (in) (other)",
                         132: "city limit (out) (other)",
                         133: "direction to village (other)",
                         134: "rural road exit (other)",
                         135: "speed limit 20 zone (prohibitory)",
                         136: "end speed limit 20 zone (prohibitory)",
                         137: "speed limit 30 zone (prohibitory)",
                         138: "end speed limit 30 zone (prohibitory)",
                         139: "speed limit 5 (prohibitory)",
                         140: "speed limit 10 (prohibitory)",
                         141: "restriction ends 10 (other)",
                         142: "restriction ends 20 (other)",
                         143: "restriction ends 30 (other)",
                         144: "speed limit 40 (prohibitory)",
                         145: "restriction ends 40 (other)",
                         146: "restriction ends 50 (other)",
                         147: "go left (now) (mandatory)",
                         148: "go right (now) (mandatory)",
                         149: "train crossing in 300m (other)",
                         150: "train crossing in 200m (other)",
                         151: "train crossing in 100m (other)",
                         152: "danger (digital) (danger)",
                         153: "restriction ends 100 (other)",
                         154: "highway turn (right) (other)"}

        self.PATH = path
        self.label_names = []
        self.label_paths = []

        for p, dirs, filenames in os.walk(self.PATH):
            self.label_names += [f for f in filenames if f[-3:] == 'xml']
            self.label_paths += [os.path.join(p, f) for f in filenames if f[-3:] == 'xml']

        self.class_score = self._calculateClassScore()

    def deleteEmptyImages(self, path=None):
        self.logger.log_sep("Bilder löschen")
        if not path:
            path = self.PATH
        d = 1
        for p, dirs, filenames in os.walk(path):
            for file in [f for f in filenames if f[-3:] == 'png']:
                if file[:-3] + 'xml' not in self.label_names:
                    os.remove(os.path.join(p, file))
                    self.logger.log(os.path.join(p, file) + " gelöscht.")
                    d = 0
        if d:
            self.logger.log("Keine Bilder ohne Label gefunden.")

        self.logger.log_sep()

    def _calculateClassScore(self, ):
        class_score = {}

        for label in self.label_paths:

            for ob in ET.parse(label).getroot().iter('object'):
                try:
                    clazz = int(ob.find('name').text)
                    xmin, ymin, xmax, ymax = [int(v.text) for v in ob.find('bndbox')]

                    if clazz in class_score:
                        class_score[clazz][0] += 1
                        class_score[clazz][1] += xmin
                        class_score[clazz][2] += ymin
                        class_score[clazz][3] += xmax
                        class_score[clazz][4] += ymax
                    else:
                        class_score[clazz] = [clazz, xmin, ymin, xmax, ymax]
                except Exception:
                    self.logger.log_err('Fehlerhafter Klassen bezeichner in: ' + label)

        for c in class_score:
            s = class_score[c][0]
            class_score[c][1] = round(class_score[c][1] / s, 2)
            class_score[c][2] = round(class_score[c][2] / s, 2)
            class_score[c][3] = round(class_score[c][3] / s, 2)
            class_score[c][4] = round(class_score[c][4] / s, 2)

        return class_score

    def _getClassName(self, i):
        if i in self.labelmap:
            return self.labelmap[i]
        else:
            self.logger.log_err(str(i) + " - kein Klassenbezeichner gefunden.")
            return "Unknown"

    def createCSVOverview(self, zipf=None):
        self.logger.log_sep("CSV Statistik erstellen")

        with open(os.path.join(self.PATH, "Summary.csv"), 'w', newline='') as out:
            writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow(['Class ID', 'Class Name', 'Frequenzy', 'Avg Xmin', 'Avg Ymin', 'Avg Xmax', 'Avg Ymax'])
            for c in self.class_score:
                if c in self.classes:
                    writer.writerow([c, self._getClassName(c), *self.class_score[c]])

        if zipf:
            zipf.write(os.path.join(self.PATH, 'Summary.csv'), 'Summary.csv', zipfile.ZIP_DEFLATED)
            os.remove(os.path.join(self.PATH, 'Summary.csv'))
        self.logger.log(os.path.join(self.PATH, 'Summary.csv') + " CSV Statisktik zur ZIP hinzugefügt.")

        self.logger.log_sep()

    def createPieChart(self, zipf=None):
        self.logger.log_sep("IMG Statistik erstellen")
        fig, ax = plt.subplots(figsize=(72, 36), subplot_kw=dict(aspect="equal"))

        data = [self.class_score[x][0] for x in self.class_score if x in self.classes]
        label = [self._getClassName(x) for x in self.class_score if x in self.classes]

        def func(pct, allvals):
            absolute = int(pct / 100. * np.sum(allvals))
            return "{:.1f}% ({:d})".format(pct, absolute)

        wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),
                                          textprops=dict(color="w"))

        legend = ax.legend(wedges, label,
                           title="Klassen",
                           loc="center left",
                           bbox_to_anchor=(1, 0, 0.5, 1),
                           prop={'size': 44});

        plt.setp(autotexts, size=34, weight="bold")
        plt.setp(legend.get_title(), fontsize=64)
        ax.text(0.3, 0.1, "Total number of objects: %d" % (np.sum(data)), fontsize=44, transform=plt.gcf().transFigure)
        ax.set_title("Klassenverteilung", fontsize=64)
        fig.savefig(os.path.join(self.PATH, 'Class Distribution.png'))

        if zipf:
            zipf.write(os.path.join(self.PATH, 'Class Distribution.png'), 'Class Distribution.png',
                       zipfile.ZIP_DEFLATED)
            os.remove(os.path.join(self.PATH, 'Class Distribution.png'))
        self.logger.log(os.path.join(self.PATH, 'Class Distribution.png') + " Diagramm zur ZIP hinzugefügt.")

        self.logger.log_sep()

    def createDataSetZIP(self, split=None, name=None):
        if not name:
            name = 'DataSet.zip'

        self.logger.log_sep(name +" erstellen")

        if split:
            t = int(len(self.label_paths) / 100 * split)
            print("t - ", t)
            train = range(t)
            shuffle(list(train))
        else:
            train = range(len(self.label_paths))

        with zipfile.ZipFile(os.path.join(self.PATH, name), 'w') as zip_file:

            for i in range(len(self.label_paths)):
                if split:
                    if i in train:
                        folder = 'Train/'
                    else:
                        folder = 'Test/'
                else:
                    folder = ''

                label = self.label_paths[i]
                xml = label.split(os.path.sep)[-1]
                img = xml[:-3] + "png"

                for ob in ET.parse(label).getroot().iter('object'):
                    try:
                        c = int(ob.find('name').text)
                        if c in self.classes:
                            img_added = []
                            zip_file.write(label, os.path.join(folder + 'Labels', xml), zipfile.ZIP_DEFLATED)

                            for p, dirs, files in os.walk(self.PATH):
                                if img in files:
                                    if img not in img_added:
                                        zip_file.write(os.path.join(p, img), os.path.join(folder + "Images", img),
                                                       zipfile.ZIP_DEFLATED)
                                        img_added.append(img)
                                    else:
                                        break
                            break
                    except Exception:
                        self.logger.log_err('Fehlerhafter Klassen bezeichner in: ' + label)

            self.createCSVOverview(zip_file)
            self.createCSVLabelMap(zip_file)

        self.logger.log_sep()

    def createCSVLabelMap(self, zipf=None):
        self.logger.log_sep("Train.csv erstellen")
        xml_list = []

        for label in self.label_paths:
            tree = ET.parse(label)
            root = tree.getroot()

            for member in root.findall('object'):
                clazz = int(member.find('name').text)

                if clazz in self.classes:
                    value = (root.find('filename').text,
                             int(root.find('size')[0].text),
                             int(root.find('size')[1].text),
                             member[0].text,
                             int(member[4][0].text),
                             int(member[4][1].text),
                             int(member[4][2].text),
                             int(member[4][3].text)
                             )
                    xml_list.append(value)
        column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
        xml_df = pd.DataFrame(xml_list, columns=column_name)
        xml_df.to_csv(os.path.join(self.PATH, 'train.csv'), index=None)

        if zipf:
            zipf.write(os.path.join(self.PATH, 'train.csv'), 'train.csv', zipfile.ZIP_DEFLATED)
            os.remove(os.path.join(self.PATH, 'train.csv'))
        self.logger.log(os.path.join(self.PATH, 'train.csv') + " Train CSV zur ZIP hinzugefügt.")

        self.logger.log_sep()
