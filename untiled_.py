import json
from PyQt5 import QtWidgets, QtCore
import subprocess
import untiled


class ChangePasswordDialog(QtWidgets.QDialog):
    def __init__(self, accounts, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Зміна паролю")
        
        self.account_combo = QtWidgets.QComboBox(self)
        self.account_combo.addItems(accounts)
        
        self.old_password_edit = QtWidgets.QLineEdit(self)
        self.old_password_edit.setPlaceholderText("Старий пароль")
        
        self.new_password_edit = QtWidgets.QLineEdit(self)
        self.new_password_edit.setPlaceholderText("Новий пароль")
        
        self.ok_button = QtWidgets.QPushButton('Ок')
        self.cancel_button = QtWidgets.QPushButton('Відміна')
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.account_combo)
        layout.addWidget(self.old_password_edit)
        layout.addWidget(self.new_password_edit)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return (
            self.account_combo.currentText(),
            self.old_password_edit.text(),
            self.new_password_edit.text()
        )

class ChangeAccountDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Зміна акаунту")
        
        self.old_account_edit = QtWidgets.QLineEdit(self)
        self.old_account_edit.setPlaceholderText("Старий акаунт")
        
        self.old_password_edit = QtWidgets.QLineEdit(self)
        self.old_password_edit.setPlaceholderText("Пароль")
        
        self.new_account_edit = QtWidgets.QLineEdit(self)
        self.new_account_edit.setPlaceholderText("Новий акаунт")
        
        self.ok_button = QtWidgets.QPushButton('Ок')
        self.cancel_button = QtWidgets.QPushButton('Відміна')
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.old_account_edit)
        layout.addWidget(self.old_password_edit)
        layout.addWidget(self.new_account_edit)
        layout.addWidget(self.ok_button)
        layout.addWidget(self.cancel_button)

    def get_data(self):
        return (
            self.old_account_edit.text(),
            self.old_password_edit.text(),
            self.new_account_edit.text()
        )

class profil(QtWidgets.QMainWindow, untiled.Ui_MainWindow):
    def __init__(self):
        super(profil, self).__init__()
        # Ініціалізуємо інтерфейс
        self.setupUi(self)
        # Встановлюємо текст та параметри елементів інтерфейсу
        self.label.setText('Виберіть дію')
        self.pushButton.setText('Змінити пароль')
        self.pushButton_2.setText('Змінити назву акаунту')
        self.pushButton_3.setText('Створення профілю')
        self.pushButton_4.setText('Видалити акаунт')

        # Створюємо комбінований список для вибору акаунтів
        self.account_combo = QtWidgets.QComboBox(self)

        # Під'єднуємо кнопки до відповідних методів
        self.pushButton.clicked.connect(self.change_password_dialog)
        self.pushButton_2.clicked.connect(self.change_account_dialog)
        self.pushButton_3.clicked.connect(self.open_profile_file)
        self.pushButton_4.clicked.connect(self.delete_account_dialog)

    def open_profile_file(self):
        subprocess.Popen(["python", "prof_1.py"])

    def change_password_dialog(self):
        # Отримуємо список акаунтів для вибору
        accounts = [self.account_combo.itemText(i) for i in range(self.account_combo.count())]
        dialog = ChangePasswordDialog(accounts, self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            account, old_password, new_password = dialog.get_data()
            self.change_password(account, old_password, new_password)

    def change_account_dialog(self):
        dialog = ChangeAccountDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            old_account, old_password, new_account = dialog.get_data()
            self.change_account(old_account, old_password, new_account)

    def change_password(self, account, old_password, new_password):
        try:
            with open('akaunt.json', 'r') as f:
                data = json.load(f)
                for user in data['users']:
                    if user['login'] == account and user['password'] == old_password:
                        user['password'] = new_password
                        break
                
            with open('akaunt.json', 'w') as f:
                json.dump(data, f, indent=4)
                QtWidgets.QMessageBox.information(self, "Зміна паролю", "Пароль успішно змінено!")
        except FileNotFoundError:
            print("Файл бази даних не знайдено.")
        except Exception as e:
            print("Помилка при зміні паролю:", e)

    def change_account(self, old_account, old_password, new_account):
        try:
            with open('akaunt.json', 'r') as f:
                data = json.load(f)
                for user in data['users']:
                    if user['login'] == old_account and user['password'] == old_password:
                        # Перевіряємо унікальність нового імені акаунту
                        if any(account['login'] == new_account for account in data['users']):
                            QtWidgets.QMessageBox.warning(self, "Помилка", f"Акаунт з ім'ям '{new_account}' вже існує. Будь ласка, виберіть інше ім'я.")
                            return
                        else:
                            user['login'] = new_account
                            break

            with open('akaunt.json', 'w') as f:
                json.dump(data, f, indent=4)
                QtWidgets.QMessageBox.information(self, "Зміна акаунту", "Назва акаунту успішно змінена!")
                
            # Також змінюємо ім'я акаунту в файлі profiles.json
            with open('profiles.json', 'r') as f:
                profiles_data = json.load(f)
                if old_account in profiles_data:
                    profiles_data[new_account] = profiles_data.pop(old_account)
                    with open('profiles.json', 'w') as profiles_file:
                        json.dump(profiles_data, profiles_file, indent=4)
        except FileNotFoundError:
            print("Файл бази даних не знайдено.")
        except Exception as e:
            print("Помилка при зміні акаунту:", e)

    def delete_account_dialog(self):
        account, ok = QtWidgets.QInputDialog.getText(self, 'Видалення акаунту', 'Введіть назву акаунту:')
        if ok:
            password, ok = QtWidgets.QInputDialog.getText(self, 'Видалення акаунту', 'Введіть пароль:', QtWidgets.QLineEdit.Password)
            if ok:
                try:
                    with open('akaunt.json', 'r') as f:
                        data = json.load(f)
                        for user in data['users']:
                            if user['login'] == account and user['password'] == password:
                                data['users'].remove(user)
                                break

                    with open('akaunt.json', 'w') as f:
                        json.dump(data, f, indent=4)
                        QtWidgets.QMessageBox.information(self, "Видалення акаунту", f"Акаунт {account} успішно видалений!")
                        
                    # Також видаляємо акаунт з файлу profiles.json
                    with open('profiles.json', 'r') as f:
                        profiles_data = json.load(f)
                        if account in profiles_data:
                            del profiles_data[account]
                            with open('profiles.json', 'w') as profiles_file:
                                json.dump(profiles_data, profiles_file, indent=4)
                except FileNotFoundError:
                    print("Файл бази даних не знайдено.")
                except Exception as e:
                    print("Помилка при видаленні акаунту:", e)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = profil()
    window.show()
    sys.exit(app.exec_())
