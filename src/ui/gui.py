import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QAbstractItemView,
    QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit,
    QFileDialog, QLabel, QComboBox, QTableView
)
from PyQt6.QtCore import QAbstractTableModel, Qt
from app import db, export
import logging

#TODO Add documentation and unit tests

logger = logging.getLogger(__name__)

class QDataFrameModel(QAbstractTableModel):
    def __init__(self,data, visible_columns=None):
        super().__init__()
        self._data = data
        if visible_columns is None:
            self.visible_columns = list(data.columns)
        else:
            self.visible_columns = visible_columns
    
    def data(self, index, role):
        if role == Qt.ItemDataRole.DisplayRole:
            column = self.visible_columns[index.column()]
            value = self._data.iloc[index.row()][column]
            return str(value)
    
    def rowCount(self, index):
        return self._data.shape[0]
    
    def columnCount(self, index):
        return len(self.visible_columns)
    
    def headerData(self, section, orientation, role):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return str(self.visible_columns[section])
            elif orientation == Qt.Orientation.Vertical:
                return str(self._data.index[section])

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aurora Parser GUI")
        #TODO add more flair to the UI

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
        self.events_table = QTableView()
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
        
        self.gameID = self.savegame_map.get(selected_game)
        if not self.gameID:
            return
        
        result = db.get_races(self.engine, self.gameID)
        self.race_combo.clear()
        self.race_map = {}

        for raceID, raceName in result:
            self.race_combo.addItem(raceName)
            self.race_map[raceName] = raceID

        self.race_combo.setEnabled(True)
        self.load_button.setEnabled(True)
    
    def load_events(self):
        selected_race = self.race_combo.currentText()
        raceID = self.race_map.get(selected_race)
        if not raceID:
            self.status.setText('No race selected.')
            return
        
        try:
            events_input = db.get_events(self.engine) #returns a df
            self.events_output = db.filter_events(self.engine, events_input, self.gameID, raceID)
            self.populate_events_table(self.events_output)
            self.status.setText(f'{len(self.events_output)} events loaded')
        except Exception as e:
            self.status.setText(f'Error loading events.')
            logging.exception(f'Failed to load events: {e}')
    
    def populate_events_table(self, df):
        self.model = QDataFrameModel(df, visible_columns=['Timestamp', 'EventType', 'MessageText'])
        self.events_table.setModel(self.model)
        self.events_table.resizeColumnsToContents()
        
        self.export_button.setEnabled(True)
    
    def show_export_dialog(self):
        filters = "CSV Files (*.csv);;JSON Files (*.json);;Excel Files (*.xlsx);;Text Files (*.txt);;HTML Files (*.html)"
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
            export.export_data(self.events_output[['Timestamp', 'MessageText']], file_path, format=fmt)
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