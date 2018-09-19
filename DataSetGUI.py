import sys, os

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, Qt
from Generator import Generator

class DSGView(QWidget):

    def __init__(self):
        self.selectedPathes = []
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
        self.grid.addWidget(self.path, 1, 2, 1, 3)
        self.grid.addWidget(self.set_path_btn, 1, 5)

        self.file_model = QFileSystemModel()
        self.tree_view = QTreeView()
        self.tree_view.setModel(self.file_model)
        self.tree_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tree_view.selectionModel().selectionChanged.connect(self.getItems)
        self.tree_view.doubleClicked.connect(self.on_double_click)
        self.tree_view.setVisible(False)
        self.grid.addWidget(self.tree_view, 2, 2, 5, 4)

        self.error = QTextEdit()
        self.error.setLineWrapColumnOrWidth(200)
        self.error.setMaximumHeight(50)
        self.error.setLineWrapMode(QTextEdit.FixedColumnWidth)
        self.grid.addWidget(self.error, 7, 2, 1, 3)

        self.dataset_btn = QPushButton('Datenset erzeugen')
        self.dataset_btn.setEnabled(False)
        self.dataset_btn.clicked.connect(self.on_dataset)
        self.grid.addWidget(self.dataset_btn, 7, 5, 1, 1, Qt.AlignBottom)

        self.delete_images_btn = QPushButton("Leere Bilder löschen")
        self.delete_images_btn.setEnabled(False)
        self.delete_images_btn.clicked.connect(self.on_delete_img)
        self.grid.addWidget(self.delete_images_btn, 3, 0, 1, 2)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 700, 450)
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

        self._update_path(self.directory)

    def on_dataset(self):
        self.generator = Generator(self.directory)
        self.generator.createDataSetZIP()

    def on_delete_img(self):
        self.generator = Generator(self.directory)
        deleted = self.generator.deleteEmptyImages()
        print(deleted)
        if deleted:
            msg = 'Gelöschte Bilder:\n' + '\n'.join(deleted)
            print(msg)
            self.error.setText(msg)
            self.error.setStyleSheet('color: green')
        else:
            self.error.setText('Keine leeren Bilder gefunden!')
            self.error.setStyleSheet('color: green')

    def getItems(self):
        selected = self.tree_view.selectionModel().selectedIndexes()
        for index in selected:
            path = self.sender().model().filePath(index)
            if path not in self.selectedPathes:
                self.selectedPathes.append(path)
        print(self.selectedPathes)

    def on_double_click(self):
        for index in self.tree_view.selectionModel().selectedIndexes():
            self.directory = self.sender().model().filePath(index)
        self._update_path(self.directory)

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
