import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QTextCursor
from PyQt5 import QtCore

form_class = uic.loadUiType("C:\\Users\\최재혁\\PycharmProjects\\Final\\main.ui")[0]
class findWindow(QDialog):
    def __init__(self, parent):
        super(findWindow, self).__init__(parent)
        uic.loadUi("C:\\Users\\최재혁\\PycharmProjects\\Final\\find.ui", self)
        self.show()
        self.parent = parent
        self.cursor = parent.plainTextEdit.textCursor()
        self.pe = parent.plainTextEdit

        self.pushButton_findnext.clicked.connect(self.findNext)
        self.pushButton_cancel.clicked.connect(self.close)

        self.radioButton_down.clicked.connect(self.updown_radio_button)
        self.radioButton_up.clicked.connect(self.updown_radio_button)
        self.up_down = "down"

    def updown_radio_button(self):
        if self.radioButton_up.isChecked():
            self.up_down = "up"
        elif self.radioButton_down.isChecked():
            self.up_down = "down"

    def keyReleaseEvent(self, event):
        if self.lineEdit.text():
            self.pushButton_findnext.setEnabled(True)
        else:
            self.pushButton_findnext.setEnabled(False)

    def findNext(self):
        pattern = self.lineEdit.text()
        text = self.pe.toPlainText()
        reg = QtCore.QRegExp(pattern)
        self.cursor = self.parent.plainTextEdit.textCursor()

        if self.checkBox_CaseSensitive.isChecked():
             cs = QtCore.Qt.CaseSensitive
        else:
             cs = QtCore.Qt.CaseInsensitive

        reg.setCaseSensitivity(cs)
        pos = self.cursor.position()
        index = reg.indexIn(text, 0)   # 검색

        if index != -1:  # 검색된 결과가 없다면
            self.setCursor(index, len(pattern)+index)


    def setCursor(self, start, end):
        print(self.cursor.selectionStart(), self.cursor.selectionEnd())
        self.cursor.setPosition(start)  # 앞에 커서를 찍고
        self.cursor.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor, end-start)  # 뒤로 커서를 움직인다
        self.pe.setTextCursor(self.cursor)


class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.action_open.triggered.connect(self.openFunction)
        self.action_save.triggered.connect(self.saveFunction)
        self.action_saveas.triggered.connect(self.saveAsFunction)
        self.action_close.triggered.connect(self.close)
        self.action_undo.triggered.connect(self.undoFunction)
        self.action_cut.triggered.connect(self.cutFunction)
        self.action_copy.triggered.connect(self.copyFunction)
        self.action_paste.triggered.connect(self.pasteFunction)
        self.action_find.triggered.connect(self.findFunction)

        self.opened = False
        self.opened_file_path = '제목 없음'

    def ischanged(self):
        if not self.opened:
            if self.plainTextEdit.toPlainText().strip():  # 열린적은 없는데 에디터 내용이 있으면
                return True
            return False

        # 현재 데이터
        current_data = self.plainTextEdit.toPlainText()

        # 파일에 저장된 데이터터
        with open(self.opened_file_path, encoding='UTF8') as f:
            file_data = f.read()

        if current_data == file_data:  # 열린적이 있고 변경사항이 없으면
            return False
        else:  # 열린적이 있고 변경사항이 있으면
            return True


    def save_changed_data(self):
        msgBox = QMessageBox()
        msgBox.setText("변경 내용을 {}애 저장하시겠습니까?".format(self.opened_file_path))
        msgBox.addButton('저장', QMessageBox.YesRole)
        msgBox.addButton('저장 안 함', QMessageBox.NoRole)
        msgBox.addButton('취소', QMessageBox.RejectRole)
        ret = msgBox.exec_()

        if ret == 0:
            self.saveFunction()
        else:
            return ret


    def closeEvent(self, event):
        if self.ischanged():
            ret = self.save_changed_data()

            if ret == 2:
                event.ignore()


    def save_file(self, fname):
        data = self.plainTextEdit.toPlainText()

        with open(fname, 'w', encoding='UTF8') as f:
            f.write(data)
        self.opened = True
        self.opened_file_path = fname

    def open_file(self, fname):
        with open(fname, encoding='UTF8') as f:
            data = f.read()
        self.plainTextEdit.setPlainText(data)
        self.opened = True
        self.opened_file_path = fname

    def openFunction(self):
        if self.ischanged():
            ret = self.save_changed_data()

        fname = QFileDialog.getOpenFileName(self)
        if fname[0]:
            self.open_file(fname[0])

    def saveFunction(self):
        if self.opened:
            self.save_file(self.opened_file_path)
        else:
            self.saveAsFunction()

    def saveAsFunction(self):
        fname = QFileDialog.getSaveFileName(self)
        if fname[0]:
            self.save_file(fname[0])

    def undoFunction(self):
        self.plainTextEdit.undo()

    def cutFunction(self):
        self.plainTextEdit.cut()

    def copyFunction(self):
        self.plainTextEdit.copy()

    def pasteFunction(self):
        self.plainTextEdit.paste()

    def findFunction(self):
        findWindow(self)


app = QApplication(sys.argv)
mainWindow = WindowClass()
mainWindow.show()
app.exec_()