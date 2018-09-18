import sys, os, argparse
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import numpy as np
import csv, zipfile
import pandas as pd


class Generator():

    def __init__(self, path, classes=range(1, 156)):
        self.classes = classes
        self.labelmap = {1: "speed limit 20 (prohibitory)", 2: "speed limit 30 (prohibitory)",
                         3: "speed limit 50 (prohibitory)", 4: "speed limit 60 (prohibitory)",
                         5: "speed limit 70 (prohibitory)", 6: "speed limit 80 (prohibitory)",
                         7: "restriction ends 80 (other)",
                         8: "speed limit 100 (prohibitory)", 9: "speed limit 120 (prohibitory)",
                         10: "no overtaking (prohibitory)", 11: "no overtaking (trucks) (prohibitory)",
                         12: "priority at next intersection (danger)", 13: "priority road (other)",
                         14: "give way (other)", 15: "stop (other)",
                         16: "no traffic both ways (prohibitory)", 17: "no trucks (prohibitory)",
                         18: "no entry (other)", 19: "danger (danger)",
                         20: "bend left (danger)", 21: "bend right (danger)", 22: "bend (danger)",
                         23: "uneven road (danger)", 24: "slippery road (danger)",
                         25: "road narrows (danger)", 26: "construction (danger)", 27: "traffic signal (danger)",
                         28: "pedestrian crossing (danger)", 29: "school crossing (danger)",
                         30: "cycles crossing (danger)", 31: "snow (danger)", 32: "animals (danger)",
                         33: "restriction ends (other)", 34: "go right (mandatory)",
                         35: "go left (mandatory)", 36: "go straight (mandatory)",
                         37: "go right or straight (mandatory)", 38: "go left or straight (mandatory)",
                         39: "keep right (mandatory)", 40: "keep left (mandatory)", 41: "roundabout (mandatory)",
                         42: "restriction ends (overtaking) (other)",
                         43: "restriction ends (overtaking (trucks)) (other)", 44: "restriction ends 60 (other)",
                         45: "restriction ends 70 (other)",
                         46: "speed limit 90 (prohibitory)", 47: "restriction ends 90 (other)",
                         48: "speed limit 110 (prohibitory)", 49: "restriction ends 110 (other)",
                         50: "restriction ends 120 (other)", 51: "speed limit 130 (prohibitory)",
                         52: "restriction ends 130 (other)", 53: "bend double right (danger)",
                         54: "highway turn (left) (other)", 55: "maximum width (prohibitory)",
                         56: "maximum height (prohibitory)", 57: "minimum truck distance (prohibitory)",
                         58: "highway exit 200 (other)", 59: "highway exit 100 (other)",
                         60: "right lane merging (other)", 61: "warning beacon roadwork (other)",
                         62: "speed limit 60 (digital) (prohibitory)",
                         63: "restriction ends 60 (digital) (other)", 64: "speed limit 70 (digital) (prohibitory)",
                         65: "restriction ends 70 (digital) (other)", 66: "speed limit 80 (digital) (prohibitory)",
                         67: "restriction ends 80 (digital) (other)", 68: "restriction ends 80 (digital) (other)",
                         69: "restriction ends 90 (digital) (other)", 70: "speed limit 100 (digital) (prohibitory)",
                         71: "restriction ends 100 (digital) (other)", 72: "speed limit 110 (digital) (prohibitory)",
                         73: "restriction ends 110 (digital) (other)",
                         74: "left lane merging (other)", 75: "speed limit 120 (digital) (prohibitory)",
                         76: "restriction ends 120 (digital) (other)", 77: "speed limit 130 (digital) (prohibitory)",
                         78: "restriction ends 130 (digital) (other)", 79: "no overtaking (digital) (prohibitory)",
                         80: "restriction ends 130 (digital) (other)",
                         81: "no overtaking (trucks) (digital) (prohibitory)",
                         82: "restriction ends (overtaking (trucks)) (other)", 83: "construction (digital) (danger)",
                         84: "traffic jam (digital) (danger)", 85: "highway exit (other)", 86: "traffic jam (other)",
                         87: "restriction distance (other)", 88: "restriction time (other)",
                         89: "highway exit 300m (other)", 90: "restriction ends 100 (other)",
                         91: "andreaskreuz (other)", 92: "one way street (left) (other)",
                         93: "one way street (right) (other)",
                         94: "beginning of highway (other)", 95: "end of highway (other)", 96: "busstop (other)",
                         97: "tunnel (other)", 98: "no cars (prohibitory)",
                         99: "train crossing (danger)", 100: "no bicycles (prohibitory)",
                         101: "no motorbikes (prohibitory)", 102: "no mopeds (prohibitory)",
                         103: "no horses (prohibitory)",
                         104: "no cars & motorbikes (prohibitory)", 105: "busses only (mandatory)",
                         106: "pedestrian zone (mandatory)", 107: "bicycle boulevard (mandatory)",
                         108: "end of bicycle boulevard (mandatory)", 109: "bicycle path (mandatory)",
                         110: "pedestrian path (mandatory)", 111: "pedestrian and bicycle path (mandatory)",
                         112: "separated path for bicycles and pedestrians (right) (mandatory)",
                         113: "separated path for bicycles and pedestrians (left) (mandatory)",
                         114: "play street (other)",
                         115: "end of play street (other)", 116: "beginning of motorway (other)",
                         117: "end of motorway (other)", 118: "crosswalk (zebra) (other)",
                         119: "dead-end street (other)", 120: "one way street (straight) (other)",
                         121: "priority road (other)", 122: "no stopping (prohibitory)",
                         123: "no stopping (beginning) (prohibitory)", 124: "no stopping (middle) (prohibitory)",
                         125: "no stopping (end) (prohibitory)",
                         126: "no parking (beginning) (prohibitory)", 127: "no parking (end) (prohibitory)",
                         128: "no parking (middle) (prohibitory)",
                         129: "no parking (prohibitory)", 130: "no parking zone (prohibitory)",
                         131: "end of no parking zone (prohibitory)", 132: "city limit (in) (other)",
                         133: "city limit (out) (other)", 134: "direction to village (other)",
                         135: "rural road exit (other)", 136: "speed limit 20 zone (prohibitory)",
                         137: "end speed limit 20 zone (prohibitory)", 138: "speed limit 30 zone (prohibitory)",
                         139: "end speed limit 30 zone (prohibitory)",
                         140: "speed limit 5 (prohibitory)", 141: "speed limit 10 (prohibitory)",
                         142: "restriction ends 10 (other)", 143: "restriction ends 20 (other)",
                         144: "restriction ends 30 (other)",
                         145: "speed limit 40 (prohibitory)", 146: "restriction ends 40 (other)",
                         147: "restriction ends 50 (other)", 148: "go left (now) (mandatory)",
                         149: "go right (now) (mandatory)",
                         150: "train crossing in 300m (other)", 151: "train crossing in 200m (other)",
                         152: "train crossing in 100m (other)", 153: "danger (digital) (danger)",
                         154: "restriction ends 100 (other)", 155: "highway turn (right) (other)"}

        self.PATH = path
        self.label_names = []
        self.label_paths = []

        for p, dirs, filenames in os.walk(self.PATH):
            self.label_names += [f for f in filenames if f[-3:] == 'xml']
            self.label_paths += [os.path.join(p, f) for f in filenames if f[-3:] == 'xml']

        self.class_score = self._calculateClassScore()

    def deleteEmptyImages(self, path=None):
        if not path:
            path = self.PATH

        for p, dirs, filenames in os.walk(path):
            for file in [f for f in filenames if f[-3:] == 'png']:
                if file[:-3] + 'xml' not in self.label_names:
                    os.remove(os.path.join(p, file))
                    print("%i deleted due to missing label!" % (os.path.join(p, file)))

    def _calculateClassScore(self, ):
        class_score = {}

        for label in self.label_paths:

            for ob in ET.parse(label).getroot().iter('object'):

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
            return "Unknown"

    def createCSVOverview(self, zipf=None):

        with open(os.path.join(self.PATH, "Summary.csv"), 'w', newline='') as out:
            writer = csv.writer(out, delimiter=',', quoting=csv.QUOTE_NONE)
            writer.writerow(['Class ID', 'Class Name', 'Frequenzy', 'Avg Xmin', 'Avg Ymin', 'Avg Xmax', 'Avg Ymax'])
            for c in self.class_score:
                if c in self.classes:
                    writer.writerow([c, self._getClassName(c), *self.class_score[c]])

        if zipf:
            zipf.write(os.path.join(self.PATH, 'Summary.csv'), 'Summary.csv', zipfile.ZIP_DEFLATED)
            os.remove(os.path.join(self.PATH, 'Summary.csv'))
        print("CSV Overview successfully created.")

    def createPieChart(self, zipf=None):
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
        print("Pie chart successfully created.")

    def createDataSetZIP(self):
        with zipfile.ZipFile(os.path.join(self.PATH, "DataSet.zip"), 'w') as zip_file:

            for label in self.label_paths:
                xml = label.split(os.path.sep)[-1]
                img = xml[:-3] + "png"

                for ob in ET.parse(label).getroot().iter('object'):
                    c = int(ob.find('name').text)
                    if c in self.classes:
                        img_added = []
                        zip_file.write(label, os.path.join('Labels', xml), zipfile.ZIP_DEFLATED)
                        for p, dirs, files in os.walk(self.PATH):
                            if img in files:
                                if img not in img_added:
                                    zip_file.write(os.path.join(p, img), os.path.join("Images", img),
                                                   zipfile.ZIP_DEFLATED)
                                    img_added.append(img)
                                else:
                                    break
                        break

            self.createPieChart(zip_file)
            self.createCSVOverview(zip_file)
            self.createCSVLabelMap(zip_file)

    def createCSVLabelMap(self, zipf=None):
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
            zipf.write(os.path.join(self.PATH, 'train.csv'), 'labels.csv', zipfile.ZIP_DEFLATED)
            os.remove(os.path.join(self.PATH, 'train.csv'))
        print("Label CSV successfully created.")


