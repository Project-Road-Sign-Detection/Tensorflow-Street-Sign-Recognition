"""An example of how to use models and views in PyQt4.
Model/view documentation can be found at
http://doc.qt.nokia.com/latest/model-view-programming.html.
"""
import sys

from PyQt5.QtWidgets import (QApplication, QColumnView, QFileSystemModel,
                             QSplitter, QTreeView)
from PyQt5.QtCore import QDir, Qt

if __name__ == '__main__':
    app = QApplication(sys.argv)
    # Splitter to show 2 views in same widget easily.
    splitter = QSplitter()
    # The model.
    model = QFileSystemModel()
    # You can setRootPath to any path.
    model.setRootPath(QDir.rootPath())
    # List of views.
    views = []
    for ViewType in (QColumnView, QTreeView):
        # Create the view in the splitter.
        view = ViewType(splitter)
        # Set the model of the view.
        view.setModel(model)
        # Set the root index of the view as the user's home directory.
        view.setRootIndex(model.index(QDir.homePath()))
    # Show the splitter.
    splitter.show()
    # Maximize the splitter.
    splitter.setWindowState(Qt.WindowMaximized)
    # Start the main loop.
    sys.exit(app.exec_())
