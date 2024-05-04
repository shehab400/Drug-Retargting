import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QComboBox, QTextEdit, QLineEdit, QFileDialog
from PyQt5.QtGui import QFont
from collections import defaultdict
from PyQt5 import QtGui, QtCore
import qdarkstyle

# Drug retargeting algorithm functions
class Node:
    def __init__(self, node_type, name):
        self.node_type = node_type
        self.name = name
        self.connections = {}  # Use a dictionary to store protein connections with weights

def construct_drug_retargeting_graph(disease_protein_map, drug_protein_map):
    graph = {}

    # Add disease nodes and connect them to protein nodes
    for disease, proteins in disease_protein_map.items():
        if disease not in graph:
            graph[disease] = Node("Disease", disease)
        for protein in proteins:
            if protein not in graph:
                graph[protein] = Node("Protein", protein)
            graph[disease].connections[protein] = 0  # Initialize effectiveness to 0 for diseases

    # Add drug nodes and connect them to protein nodes
    for drug, protein_list in drug_protein_map.items():
        if drug not in graph:
            graph[drug] = Node("Drug", drug)
        for protein, effectiveness in protein_list.items():
            if protein not in graph:
                graph[protein] = Node("Protein", protein)
            graph[drug].connections[protein] = effectiveness

    return graph

def find_potential_targets(graph, drug):
    if drug not in graph:
        return []
    
    targets = set()
    visited_proteins = set()  # Track visited proteins to avoid cycles
    drug_node = graph[drug]
    
    # DFS to explore protein interactions
    def dfs(node, weight_so_far):
        if node.node_type == "Disease":
            targets.add(node.name)
            return
        for protein, effectiveness in node.connections.items():
            if protein not in visited_proteins:
                visited_proteins.add(protein)
                dfs(graph[protein], weight_so_far * effectiveness)
    
    dfs(drug_node, 1)  # Start DFS traversal with initial weight 1
    return list(targets)

# GUI class
class DrugRetargetingGUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drug Retargeting GUI")
        self.setGeometry(100, 100, 600, 400)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout()

        # Disease-Protein Mappings Section
        label_mappings = QLabel("Disease-Protein Mappings")
        label_mappings.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label_mappings)
        self.disease_protein_layout = QVBoxLayout()
        layout.addLayout(self.disease_protein_layout)
        self.add_mapping_button = QPushButton("Add Mapping")
        self.add_mapping_button.setStyleSheet("font-size: 12px;")
        self.add_mapping_button.clicked.connect(self.add_disease_protein_mapping)
        self.add_mapping_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(self.add_mapping_button)

        # Drug Selection Section
        label_drug = QLabel("Drug Selection")
        label_drug.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(label_drug)
        self.drug_combo_box = QComboBox()
        self.drug_combo_box.setStyleSheet("font-size: 12px;")
        layout.addWidget(self.drug_combo_box)

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

        # Load Drug-Protein CSV Button
        self.load_csv_button = QPushButton("Load Drug-Protein CSV")
        self.load_csv_button.setStyleSheet("font-size: 12px;")
        self.load_csv_button.clicked.connect(self.load_csv_file)
        self.load_csv_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        layout.addWidget(self.load_csv_button)

        self.central_widget.setLayout(layout)

        # Initialize drug-protein data
        self.drug_protein_data = {}

        # Apply button hover style
        self.apply_button_hover_style()

    def apply_button_hover_style(self):
        # Red color when hovering over buttons
        hover_style = "QPushButton:hover { background-color: red; }"
        self.add_mapping_button.setStyleSheet(hover_style)
        self.search_button.setStyleSheet(hover_style)
        self.load_csv_button.setStyleSheet(hover_style)

    def add_disease_protein_mapping(self):
        disease_text_box = QLineEdit()
        protein_text_box = QLineEdit()
        layout = QHBoxLayout()
        layout.addWidget(disease_text_box)
        layout.addWidget(protein_text_box)
        self.disease_protein_layout.addLayout(layout)

    def search_potential_targets(self):
        selected_drug = self.drug_combo_box.currentText()
        graph = construct_drug_retargeting_graph(self.get_disease_protein_mappings(), self.drug_protein_data)
        targets = find_potential_targets(graph, selected_drug)
        self.potential_targets_text_edit.clear()
        self.potential_targets_text_edit.append("\n".join(targets))

    def get_disease_protein_mappings(self):
        mappings = defaultdict(set)
        for i in range(self.disease_protein_layout.count()):
            layout = self.disease_protein_layout.itemAt(i)
            disease = layout.itemAt(0).widget().text()
            protein = layout.itemAt(1).widget().text()
            mappings[disease].add(protein)
        return mappings

    def load_csv_file(self):
        file_dialog = QFileDialog()
        file_dialog.setNameFilter("CSV files (*.csv)")
        if file_dialog.exec_():
            file_name = file_dialog.selectedFiles()[0]
            self.load_csv_data(file_name)

    def load_csv_data(self, file_name):
        # Here you would implement the logic to read the CSV file and populate self.drug_protein_data
        # For simplicity, I'll just assume a sample data format
        self.drug_protein_data = {
            "Drug A": {"Protein A": 0.8, "Protein B": 0.7},
            "Drug B": {"Protein B": 0.9, "Protein C": 0.6}
        }
        self.update_drug_combo_box()

    def update_drug_combo_box(self):
        self.drug_combo_box.clear()
        self.drug_combo_box.addItems(self.drug_protein_data.keys())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DrugRetargetingGUI()
    app.setStyleSheet(qdarkstyle.load_stylesheet())
    window.show()
    sys.exit(app.exec_())
