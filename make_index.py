import sqlite3


def make_index(sql_database_path: str, index_database_name: str, database_path: str, legend_name: str) -> list[str]:
    """Funkcja tworząca bazę danych pd dane białko. Na tym etapie baza zawiera tylko tabelę indexową - legendę"""

    spectra_files_names = []

    database = sqlite3.connect(f"{sql_database_path}\{index_database_name}.db")
    cursor = database.cursor()

    cursor.execute(f"""
        CREATE TABLE {index_database_name} (
            correct BOOL,
            series VARCHAR(64),
            measurement VARCHAR(8),
            measurement_mode VARCHAR(8),
            sample_id VARCHAR(16),
            protein_concentration FLOAT,
            philide_concentration FLOAT,
            total_lipids_concentration FLOAT,
            nadph_concentration FLOAT,
            mgdg_concentration FLOAT,
            dgdg_concentration FLOAT,
            pg_concentration FLOAT,
            sqdg_concentration FLOAT,
            solvent VARCHAR(32)
        )
    """)
    database.commit()
    
    with open(f"{database_path}\{legend_name}.leg", "r", encoding="utf-8") as legend_file:
        for line in legend_file:
            fields = line.split()

            correct = fields[0]
            series = "_".join(fields[1].split("_")[:-1])
            measurement = fields[1].split("_")[-1].replace(".", "_")
            measurement_mode = fields[1].split("_")[-2]
            sample_id = measurement_mode + "_" + series.split("_")[-2] + measurement
            protein_concentration = fields[2]
            philide_concentration = fields[3]
            total_lipids_concentration = fields[4]
            nadph_concentration = fields[5]
            mgdg_concentration = fields[6]
            dgdg_concentration = fields[7]
            pg_concentration = fields[8]
            sqdg_concentration = fields[9]
            solvent = fields[10]

            spectra_files_names.append("_".join(fields[1].split("_")[:-1]))

            cursor.execute(f"""
                INSERT INTO {index_database_name} (
                    correct,
                    series,
                    measurement,
                    measurement_mode,
                    sample_id,
                    protein_concentration,
                    philide_concentration,
                    total_lipids_concentration,
                    nadph_concentration,
                    mgdg_concentration,
                    dgdg_concentration,
                    pg_concentration,
                    sqdg_concentration,
                    solvent
                )
                VALUES (
                    {correct},
                    \'{series}\',
                    \'{measurement}\',
                    \'{measurement_mode}\',
                    \'{sample_id}\',
                    {protein_concentration},
                    {philide_concentration},
                    {total_lipids_concentration},
                    {nadph_concentration},
                    {mgdg_concentration},
                    {dgdg_concentration},
                    {pg_concentration},
                    {sqdg_concentration},
                    \'{solvent}\'
                )
            """)

    database.commit()
    database.close()

    return spectra_files_names



def load_spectra(sql_database_path: str, index_database_name: str, database_path: str, spectra_file_name: str):
    """Funkcja ładująca wszystkie spektra danego białka do bazy tego białka"""

    with open(f"{database_path}\{spectra_file_name}.txt", "r", encoding="utf-8") as spectra_file:
        for _ in range(37):
            next(spectra_file)
        
        measurements = next(spectra_file).replace(".", "_").split()[1:]

        table_fields = "wavelength FLOAT"

        for measurement in measurements:
            table_fields += f",{measurement} FLOAT"

        database = sqlite3.connect(f"{sql_database_path}\{index_database_name}.db")
        cursor = database.cursor()

        cursor.execute(f"""
            CREATE TABLE spectra_{spectra_file_name} (
                {table_fields}
            )
        """)

        database.commit()

        for _ in range(4):
            next(spectra_file)

        for line in spectra_file:
            fields = [field.replace(",", ".") for field in line.split()]

            cursor.execute(f"""
                INSERT INTO spectra_{spectra_file_name} (
                    wavelength,
                    {",".join(measurements)}
                )
                VALUES (
                    {",".join(fields)}
                )
            """)

        database.commit()
        database.close()



if __name__ == "__main__":
    PROTEINS = ["AtPORA", "AtPORB", "AtPORC", "HA1", "HA2", "HA3", "PeaPOR", "PinPOR", "SlPOR1", "SlPOR2", "SlPOR3"]
    
    DATABASE_PATH = "Database\___"
    SQL_DATABASE_PATH = "SQLDatabase"
    
    for protein in PROTEINS:
        spectra_file_names = make_index(SQL_DATABASE_PATH, protein, DATABASE_PATH + protein, protein)
    
        for spectra_file in set(spectra_file_names):
            try:
                load_spectra(SQL_DATABASE_PATH, protein, DATABASE_PATH + protein, spectra_file)
            except:
                print(f"Error! Problem z: {protein}/{spectra_file}")
