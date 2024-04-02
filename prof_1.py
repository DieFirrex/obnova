import sys
import json
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from prof_ import Ui_MainWindow

class ProfileApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.label.setText("Введіть ім'я")
        self.label_2.setText("Введіть вік")
        self.label_3.setText("Опис себе")
        self.label_4.setText("Редагування профілю")
        self.pushButton.setText('Зберегти')
        self.pushButton.clicked.connect(self.save_profile)

    def save_profile(self):
        name = self.lineEdit.text()
        age = self.spinBox.value()
        description = self.textEdit.toPlainText()

        if name and description:
            account, ok = QInputDialog.getText(self, 'Вибір акаунту', 'Введіть назву акаунту:')
            if ok:
                profile = {
                    "name": name,
                    "age": age,
                    "description": description
                }
                profiles = {}
                try:
                    with open('profiles.json', 'r') as file:
                        profiles = json.load(file)
                except FileNotFoundError:
                    pass

                profiles[account] = profile

                with open('profiles.json', 'w') as file:
                    json.dump(profiles, file, indent=4)

                QMessageBox.information(self, "Збережено", "Ваш профіль успішно збережено!")
        else:
            QMessageBox.warning(self, "Помилка", "Ім'я та опис обов'язкові до заповнення!")

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ProfileApp()
    window.show()
    sys.exit(app.exec_())
