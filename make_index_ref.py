import sqlite3


def make_index_ref(sql_database_path: str, index_database_name: str, database_path: str, legend_name: str) -> list[str]:
    spectra_files_names = []

    database = sqlite3.connect(f"{sql_database_path}\{index_database_name}.db")
    cursor = database.cursor()

    cursor.execute(f"""
        CREATE TABLE {index_database_name} (
            correct BOOL,
            spectra_file VARCHAR(64),
            sample_id VARCHAR(16),
            protein_concentration FLOAT,
            philide_concentration FLOAT,
            chilide_concentration FLOAT,
            nadph_concentration FLOAT,
            nadpp_concentration FLOAT,
            total_lipids_concentration FLOAT,
            mgdg_concentration FLOAT,
            dgdg_concentration FLOAT,
            pg_concentration FLOAT,
            sqdg_concentration FLOAT,
            solvent VARCHAR(32)
        )
    """)
    database.commit()
    
    with open(f"{database_path}\{legend_name}.rleg", "r", encoding="utf-8") as legend_file:
        next(legend_file)

        for line in legend_file:
            fields = line.split()

            correct = fields[0]
            spectra_file = fields[1]
            sample_id = fields[2].replace(".", "_")
            protein_concentration = fields[3]
            philide_concentration = fields[4]
            chilide_concentration = fields[5]
            nadph_concentration = fields[6]
            nadpp_concentration = fields[7]
            total_lipids_concentration = fields[8]
            mgdg_concentration = fields[9]
            dgdg_concentration = fields[10]
            pg_concentration = fields[11]
            sqdg_concentration = fields[12]
            solvent = fields[13]

            spectra_files_names.append(spectra_file)

            cursor.execute(f"""
                INSERT INTO {index_database_name} (
                    correct,
                    spectra_file,
                    sample_id,
                    protein_concentration,
                    philide_concentration,
                    chilide_concentration,
                    nadph_concentration,
                    nadpp_concentration,
                    total_lipids_concentration,
                    mgdg_concentration,
                    dgdg_concentration,
                    pg_concentration,
                    sqdg_concentration,
                    solvent
                )
                VALUES (
                    {correct},
                    \'{spectra_file}\',
                    \'{sample_id}\',
                    {protein_concentration},
                    {philide_concentration},
                    {chilide_concentration},
                    {nadph_concentration},
                    {nadpp_concentration},
                    {total_lipids_concentration},
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


def load_spectra_ref(sql_database_path: str, index_database_name: str, database_path: str, spectra_file_name: str):
    with open(f"{database_path}\{spectra_file_name}.ref", "r", encoding="utf-8") as spectra_file:
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
    SQL_DATABASE_PATH = "SQLDatabase"
    REF_DATABASE_NAME = "Ref"
    DATABASE_PATH = "Database\REF"
    LEGEND_NAME = "REF_LEG"

    spectra_files = make_index_ref(SQL_DATABASE_PATH, REF_DATABASE_NAME, DATABASE_PATH, LEGEND_NAME)

    for file_name in set(spectra_files):
        load_spectra_ref(SQL_DATABASE_PATH, REF_DATABASE_NAME, "Database\___" + file_name.split("_")[0], file_name)

