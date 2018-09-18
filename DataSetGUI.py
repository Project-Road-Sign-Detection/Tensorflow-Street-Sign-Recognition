import sys

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDir, Qt
from Generator import Generator

class DSGView(QWidget):

    def __init__(self):
        super().__init__()
        self.generator = None
        self.directory = ""

        self.grid = QGridLayout()
        self.grid.setSpacing(10)

        self.path_label = QLabel('Arbeitsverzeichnis')
        self.set_path_btn = QPushButton("Pfad wählen")
        self.set_path_btn.clicked.connect(self.on_set_path)
        self.path = QLineEdit()

        self.grid.addWidget(self.path_label, 1, 0)
        self.grid.addWidget(self.path, 1, 1, 1, 3)
        self.grid.addWidget(self.set_path_btn, 1, 4)

        self.file_model = QFileSystemModel()
        self.tree_view = QTreeView()
        self.tree_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.tree_view.setVisible(False)
        self.grid.addWidget(self.tree_view, 2, 1, 5, 3)

        self.dataset_btn = QPushButton('Datenset erzeugen')
        self.dataset_btn.setEnabled(False)
        self.dataset_btn.clicked.connect(self.on_dataset)
        self.grid.addWidget(self.dataset_btn, 7, 4)

        self.delete_images_btn = QPushButton("Leere Bilder löschen")
        self.delete_images_btn.setEnabled(False)
        self.delete_images_btn.clicked.connect(self.on_delete_img)
        self.grid.addWidget(self.delete_images_btn, 3, 0)

        self.setLayout(self.grid)
        self.setGeometry(300, 300, 700, 350)
        self.setWindowTitle('Data Set Generator')

    def on_set_path(self):
        self.directory = str(QFileDialog.getExistingDirectory(self, "Arbeitsverzeichnis wählen"))
        self.path.setText(self.directory)

        self.dataset_btn.setEnabled(True)
        self.delete_images_btn.setEnabled(True)

        self.file_model.setRootPath(self.directory)
        self.tree_view.setModel(self.file_model)
        self.tree_view.setRootIndex(self.file_model.index(self.directory))
        self.tree_view.setVisible(True)

    def on_dataset(self):
        self.generator = Generator(self.directory)
        print(self.generator.__class__)
        self.generator.createDataSetZIP()

    def on_delete_img(self):
        print(self.file_model.filePath(self.file_model.index()))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = DSGView()
    ex.show()
    sys.exit(app.exec_())
