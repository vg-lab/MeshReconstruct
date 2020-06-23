import os
import sys
from PyQt5 import QtGui, QtCore, QtWidgets
from main_window import Ui_MainWindow
from multiprocessing import Process
from builtins import str

if (os.name == 'nt'):
    import vtk

    vtk.vtkObject.GlobalWarningDisplayOff()
import compute_areas


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parameters, *args):
        super(MainWindow, self).__init__(*args)
        Ui_MainWindow.setupUi(self, self)
        self.last_dir = os.path.expanduser("~")
        self.connect_signals()
        if not parameters:
            self.precisionSpinBox.hide()
            self.precisionLabel.hide()
            self.exportResolutionLabel.hide()
            self.exportReductionDoubleSpinBox.hide()
            self.includeSegmentsCheckBox.hide()
            self.includeSegmentsLabel.hide()
            self.kernelSizeSpinBox.hide()
            self.kernelSizeLabel.hide()
            self.cleanVrmlCheckBox.hide()
            self.cleanVrmlLabel.hide()

    def connect_signals(self):
        self.one_vrml_button.clicked.connect(lambda: self.open_dialog(self.one_vrml_input, "*.vrml *.imx"))
        self.one_vrml_csv_button.clicked.connect(lambda: self.save_dialog(self.one_vrml_csv_input, "*.csv"))
        self.many_vrml_button.clicked.connect(lambda: self.open_dir_dialog(self.many_vrml_input))
        self.many_vrml_csv_button.clicked.connect(lambda: self.open_dir_dialog(self.many_vrml_csv_input))
        self.one_vrml_run_button.clicked.connect(lambda: self.run("one_vrml"))
        self.many_vrml_run_button.clicked.connect(lambda: self.run("many_vrml"))

    def run(self, kind):
        args = []

        if kind == "one_vrml":
            if not os.path.isfile(self.one_vrml_input.text()):
                self.one_vrml_input.setFocus()
                return
            if self.one_vrml_csv_input.text() == "":
                self.one_vrml_csv_input.setFocus()
                return
            args = ["-a", "{}".format(self.one_vrml_csv_input.text()),
                    "-v", "{}".format(self.one_vrml_input.text()),
                    "-s", "{}".format(self.outputFormatComboBox.currentText()),
                    "-p", "{}".format(self.precisionSpinBox.value()),
                    "-r", "{}".format(self.exportReductionDoubleSpinBox.value()),
                    "-f", "{}".format(self.includeSegmentsCheckBox.isChecked()),
                    "-k", "{}".format(self.kernelSizeSpinBox.value()),
                    "-c", "{}".format(self.cleanVrmlCheckBox.isChecked())]

        if kind == "many_vrml":
            if not os.path.isdir(self.many_vrml_input.text()):
                self.many_vrml_input.setFocus()
                return
            if not os.path.isdir(self.many_vrml_csv_input.text()):
                self.many_vrml_csv_input.setFocus()
                return
            args = ["-o", "{}".format(self.many_vrml_csv_input.text()),
                    "-w", "{}".format(self.many_vrml_input.text()),
                    "-s", "{}".format(self.outputFormatComboBox.currentText()),
                    "-p", "{}".format(self.precisionSpinBox.value()),
                    "-r", "{}".format(self.exportReductionDoubleSpinBox.value()),
                    "-f", "{}".format(self.includeSegmentsCheckBox.isChecked()),
                    "-k", "{}".format(self.kernelSizeSpinBox.value()),
                    "-c", "{}".format(self.cleanVrmlCheckBox.isChecked())]

        print("python compute_areas.py " + " ".join(args))

        p = Process(target=compute_areas.main, args=[args])
        p.start()

        self.statusBar.clearMessage()
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.WaitCursor))
        self.tabWidget.setDisabled(True)
        self.check_running(p)

    def check_running(self, p):
        if p.is_alive():
            QtCore.QTimer.singleShot(250, lambda: self.check_running(p))
        else:
            p.join()
            if p.exitcode != 0:
                self.statusBar.showMessage("ERROR: There was an error computing Areas, try with other vrml/imx")
            self.tabWidget.setDisabled(False)
            QtWidgets.QApplication.restoreOverrideCursor()

    def _handle_file_path(self, file_path):
        if type(file_path) is tuple:
            file = file_path[0]
        else:
            file = file_path

        self.last_dir = os.path.dirname(file)
        return file

    def open_dialog(self, target, filter):
        file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File",
                                                     self.last_dir, filter)  # QtCore.QString
        file = self._handle_file_path(file)
        target.setText(file)

    def save_dialog(self, target, filter):
        file = QtWidgets.QFileDialog.getSaveFileName(self, "Save File",
                                                     self.last_dir, filter)  # QtCore.QString
        file = self._handle_file_path(file)
        target.setText(file)

    def open_dir_dialog(self, target):
        file = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Folder", self.last_dir)  # QtCore.QString
        file = self._handle_file_path(file)
        target.setText(file)


def main(argv):
    app = QtWidgets.QApplication(sys.argv)
    mw = MainWindow("-p" in argv)
    # mw.one_imx_input.setText("/home/jmorales/sets/imxs/humanas-cingular/Api/api if6 1 8enero LONGS.imx")
    # mw.one_csv_input.setText("/tmp/paco.csv")
    mw.show()
    app.exec_()


if __name__ == '__main__':
    main(sys.argv)
