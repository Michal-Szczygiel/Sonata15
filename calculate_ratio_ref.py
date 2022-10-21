import sqlite3

DATABASE = "Ref"
DATABASE_PATH = f"SQLDatabase/{DATABASE}.db"
OUTPUT_FILE = "SQLDatabase/ratios_ref.csv"

database = sqlite3.connect(DATABASE_PATH)
cursor = database.cursor()

cursor.execute(f"""
    SELECT
        spectra_file,
        sample_id,
        philide_concentration,
        chilide_concentration,
        nadph_concentration,
        nadpp_concentration,
        total_lipids_concentration,
        mgdg_concentration,
        dgdg_concentration,
        pg_concentration,
        sqdg_concentration
    FROM {DATABASE}
""")
spectra = list(cursor)

with open(OUTPUT_FILE, "w") as output_file:
    for series, sample_id, philide, chilide, nadph, nadpp, total_lipids, mgdg, dgdg, pg, sqdg in spectra:
        if philide > 0 and chilide == 0:
            pigment = "P"

            cursor.execute(f"""
                SELECT 
                    (SELECT {sample_id} FROM spectra_{series} WHERE wavelength = 657) 
                        / 
                    (SELECT {sample_id} FROM spectra_{series} WHERE wavelength = 622)
            """)
        elif philide == 0 and chilide > 0:
            pigment = "C"

            cursor.execute(f"""
                SELECT 
                    (SELECT {sample_id} FROM spectra_{series} WHERE wavelength = 696) 
                        / 
                    (SELECT {sample_id} FROM spectra_{series} WHERE wavelength = 676)
            """)
        else:
            continue


        if nadph > 0 and nadpp == 0:
            nucleotide = "NH"
        elif nadph == 0 and nadpp > 0:
            nucleotide = "N+"

        if total_lipids == 0:
            lipids = "NoLi"
        elif mgdg == 50 and dgdg == 35 and pg == 15 and sqdg == 0:
            lipids = "OPT"
        elif mgdg > 0 and dgdg == 0 and pg == 0 and sqdg == 0:
            lipids = "MGDG"
        elif mgdg == 0 and dgdg > 0 and pg == 0 and sqdg == 0:
            lipids = "DGDG"
        elif mgdg == 0 and dgdg == 0 and pg > 0 and sqdg == 0:
            lipids = "PG"
        elif mgdg == 0 and dgdg == 0 and pg == 0 and sqdg > 0:
            lipids = "SQDG"
        else:
            lipids = "--"
            
        output_file.write(f"{series},{sample_id},{pigment},{lipids},{next(cursor)[0]}\n")


database.close()