class FullPaths(argparse.Action):
    """Expand user- and relative-paths"""
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, os.path.abspath(os.path.expanduser(values)))


def is_dir(dirname):
    """Checks if a path is an actual directory"""
    if not os.path.isdir(dirname):
        msg = "{0} is not a directory".format(dirname)
        raise argparse.ArgumentTypeError(msg)
    else:
        return dirname


def main(argv):
    parser = argparse.ArgumentParser(description='Generate Data Sets for Object detection!')
    parser.add_argument('-p', help="Pfad zum Ordner des Datasets.", action=FullPaths, type=is_dir, metavar='PATH')

    parser.add_argument('-c', help="Bestimmte Klassen setzen.", metavar='classes', type=int, nargs='*')
    parser.add_argument('--zip', help='Komplettes Datenset als zip erstellen.', dest='zip', action='store_true')
    parser.add_argument('--stat_csv', help='Klassen Statistik als csv erstellen.', dest='csv', action='store_true')
    parser.add_argument('--stat_img', help='Klassen Statistik als png erstellen.', dest='img', action='store_true')
    parser.add_argument('--del_img', help='Bilder ohne Label löschen.', dest='delete', action='store_true')
    parser.add_argument('--train_csv', help='Train.csv für Object Detection erstellen.', dest='train', action='store_true')

    args = parser.parse_args(argv)

    if args.c:
        generator = Generator(args.p, args.c)
    else:
        generator = Generator(args.p)

    if args.delete:
        generator.deleteEmptyImages()

    if args.zip:
        generator.createDataSetZIP()

    if args.csv:
        generator.createCSVOverview()

    if args.img:
        generator.createPieChart()

    if args.train:
        generator.createCSVLabelMap()


if __name__ == '__main__':
    main(sys.argv[1:])