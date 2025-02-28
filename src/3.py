import pandas as pd
import matplotlib.pyplot as plt
import glob
import numpy as np

step_data = {}

files = glob.glob("data3/*.csv")
print(f"Trovati {len(files)} file nella cartella data: {files}")

expected_columns = ['time',
                    'CompletedStepA@node-id1', 'CompletedStepA@node-id2', 'CompletedStepA@node-id3',
                    'CompletedStepB@node-id1', 'CompletedStepB@node-id2', 'CompletedStepB@node-id3',
                    'CompletedStepC@node-id1', 'CompletedStepC@node-id2', 'CompletedStepC@node-id3']

for file in files:
    print(f"Elaborando il file: {file}")
    try:
        with open(file, 'r') as f:
            lines = f.readlines()

        header_line = None
        for i, line in enumerate(lines):
            if line.strip().startswith("# The columns have the following meaning:"):
                header_line = i + 1
                break

        if header_line is None:
            print(f"Intestazione non trovata nel file {file}.")
            continue

        data = pd.read_csv(file, sep='\s+', comment='#', skiprows=header_line)

        if data.shape[1] != len(expected_columns):
            print(f"Numero di colonne errato nel file {file}.")
            continue

        data.columns = expected_columns
        data = data.fillna(0)

        for step, node_prefix in [('A', 'CompletedStepA'), ('B', 'CompletedStepB'), ('C', 'CompletedStepC')]:
            for i in range(1, 4):  # Per ogni nodo (1, 2, 3)
                node_id = f"{node_prefix}@node-id{i}"
                if node_id not in step_data:
                    step_data[node_id] = []

                filtered_data = data[(data['time'] >= 299.5) & (data['time'] <= 300.5)]

                step_data[node_id].extend(filtered_data[node_id].values)

    except Exception as e:
        print(f"Errore nel leggere il file {file}: {e}")

fig, ax = plt.subplots(figsize=(12, 7))

boxplot_data = [step_data[f'CompletedStepA@node-id{i}'] for i in range(1, 4)] + \
               [step_data[f'CompletedStepB@node-id{i}'] for i in range(1, 4)] + \
               [step_data[f'CompletedStepC@node-id{i}'] for i in range(1, 4)]

labels = ['Step A P1', 'Step A P2', 'Step A P3',
          'Step B P1', 'Step B P2', 'Step B P3',
          'Step C P1', 'Step C P2', 'Step C P3']

ax.boxplot(boxplot_data, vert=True, patch_artist=True,
           boxprops=dict(facecolor="lightblue", color="black"),
           whiskerprops=dict(color="black"),
           capprops=dict(color="black"),
           medianprops=dict(color="red"),
           flierprops=dict(marker="o", color="green", alpha=0.5))

ax.set_yscale('symlog', linthresh=1)

ax.set_title("Specializzazione delle unità produttive", fontsize=16, fontweight='bold', color='darkblue')
ax.set_ylabel("Numero di Step completati", fontsize=14, fontweight='bold')
ax.set_xlabel("Tipo di Step per unità produttiva", fontsize=14, fontweight='bold')
ax.set_xticks(range(1, len(labels) + 1))
ax.set_xticklabels(labels, rotation=45, ha="right")

plt.tight_layout()
plt.show()
