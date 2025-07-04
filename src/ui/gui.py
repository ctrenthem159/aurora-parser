import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QAbstractItemView,
    QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QFileDialog, QLabel, QComboBox, QTableView, QListWidget,
    QListWidgetItem
)
from PyQt6.QtCore import QAbstractTableModel, Qt
from app import db, export
import logging

#TODO Add documentation and unit tests
#TODO Clean up imports, remove unused ones
#TODO remove gui.mockup once these are done.

logger = logging.getLogger(__name__)

#TODO - Add DataFrameModel class (see ChatGPT)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aurora Parser GUI")
        #TODO Find a suitable minimum size
        #TODO add more flair to the UI
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
        self.savegame_combo.currentTextChanged.connect(self.list_races)

        self.race_combo = QComboBox()
        self.race_combo.setPlaceholderText('Select Race')
        self.race_combo.setEnabled(True)

        self.load_button = QPushButton('Load')
        self.load_button.setEnabled(False)
        self.load_button.clicked.connect(self.load_events)

        filter_layout.addWidget(self.savegame_combo)
        filter_layout.addWidget(self.race_combo)
        filter_layout.addWidget(self.load_button)

        main_layout.addLayout(filter_layout)

        # Evvents table display
        #TODO Change to QTableView
        self.events_table = QListWidget()
        self.events_table.setMinimumHeight(400)
        self.events_table.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

        main_layout.addWidget(self.events_table, stretch=1)

        # Export settings
        self.export_button = QPushButton('Export')
        self.export_button.setEnabled(False)
        self.export_button.clicked.connect(self.show_export_dialog)

        export_layout = QHBoxLayout()
        export_layout.addStretch()
        export_layout.addWidget(self.export_button)

        main_layout.addLayout(export_layout)

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
                self.list_saves()
    
    def list_saves(self):
        game_query = db.get_saves(self.engine)
        self.savegame_combo.clear()
        self.savegame_map = {}

        for GameID, GameName in game_query:
            self.savegame_combo.addItem(GameName)
            self.savegame_map[GameName] = GameID
    
    def list_races(self):
        selected_game = self.savegame_combo.currentText()
        if not selected_game:
            return
        
        gameID = self.savegame_map.get(selected_game)
        if not gameID:
            return
        
        result = db.get_races(self.engine, gameID)
        self.race_combo.clear()
        self.race_map = {}

        for raceID, raceName in result:
            self.race_combo.addItem(raceName)
            self.race_map[raceName] = raceID

        self.race_combo.setEnabled(True)
        self.load_button.setEnabled(True)
    
    #TODO Refactor this to use a DataFrameModel for QTableView
    def load_events(self):
        selected_race = self.race_combo.currentText()
        raceID = self.race_map.get(selected_race)
        if not raceID:
            self.status.setText('No race selected.')
            return
        
        try:
            events_input = db.get_events(self.engine)
            self.events_output = db.filter_events(self.engine, events_input, gui=True, raceID=raceID)
            self.populate_events_table(self.events_output)
            self.status.setText(f'{len(self.events_output)} events loaded')
        except Exception as e:
            self.status.setText(f'Error loading events.')
            logging.exception(f'Failed to load events: {e}')
    
    def populate_events_table(self, df):
        self.events_table.clear()
        #FIXME review this code, I don't understand what for _, row is doing
        for _, row in df.iterrows():
            summary = row.get('MessageText', str(row.to_dict()))
            item = QListWidgetItem(summary)
            self.events_table.addItem(item)
        
        self.export_button.setEnabled(True)
    
    def show_export_dialog(self):
        filters = "CSV Files (*.csv);;JSON Files (*.json);;Excel Files (*.xlsx);;Text Files (*.txt);;HTML Files (*.html)"
        #FIXME Analyze this code, figure out how getSaveFileName works
        file_path, selected_filter = QFileDialog.getSaveFileName(
            self,
            "Export Events",
            "",  # default path
            filters
        )

        if not file_path:
            return
        
        # Determine format from selected filter
        if selected_filter.startswith("CSV"):
            fmt = "csv"
        elif selected_filter.startswith("JSON"):
            fmt = "json"
        elif selected_filter.startswith("Excel"):
            fmt = "xlsx"
        elif selected_filter.startswith("Text"):
            fmt = "txt"
        elif selected_filter.startswith("HTML"):
            fmt = "html"
        else:
            self.status.setText("Unsupported file type.")
            return
        
        #TODO validate excel, txt, and json. csv and html work fine.
        try:
            export.export_data(self.events_output[['IncrementID', 'MessageText']], file_path, format=fmt)
            self.status.setText(f"Exported to {file_path}")
        except Exception as e:
            logging.exception("Export failed")
            self.status.setText("Export failed. See logs.")

def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    run_gui()