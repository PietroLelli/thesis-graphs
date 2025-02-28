import pandas as pd
import matplotlib.pyplot as plt
import glob

modes = ["Random", "Self", "ShortWaitingList"]

time_series = {}

for mode in modes:
    try:
        files = glob.glob(f"data2/*{mode}*.csv")
        print(f"Trovati {len(files)} file per la modalità {mode}: {files}")

        mode_data = pd.DataFrame()

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

                data = pd.read_csv(file, delim_whitespace=True, comment='#', skiprows=header_line)
                expected_columns = ['time', 'ResultsSize[mean]', 'ResultsSize[max]', 'ResultsSize[min]']
                data.columns = expected_columns[:len(data.columns)]

                print(f"Colonne trovate nel file {file}: {data.columns}")

                if 'time' not in data.columns or 'ResultsSize[mean]' not in data.columns:
                    print(f"Colonne 'time' o 'ResultsSize[mean]' mancanti nel file {file}.")
                    continue

                data['time'] = data['time'].round().astype(int)

                mode_data = pd.concat([mode_data, data[['time', 'ResultsSize[mean]']]])

            except Exception as e:
                print(f"Errore nel leggere il file {file}: {e}")

        if not mode_data.empty:
            mode_data = mode_data.groupby('time').agg({'ResultsSize[mean]': 'mean'}).reset_index()

        time_series[mode] = mode_data

    except Exception as e:
        print(f"Errore nel processare i file per la modalità {mode}: {e}")

plt.figure(figsize=(10, 7))
for mode, df in time_series.items():
    if not df.empty:
        df = df.sort_values(by='time')
        plt.plot(df['time'], df['ResultsSize[mean]'], label=mode, marker='o')

plt.title("Andamento dei Result nel tempo", fontsize=16, fontweight='bold', color='darkblue')
plt.xlabel("Tempo", fontsize=14, fontweight='bold')
plt.ylabel("Numero di Result", fontsize=14, fontweight='bold')
plt.legend(title="Modalità", fontsize=12)
plt.grid(axis='both', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()
