import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import glob

modes = ["Random", "Self", "ShortWaitingList"]

data_dict = {'Mode': [], 'ResultsSize[mean]': []}

for mode in modes:
    try:
        files = glob.glob(f"data2/*{mode}*.csv")
        print(f"Trovati {len(files)} file per la modalità {mode}: {files}")

        mode_means = []

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

                filtered_data = data[(data['time'] >= 299.5) & (data['time'] <= 300.5)]

                data_dict['Mode'].extend([mode] * len(filtered_data))
                data_dict['ResultsSize[mean]'].extend(filtered_data['ResultsSize[mean]'].tolist())

                if not filtered_data.empty:
                    mode_means.append(filtered_data['ResultsSize[mean]'].mean())

            except Exception as e:
                print(f"Errore nel leggere il file {file}: {e}")

        if mode_means:
            overall_mean = sum(mode_means) / len(mode_means)
            print(f"Media di ResultsSize[mean] per la modalità {mode}: {overall_mean:.2f}")
        else:
            print(f"Nessun dato valido trovato per la modalità {mode}.")

    except Exception as e:
        print(f"Errore nel processare i file per la modalità {mode}: {e}")

df = pd.DataFrame(data_dict)

plt.figure(figsize=(10, 7))
sns.boxplot(x='Mode', y='ResultsSize[mean]', data=df, palette="Set2")

plt.title("Distribuzione di ResultsSize al tempo 300", fontsize=16, fontweight='bold', color='darkblue')
plt.xlabel("Modalità", fontsize=14, fontweight='bold')
plt.ylabel("Numero di Result", fontsize=14, fontweight='bold')

plt.tight_layout()
plt.show()
