import csv

# Define the data
data = [
    ("Spike protein", 0.8),
    ("ACE2 receptor", 0.7),
    ("Beta-amyloid protein", 0.6),
    ("Tau protein", 0.9),
    ("Beta-amyloid protein", 0.75),
    ("Alpha-synuclein protein", 0.65),
    ("Insulin receptor", 0.85),
    ("Glucose transporter", 0.7),
    ("Dopamine receptor", 0.8),
    ("BRCA1 gene", 0.7),
    ("HER2 protein", 0.9),
    ("CD4 receptor", 0.8),
    ("Alpha-synuclein protein", 0.6),
    ("Dopamine receptor", 0.85),
    ("Vitamin D receptor", 0.8),
    ("CD4 receptor", 0.75),
    ("HIV-1 gp120 protein", 0.8),
    ("Vitamin D receptor", 0.9),
    ("Vitamin D receptor", 0.4),
    ("Calcium-binding protein", 0.85),
    ("Insulin receptor", 0.85)
]

# Write the data to a CSV file
file_path = "drug_protein_data.csv"
with open(file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in data:
        writer.writerow(row)

print(f"CSV file '{file_path}' has been generated.")
