# gui.py

from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit, QLineEdit, QFileDialog,QMessageBox
from PyQt5.QtGui import QFont
from PyQt5 import QtGui, QtCore
from collections import defaultdict
from algo import *
import csv
from spellchecker import SpellChecker

class DrugRetargetingGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drug Retargeting GUI")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Load Drug-Protein CSV Button
        # Load Drug-Protein CSV Button
        self.load_csv_button = QPushButton("Load Drug-Protein CSV")
        self.load_csv_button.setStyleSheet("""
            QPushButton {
                font-size: 10px;  /* Smaller font size */
                background-color: #4CAF50; /* Green */
                border: none;
                color: white;
                padding: 2px 5px;  /* Smaller padding */
                text-align: center;
                text-decoration: none;
                display: inline-block;
                margin: 2px 1px;  /* Smaller margin */
                cursor: pointer;
            }

            QPushButton:hover {
                background-color: #45a049; /* Darker green */
            }
        """)
        self.load_csv_button.clicked.connect(self.open_file_dialog)
        self.load_csv_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))

        # Create a horizontal layout to left-align the button
        hlayout = QHBoxLayout()
        hlayout.addWidget(self.load_csv_button)
        hlayout.addStretch()

        layout.addLayout(hlayout)

        # Protein Input Section
        label_protein = QLabel("Enter Protein:")
        label_protein.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label_protein)
        self.protein_line_edit = QLineEdit()
        self.protein_line_edit.setStyleSheet("font-size: 12px;")
        layout.addWidget(self.protein_line_edit)

        # ...

        self.central_widget.setLayout(layout)
        # Potential Targets Section
        label_targets = QLabel("Potential Targets")
        label_targets.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label_targets)
        self.potential_targets_text_edit = QTextEdit()
        self.potential_targets_text_edit.setStyleSheet("font-size: 12px;")
        layout.addWidget(self.potential_targets_text_edit)

        # Search Button
        self.search_button = QPushButton("Search")
        self.search_button.setStyleSheet("font-size: 12px;")
        self.search_button.clicked.connect(self.search_potential_targets)
        self.search_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(self.search_button)


        # Initialize drug-protein data
        self.drug_protein_data = {
            "Drug 1": {"Spike protein": 0.8, "ACE2 receptor": 0.7, "Beta-amyloid protein": 0.6},
            "Drug 2": {"Tau protein": 0.9, "Beta-amyloid protein": 0.75, "Alpha-synuclein protein": 0.65},
            "Drug 3": {"Insulin receptor": 0.85, "Glucose transporter": 0.7, "Dopamine receptor": 0.8},
            "Drug 4": {"BRCA1 gene": 0.7, "HER2 protein": 0.9, "CD4 receptor": 0.8},
            "Drug 5": {"Alpha-synuclein protein": 0.6, "Dopamine receptor": 0.85, "Vitamin D receptor": 0.8},
            "Drug 6": {"CD4 receptor": 0.75, "HIV-1 gp120 protein": 0.8, "Vitamin D receptor": 0.9},
            "Drug 7": {"Vitamin D receptor": 0.4, "Calcium-binding protein": 0.85, "Insulin receptor": 0.85}
        }

        self.disease_protein_map = {
            "COVID-19": {"Spike protein", "ACE2 receptor"},
            "Alzheimer's disease": {"Tau protein", "Beta-amyloid protein"},
            "Type 2 diabetes": {"Insulin receptor", "Glucose transporter"},
            "Breast cancer": {"BRCA1 gene", "HER2 protein"},
            "Parkinson's disease": {"Alpha-synuclein protein", "Dopamine receptor"},
            "HIV/AIDS": {"CD4 receptor", "HIV-1 gp120 protein"},
            "Osteoporosis": {"Vitamin D receptor", "Calcium-binding protein"}
        }

        # Apply button hover style
        self.apply_button_hover_style()
        
    def open_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Drug-Protein CSV", "", "CSV files (*.csv)", options=options)
        if file_path:
            self.load_csv_data(file_path)
            
    def load_csv_data(self, file_path):
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                drug_name, protein1, effectiveness1, protein2, effectiveness2, protein3, effectiveness3 = row
                self.drug_protein_data[drug_name] = {
                    protein1: float(effectiveness1),
                    protein2: float(effectiveness2),
                    protein3: float(effectiveness3)
                }
        return self.drug_protein_data

    def apply_button_hover_style(self):
        # Red color when hovering over buttons
        hover_style = "QPushButton:hover { background-color: red; }"
        # self.add_mapping_button.setStyleSheet(hover_style)
        self.search_button.setStyleSheet(hover_style)
        
    def search_potential_targets(self):
        protein = self.protein_line_edit.text()
        graph = construct_drug_retargeting_graph(self.disease_protein_map, self.drug_protein_data)

        # Create a spell checker and give it the list of correct protein names
        spell = SpellChecker(language=None, case_sensitive=True)
        all_proteins = set(protein for proteins in self.drug_protein_data.values() for protein in proteins)
        spell.word_frequency.load_words(all_proteins)

        # Check the spelling of the entered protein
        misspelled = spell.unknown([protein])
        for word in misspelled:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText(f"Did you mean {spell.correction(word)}?")
            msg.setWindowTitle("Spelling Suggestion")
            msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            retval = msg.exec_()
            if retval == QMessageBox.Ok:
                self.protein_line_edit.setText(spell.correction(word))
                protein = self.protein_line_edit.text()
            else:
                return  # Exit the function if user clicked Cancel

        targets = find_potential_targets(graph, protein)
        self.potential_targets_text_edit.clear()
        if not targets:
            self.potential_targets_text_edit.clear()
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('No potential targets found for the given protein.')
            msg.setWindowTitle("Error")
            msg.exec_()
        else:
            for drug, effectiveness in targets.items():
                self.potential_targets_text_edit.append(f"{drug}: {effectiveness}")

    # def load_csv_file(self):
    #     file_dialog = QFileDialog()
    #     file_dialog.setNameFilter("CSV files (*.csv)")
    #     if file_dialog.exec_():
    #         file_name = file_dialog.selectedFiles()[0]
    #         self.load_csv_data(file_name)


   
