import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget,
    QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QFileDialog, QLabel, QComboBox, QTableView, QListWidget
)
from app import db

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aurora Parser GUI")
        self.setMinimumSize(800,600)

        # Central widget
        main_layout = QVBoxLayout()
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)
        self.status = QLabel('')
        self.statusBar().addPermanentWidget(self.status)

        # Top file selection
        file_layout = QHBoxLayout()

        self.file_input = QLineEdit()
        self.file_input.setPlaceholderText('Select the AuroraDB.db file')
        self.file_input.setReadOnly(True)

        file_button = QPushButton('Select Database')
        file_button.clicked.connect(self.select_database_file)

        file_layout.addWidget(file_button)
        file_layout.addWidget(self.file_input)

        main_layout.addLayout(file_layout)

        # Game & Race selection
        filter_layout = QHBoxLayout()

        self.savegame_combo = QComboBox()
        self.savegame_combo.setPlaceholderText('Select Save')
        self.savegame_combo.setEnabled(True)

        self.race_combo = QComboBox()
        self.race_combo.setPlaceholderText('Select Race')
        self.race_combo.setEnabled(True)

        filter_layout.addWidget(self.savegame_combo)
        filter_layout.addWidget(self.race_combo)

        main_layout.addLayout(filter_layout)

    def select_database_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, 'Select AuroraDB.db', '', 'SQLite Database (*.db)'
        )

        if file_path:
            self.file_input.setText(file_path)
            self.engine = db.connect_db(file_path)

            if self.engine is None:
                self.status.setText('Failed to connect to the database. Check the logs for details.')
            else:
                self.status.setText('Database connected successfully')
                self.load_filters()
    
    def load_filters(self):
        game_query = db.get_saves(self.engine)
        self.savegame_combo.clear()
        self.savegame_map = {}

        for GameID, GameName in game_query:
            self.savegame_combo.addItem(GameName)
            self.savegame_map[GameName] = GameID

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()