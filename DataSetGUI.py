import sys, os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, Qt
from Generator import Generator
from GuiLogger import  GuiLogger

class DSGView(QWidget):

    def __init__(self):
        self.selectedPathes = []
        self.logger = GuiLogger(self)
        super().__init__()
        self.generator = None
        self.directory = ""

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.path_label = QLabel('Arbeitsverzeichnis')
        self.set_path_btn = QPushButton("Pfad wählen")
        self.set_path_btn.clicked.connect(self.on_set_path)
        self.path = QLineEdit()

        self.grid.addWidget(self.path_label, 1, 0, 1, 2)
        self.grid.addWidget(self.path, 1, 2, 1, 5)
        self.grid.addWidget(self.set_path_btn, 1, 7)

        self.file_model = QFileSystemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setStyleSheet('color: black')
        self.tree_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tree_view.selectionModel().selectionChanged.connect(self.getItems)
        self.tree_view.doubleClicked.connect(self.on_double_click)
        self.tree_view.setVisible(False)
        self.grid.addWidget(self.tree_view, 2, 2, 5, 5)

        self.error = QTextEdit()
        self.error.setLineWrapColumnOrWidth(200)
        self.error.setMaximumHeight(50)
        self.error.setLineWrapMode(QTextEdit.FixedColumnWidth)
        self.grid.addWidget(self.error, 7, 2, 1, 5)

        self.dataset_btn = QPushButton('Datenset erzeugen')
        self.dataset_btn.setEnabled(False)
        self.dataset_btn.clicked.connect(self.on_dataset)
        self.grid.addWidget(self.dataset_btn, 7, 7, 1, 1, Qt.AlignBottom)

        self.delete_images_btn = QPushButton("Leere Bilder löschen")
        self.delete_images_btn.setEnabled(False)
        self.delete_images_btn.clicked.connect(self.on_delete_img)
        self.grid.addWidget(self.delete_images_btn, 3, 0, 1, 2)

        self.create_stat_btn = QPushButton('Statistik erzeugen')
        self.create_stat_btn.setEnabled(False)
        self.create_stat_btn.clicked.connect(self.on_create_stat)
        self.grid.addWidget(self.create_stat_btn, 4, 0, 1, 2)

        self.train_btn = QPushButton('Train.csv erstellen')
        self.train_btn.setEnabled(False)
        self.train_btn.clicked.connect(self.on_create_train)
        self.grid.addWidget(self.train_btn, 5, 0, 1, 2)

        self.setLayout(self.grid)
        self.setGeometry(150, 150, 900, 450)
        self.setWindowTitle('Data Set Generator')

        self.up_btn = QToolButton()
        self.up_btn.setArrowType(Qt.UpArrow)
        self.up_btn.setEnabled(False)
        self.up_btn.clicked.connect(self.on_navi_up)
        self.grid.addWidget(self.up_btn, 2, 1)

    def on_set_path(self):
        self.directory = str(QFileDialog.getExistingDirectory(self, "Arbeitsverzeichnis wählen"))

        self.up_btn.setEnabled(True)
        self.dataset_btn.setEnabled(True)
        self.delete_images_btn.setEnabled(True)
        self.tree_view.setVisible(True)
        self.create_stat_btn.setEnabled(True)
        self.train_btn.setEnabled(True)

        self._update_path(self.directory)

    def on_dataset(self):
        if self.selectedPathes:
            for p in self.selectedPathes:
                if os.path.isdir(p):
                    self.generator = Generator(p)
                    self.generator.createDataSetZIP()
                    self.logger.log(p+"/Dataset.zip erstellt.")
        else:
            self.generator = Generator(self.directory)
            self.generator.createDataSetZIP()

    def on_delete_img(self):
        deleted = []

        if self.selectedPathes:
            for p in self.selectedPathes:
                if os.path.isdir(p):
                    self.generator = Generator(p)
                    deleted += self.generator.deleteEmptyImages()
        else:
            self.generator = Generator(self.directory)
            deleted+=self.generator.deleteEmptyImages()

        if deleted:
            msg = 'Gelöschte Bilder:\n' + '\n'.join(deleted)
            self.error.setText(msg)
            self.error.setStyleSheet('color: green')
        else:
            self.error.setText('Keine leeren Bilder gefunden!')
            self.error.setStyleSheet('color: green')

    def on_create_stat(self):
        choices = ['Graphische Statistik', 'CSV Statistik', 'Beides']
        item, okPressed = QInputDialog.getItem(self, 'Statistik auswählen!', 'Statistik:', choices, 0, False)

        if okPressed and item:
            if self.selectedPathes:
                for p in self.selectedPathes:
                    if os.path.isdir(p):
                        self.generator = Generator(p)
                        if item != choices[1]:
                            self.generator.createPieChart()
                            self.logger.log(p+"/Class Distribution.png erstellt!")
                        if item != choices[0]:
                            self.generator.createCSVOverview()
                            self.logger.log(p + "/Summary.csv erstellt!")

            else:
                self.generator = Generator(self.directory)
                if item != choices[1]:
                    self.generator.createPieChart()
                    self.logger.log(self.directory + "/Class Distribution.png erstellt!")
                if item != choices[0]:
                    self.generator.createCSVOverview()
                    self.logger.log(self.directory + "/Summary.csv erstellt!")

    def on_create_train(self):
        msg = ""
        if self.selectedPathes:
            for p in self.selectedPathes:
                if os.path.isdir(p):
                    self.generator = Generator(p)
                    self.generator.createCSVLabelMap()
                    self.logger.log(p+'/train.csv wurde erstellt.')
        else:
            self.generator = Generator(self.directory)
            self.generator.createCSVLabelMap()
            self.logger.log(self.directory+'/train.csv wurde erstellt.')


    def getItems(self):
        selected = self.tree_view.selectionModel().selectedIndexes()
        new = []
        for index in selected:
            path = self.sender().model().filePath(index)
            if path not in new:
                new.append(path)
        self.selectedPathes = new

    def on_double_click(self):
        for index in self.tree_view.selectionModel().selectedIndexes():
            self.directory = self.sender().model().filePath(index)
        self._update_path(self.directory)
        self.selectedPathes = []
        self.tree_view.clearSelection()
        self.logger.clear()

    def on_navi_up(self):
        self.directory = '/'.join(self.directory.split('/')[:-1])
        self._update_path(self.directory)

    def _update_path(self,path):
        self.path.setText(path)
        self.directory = path
        self.file_model.setRootPath(self.directory)
        self.tree_view.setRootIndex(self.file_model.index(self.directory))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DSGView()
    ex.show()
    sys.exit(app.exec_())
