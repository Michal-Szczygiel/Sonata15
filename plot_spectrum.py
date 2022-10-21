import sqlite3

import matplotlib.pyplot as plt

COLORS = ["red", "green", "blue", "cyan", "magenta", "black", "gray", "yellow", "pink"]

DATABASE = "SQLDatabase\AtPORA.db"
database = sqlite3.connect(DATABASE)
cursor = database.cursor()

cursor.execute("""
        SELECT series, measurement, nadph_concentration FROM AtPORA WHERE 
            correct = 1
            AND measurement_mode = \'D\'
            AND total_lipids_concentration = 0
            AND protein_concentration = 15
            AND philide_concentration = 5
    """)

hits = [hit for hit in cursor if hit[0].split("_")[0] == "2019" and hit[0].split("_")[3] == "A"]

spectra = []

for hit in hits:
    spectra.append(([], [], hit[2]))
    measurement = hit[0].split("_")[4] + "_" + hit[0].split("_")[3] + hit[1]
    cursor.execute(f"""SELECT wavelength, {measurement} FROM spectra_{hit[0]}""")

    for w, d in cursor:
        spectra[-1][0].append(w)
        spectra[-1][1].append(d)

database.close()

for index, (wavelengths, values, nadph) in enumerate(spectra):
    plt.plot(wavelengths, values, color=COLORS[index % len(COLORS)], label=nadph)

plt.grid()
plt.legend()
plt.show()
