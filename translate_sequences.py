import numpy as np

SEQUENCES_PATH = "Sequences/seq_aas_short.txt"

TRANSLATION_NUMERIC = {
    # Aminokwas: [
    #    polarność łańcucha bocznego {niepolarny -> 0, polarny -> 1},
    #    charakter chemiczny {kwaśny -> -1, obojętny -> 0, zasadowy -> 1},
    #    masa cząsteczkowa,
    #    punkt izoelektryczny,
    #    promień van deer Waalsa
    # ]

    # Alanina
    "A": [0, 0, 89.09404, 6.11, 67],

    # Cysteina
    "C": [1, 0, 121.15404, 5.05, 86],

    # Kwas asparaginowy
    "D": [1, -1, 133.10384, 2.85, 91],

    # Kwas glutaminowy
    "E": [1, -1, 147.13074, 3.15, 109],

    # Fenyloalanina
    "F": [0, 0, 165.19074, 5.49, 135],
    
    # Glicyna
    "G": [0, 0, 75.06714, 6.06, 48],

    # Histydyna
    "H": [1, 1, 155.15634, 7.60, 108],

    # Izoleucyna
    "I": [0, 0, 131.17464, 6.05, 124],

    # Lizyna
    "K": [1, 1, 146.18934, 9.60, 135],

    # Leucyna
    "L": [0, 0, 131.17464, 6.01, 124],

    # Metionina
    "M": [0, 0, 149.20784, 5.74, 124],

    # Asparagina
    "N": [1, 0, 132.11904, 5.41, 96],

    # Prolina
    "P": [0, 0, 115.13194, 6.30, 90],

    # Glutamina
    "Q": [1, 0, 146.14594, 5.65, 114],

    # Arginina
    "R": [1, 1, 174.20274, 10.76, 148],

    # Seryna
    "S": [1, 0, 105.09344, 5.68, 73],

    # Treonina
    "T": [1, 0, 119.12034, 5.60, 93],

    # Walina
    "V": [0, 0, 117.14784, 6.0, 105],

    # Tryptofan
    "W": [0, 0, 204.22844, 5.89, 163],

    # Tyrozyna
    "Y": [1, 0, 181.19124, 5.64, 141],

    # Gap
    "-": [0, 0, 0, 0, 0]
}

TRANSLATION_NUCLEO = {
    # Aminokwas: Kodon

    # Alanina
    "A": "GCU",

    # Cysteina
    "C": "UGU",

    # Kwas asparaginowy
    "D": "GAU",

    # Kwas glutaminowy
    "E": "GAA",

    # Fenyloalanina
    "F": "UUU",
    
    # Glicyna
    "G": "GGU",

    # Histydyna
    "H": "CAU",

    # Izoleucyna
    "I": "AUU",

    # Lizyna
    "K": "AAA",

    # Leucyna
    "L": "UUA",

    # Metionina
    "M": "AUG",

    # Asparagina
    "N": "AAU",

    # Prolina
    "P": "CCU",

    # Glutamina
    "Q": "CCA",

    # Arginina
    "R": "CGU",

    # Seryna
    "S": "UCU",

    # Treonina
    "T": "ACU",

    # Walina
    "V": "GUU",

    # Tryptofan
    "W": "UGG",

    # Tyrozyna
    "Y": "UAU",

    # Gap (kodon stop, bo nie jest używany przez inne aminokwasy)
    "-": "UAA"
}

NUCLEO_TO_NUMBER = {
    "A": 0.0,
    "C": 0.25,
    "G": 0.5,
    "U": 0.75
}

def translate_sequences_numeric(sequences_path: str):
    sequences = []

    with open(sequences_path, "r") as input_file:
        for line in input_file:
            if line[0] == ">":
                sequences.append([line[1:].strip()])
            else:
                sequences[-1].append(line.strip())


    for index in range(len(sequences)):
        representation = []

        for aa in sequences[index][1]:
            representation.append(TRANSLATION_NUMERIC[aa])

        representation = np.array(representation, dtype=np.float32)
        sequences[index].append(representation)

    return sequences


def translate_sequences_nucleo(sequences_path: str):
    sequences = []

    with open(sequences_path, "r") as input_file:
        for line in input_file:
            if line[0] == ">":
                sequences.append([line[1:].strip()])
            else:
                sequences[-1].append(line.strip())


    for index in range(len(sequences)):
        representation = ""

        for aa in sequences[index][1]:
            representation += TRANSLATION_NUCLEO[aa]

        representation = [NUCLEO_TO_NUMBER[nucleo] for nucleo in representation]
        representation = np.array(representation, dtype=np.float32)
        sequences[index].append(representation)

    return sequences

