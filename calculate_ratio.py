import sqlite3

DATABASE = "Ref"

DATABASE_PATH = f"SQLDatabase/{DATABASE}.db"

database = sqlite3.connect(DATABASE_PATH)
cursor = database.cursor()

cursor.execute(f"""
    SELECT 
        spectra_file,
        sample_id 
    FROM {DATABASE} 
    WHERE spectra_file = \'SlPOR1_A\'
    AND chilide_concentration = 0
    AND 
""")
spectra = list(cursor)

for series, sample_id in spectra:
    cursor.execute(f"""
        SELECT 
            (SELECT {sample_id} FROM spectra_{series} WHERE wavelength = 657) 
                / 
            (SELECT {sample_id} FROM spectra_{series} WHERE wavelength = 672)
    """)
    print(f"{series}\{sample_id}: {next(cursor)[0]}")


database.close()

