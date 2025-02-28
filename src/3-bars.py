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
                    step_data[node_id] = {'A': [], 'B': [], 'C': []}

                filtered_data = data[(data['time'] >= 299.5) & (data['time'] <= 300.5)]

                step_data[node_id][step].append(filtered_data[node_id].sum())

    except Exception as e:
        print(f"Errore nel leggere il file {file}: {e}")

averages = {node_id: {step: np.mean(values) if values else 0 for step, values in steps.items()}
            for node_id, steps in step_data.items()}

variances = {node_id: {step: np.var(values) if values else 0 for step, values in steps.items()}
             for node_id, steps in step_data.items()}

fig, ax = plt.subplots(figsize=(12, 7))

labels = ['Step A P1', 'Step A P2', 'Step A P3',
          'Step B P1', 'Step B P2', 'Step B P3',
          'Step C P1', 'Step C P2', 'Step C P3']
values_A = []
values_B = []
values_C = []
bar_width = 0.25
x_offset = np.arange(len(labels))

values_A = [averages[f'CompletedStepA@node-id1']['A'], averages[f'CompletedStepA@node-id2']['A'], averages[f'CompletedStepA@node-id3']['A']]
values_B = [averages[f'CompletedStepB@node-id1']['B'], averages[f'CompletedStepB@node-id2']['B'], averages[f'CompletedStepB@node-id3']['B']]
values_C = [averages[f'CompletedStepC@node-id1']['C'], averages[f'CompletedStepC@node-id2']['C'], averages[f'CompletedStepC@node-id3']['C']]

bar_A = ax.bar(x_offset[:3], values_A, width=bar_width, color='blue', edgecolor='black')
bar_B = ax.bar(x_offset[3:6], values_B, width=bar_width, color='orange', edgecolor='black')
bar_C = ax.bar(x_offset[6:], values_C, width=bar_width, color='green', edgecolor='black')

for i, bar in enumerate(bar_A):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f'{round(bar.get_height())} ± {round(np.sqrt(variances[f"CompletedStepA@node-id{i+1}"]["A"]))}',
            ha='center', va='bottom', fontsize=12, color='black')


for i, bar in enumerate(bar_B):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f'{round(bar.get_height())} ± {round(np.sqrt(variances[f"CompletedStepB@node-id{i+1}"]["B"]))}',
            ha='center', va='bottom', fontsize=12, color='black')

for i, bar in enumerate(bar_C):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
            f'{round(bar.get_height())} ± {round(np.sqrt(variances[f"CompletedStepC@node-id{i+1}"]["C"]))}',
            ha='center', va='bottom', fontsize=12, color='black')

ax.set_xlabel('Tipo di Step per unità produttiva', fontsize=14, fontweight='bold')
ax.set_ylabel('Totale Step eseguiti', fontsize=14, fontweight='bold')
ax.set_title('Specializzazione delle unità produttive', fontsize=16, fontweight='bold', color='darkblue')
ax.set_xticks(x_offset)
ax.set_xticklabels(labels)

handles = [plt.Rectangle((0, 0), 1, 1, color='blue', edgecolor='black'),
           plt.Rectangle((0, 0), 1, 1, color='orange', edgecolor='black'),
           plt.Rectangle((0, 0), 1, 1, color='green', edgecolor='black')]

labels_legend = ['Step A (± σ)', 'Step B (± σ)', 'Step C (± σ)']
ax.legend(handles=handles, labels=labels_legend)

ax.text(0, -0.15, "Nota: ± σ indica la deviazione standard calcolata dai dati raccolti.",
        fontsize=12, color='gray', ha='left', va='top', transform=ax.transAxes)

plt.tight_layout()
plt.show()
