import os
import sys
from PyQt4 import QtGui, QtCore
from main_window import Ui_MainWindow
from multiprocessing import Process

if (os.name == 'nt'):
    import vtk
    vtk.vtkObject.GlobalWarningDisplayOff()
import compute_areas

class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, *args):
        super(MainWindow, self).__init__(*args)
        Ui_MainWindow.setupUi(self, self)
        self.last_dir = os.path.expanduser("~")
        self.connect_signals()

    def connect_signals(self):
        self.one_vrml_button.clicked.connect(lambda: self.open_dialog(self.one_vrml_input, "*.vrml"))
        self.one_csv_button.clicked.connect(lambda: self.save_dialog(self.one_csv_input, "*.csv"))
        self.many_vrml_button.clicked.connect(lambda: self.open_dir_dialog(self.many_vrml_input))
        self.many_csv_button.clicked.connect(lambda: self.open_dir_dialog(self.many_csv_input))
        self.one_run_button.clicked.connect(lambda: self.run("one"))
        self.many_run_button.clicked.connect(lambda: self.run("many"))

    def run(self, kind):
        args = []
        if kind == "one":
            if not os.path.isfile(self.one_vrml_input.text()):
                self.one_vrml_input.setFocus()
                return
            if self.one_csv_input.text() == "":
                self.one_csv_input.setFocus()
                return

            args = ["-a", "{}".format(self.one_csv_input.text()),
                    "-i", "{}".format(self.one_vrml_input.text())]
        if kind == "many":
            if not os.path.isdir(self.many_vrml_input.text()):
                self.many_vrml_input.setFocus()
                return
            if not os.path.isdir(self.many_csv_input.text()):
                self.many_csv_input.setFocus()
                return

            args = ["-o", "{}".format(self.many_csv_input.text()),
                    "-d", "{}".format(self.many_vrml_input.text())]

        print "python compute_areas.py " + " ".join(args)
        p = Process(target=compute_areas.main, args=[args])
        p.start()
        self.statusBar.clearMessage()
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.tabWidget.setDisabled(True)
        self.check_running(p)


    def check_running(self, p):
        if p.is_alive():
            QtCore.QTimer.singleShot(250, lambda: self.check_running(p))
        else:
            p.join()
            if p.exitcode != 0:
                self.statusBar.showMessage("ERROR: There was an error computing Areas, try with other VRML")
            self.tabWidget.setDisabled(False)
            QtGui.QApplication.restoreOverrideCursor()

    def _handle_file_path(self, file_path):
        file = unicode(file_path, sys.getfilesystemencoding())  # To unicode
        file = file.encode(sys.getfilesystemencoding())  # To latin-1 if needed
        self.last_dir = os.path.dirname(file)
        return file

    def open_dialog(self, target, filter):
        file = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                                                 self.last_dir, filter)  # QtCore.QString
        file = self._handle_file_path(file)
        target.setText(file)

    def save_dialog(self, target, filter):
        file = QtGui.QFileDialog.getSaveFileName(self, "Save File",
                                                 self.last_dir, filter)  # QtCore.QString
        file = self._handle_file_path(file)
        target.setText(file)

    def open_dir_dialog(self, target):
        file = QtGui.QFileDialog.getExistingDirectory(self, "Open Folder", self.last_dir)  # QtCore.QString
        file = self._handle_file_path(file)
        target.setText(file)


def main():
    app = QtGui.QApplication(sys.argv)
    mw = MainWindow()
    # mw.one_vrml_input.setText("/home/jmorales/sets/vrmls/humanas-cingular/Api/api if6 1 8enero LONGS.vrml")
    # mw.one_csv_input.setText("/tmp/paco.csv")
    mw.show()
    app.exec_()

if __name__ == '__main__':
    main()
