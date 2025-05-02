from PyQt6.QtWidgets import *
from fortunegui import *
import random


class Logic(QMainWindow, Ui_MainWindow):
    __fortunes = {}
    __misfortunes = {}

    def __init__(self) -> None:
        """
        method to set the form default values
        """
        super().__init__()
        self.setupUi(self)

        self.__read_fortunes()
        self.button_get_fortune_page.clicked.connect(lambda: self.show_get_fortune_page())
        self.button_add_fortune_page.clicked.connect(lambda: self.show_add_fortune_page())
        self.button_get_fortune_back.clicked.connect(lambda: self.show_main_page())
        self.button_add_fortune_back.clicked.connect(lambda: self.show_main_page())
        self.label_number.setText(f"Enter a Number 1 - {len(self.__fortunes)}")
        self.radio_fortune.clicked.connect(self.__reset_fortunes)
        self.radio_misfortune.clicked.connect(self.__reset_misfortunes)
        self.radio_addFortune.clicked.connect(self.__reset_input_fortune)
        self.radio_addMisfortune.clicked.connect(self.__reset_input_fortune)
        self.button_getFortune.clicked.connect(lambda: self.get_fortune())
        self.button_addFortune.clicked.connect(lambda: self.add_fortune())

    def show_get_fortune_page(self) -> None:
        """
        method to show the get fortune page
        """
        self.__read_fortunes()
        self.radio_fortune.setChecked(True)
        self.label_number.setText(f"Enter a Number 1 - {len(self.__fortunes)}")
        self.stackedWidget.setCurrentIndex(1)
        self.input_number.setFocus()
        self.label_fortune.clear()


    def show_add_fortune_page(self) -> None:
        """
        method to show the add fortune page
        """
        self.radio_addFortune.setChecked(True)
        self.stackedWidget.setCurrentIndex(2)
        self.input_fortune.setFocus()

    def show_main_page(self) -> None:
        """
        method to show the main page
        """
        self.stackedWidget.setCurrentIndex(0)

    def __reset_fortunes(self) -> None:
        """
        method to reset the get fortune area of the form when the fortune radio button is clicked
        """
        self.label_number.setText(f"Enter a Number 1 - {len(self.__fortunes)}")
        self.input_number.clear()
        self.input_number.setFocus()
        self.label_fortune.clear()

    def __reset_misfortunes(self) -> None:
        """
        method to reset the get fortune area of the form when the misfortune radio button is clicked
        """
        self.label_number.setText(f"Enter a Number 1 - {len(self.__misfortunes)}")
        self.input_number.clear()
        self.input_number.setFocus()
        self.label_fortune.clear()

    def __reset_input_fortune(self) -> None:
        """
        method to reset the add fortune area of the form
        """
        self.label_error.setText('')
        self.input_fortune.clear()
        self.input_fortune.setFocus()


    def __read_fortunes(self) -> None:
        """
        method to read from fortunes and misfortunes files into dictionaries
        """
        with open('fortunes.txt', 'r') as file:
            x = 1
            for line in file:
                self.__fortunes[x] = line
                x += 1

        with open('misfortunes.txt', 'r') as file:
            x = 1
            for line in file:
                self.__misfortunes[x] = line
                x += 1

    def get_fortune(self) -> None:
        """
        method to get a random fortune
        """
        fortune_type = self.buttonGroup_getFortune.checkedButton().text()
        user_input = self.input_number.text().strip()

        if fortune_type == 'Fortune':
            try:
                user_input = int(user_input)

                if user_input <= 0 or user_input > len(self.__fortunes):
                    raise ValueError
                else:
                    num = random.randint(1, len(self.__fortunes))
                    while num == user_input:
                        num = random.randint(1, len(self.__fortunes))
                    self.label_fortune.setText(self.__fortunes.get(num,'This is not the fortune you are looking for ;)'))
                    self.__clear_get_fortune()
            except ValueError:
                self.label_fortune.setText(f'You must enter a number between 1 - {len(self.__fortunes)}')
                self.input_number.clear()
                self.input_number.setFocus()
            except TypeError:
                self.label_fortune.setText(f'You must enter a number between 1 - {len(self.__fortunes)}')
                self.input_number.clear()
                self.input_number.setFocus()
        else:
            try:
                user_input = int(user_input)

                if user_input <= 0 or user_input > len(self.__misfortunes):
                    raise ValueError
                else:
                    num = random.randint(1, len(self.__misfortunes))
                    while num == user_input:
                        num = random.randint(1, len(self.__misfortunes))
                    self.label_fortune.setText(self.__misfortunes.get(num,'This is not the fortune you are looking for ;)'))
                    self.__clear_get_fortune()
            except ValueError:
                self.label_fortune.setText(f'You must enter a number between 1 - {len(self.__misfortunes)}')
                self.input_number.clear()
                self.input_number.setFocus()
            except TypeError:
                self.label_fortune.setText(f'You must enter a number between 1 - {len(self.__misfortunes)}')
                self.input_number.clear()
                self.input_number.setFocus()

    def __clear_get_fortune(self) -> None:
        """
        method to clear the get fortune page
        """
        self.__read_fortunes()
        fortune_type = self.buttonGroup_getFortune.checkedButton().text()

        if fortune_type == 'Fortune':
            self.label_number.setText(f"Enter a Number 1 - {len(self.__fortunes)}")
        else:
            self.label_number.setText(f"Enter a Number 1 - {len(self.__misfortunes)}")

        self.input_number.clear()
        self.input_number.setFocus()
        self.button_getFortune.setText('Get Another Fortune')


    def add_fortune(self) -> None:
        """
        method to add a fortune
        """
        try:
            user_input = self.input_fortune.text().strip()

            #lists, sets, dicts, quotes, only numbers and > 42 chars are invalid data
            if user_input == '':
                raise ValueError
            elif len(user_input) > 42:
                raise ValueError
            elif user_input.startswith('[') and user_input.endswith(']'):
                raise ValueError
            elif user_input.startswith('(') and user_input.endswith(')'):
                raise ValueError
            elif user_input.startswith('{') and user_input.endswith('}'):
                raise ValueError
            elif user_input.startswith("'") and user_input.endswith("'"):
                raise ValueError
            elif user_input.startswith('"') and user_input.endswith('"'):
                raise ValueError
            elif user_input.isdigit():
                raise ValueError
            else:
                self.__write_fortunes(user_input)
                self.__clear_add_fortune()

        except ValueError:
            if len(user_input) > 42:
                self.label_error.setText(f'Enter a shorter fortune')
            elif user_input.startswith('[') and user_input.endswith(']'):
                self.label_error.setText(f'Enter a phrase, not a list')
            elif user_input.startswith('(') and user_input.endswith(')'):
                self.label_error.setText(f'Enter a phrase, not a set')
            elif user_input.startswith('{') and user_input.endswith('}'):
                self.label_error.setText(f'Enter a phrase, not a dictionary')
            elif user_input.startswith("'") and user_input.endswith("'"):
                self.label_error.setText(f'Enter a phrase, not a quote')
            elif user_input.startswith('"') and user_input.endswith('"'):
                self.label_error.setText(f'No quotes!')
            elif user_input.isdigit():
                self.label_error.setText(f'Enter a phrase, not numbers')
            else:
                self.label_error.setText(f'Enter a valid fortune')

            self.input_fortune.clear()
            self.input_fortune.setFocus()
        except TypeError:
            self.label_error.setText(f'Enter a valid fortune')
            self.input_fortune.clear()
            self.input_fortune.setFocus()

    def __write_fortunes(self, fortune) -> None:
        """
        method to write a user input fortune to the fortunes or misfortunes files
        :param fortune: fortune input into the form by the user
        """
        fortune_type = self.buttonGroup_addFortune.checkedButton().text()
        if fortune_type == 'Fortune':
            with open('fortunes.txt', 'a',newline='') as file:
                file.write(fortune + '\n')
        else:
            with open('misfortunes.txt', 'a',newline='') as file:
                file.write(fortune + '\n')

    def __clear_add_fortune(self) -> None:
        """
        method to clear the add fortune page
        """
        self.label_error.clear()
        self.input_fortune.clear()
        self.input_fortune.setFocus()
        self.button_addFortune.setText('Add Another Fortune')

    def __str__(self) -> str:
        """
        method to return information about what this program does
        :return: what the program does
        """
        return f'This program provides fortune cookie wisdom'