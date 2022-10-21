## Repozytorium zawiera skrypty wspomagające przetwarzanie i obróbkę danych:
- **make_index.py** - skrypt tworzący SQL'owe bazy danych dla białek znajdujących się w bazie dabych (każda taka baza składa się z: głównej tabeli zawierającej legendę,
osobnych tabel zawierających widma),
- **make_index_ref.py** - skrypt tworzący SQL'ową bazę danych dla widm referencyjnych,
- **plot_spectrum.py** - skrypt przedstawiający przykładowy sposób dostępu do danych z baz SQL'owych,
- **calculate_ratio.py** - skrypt tworzący plik .csv zawierający wyliczone z widm referencyjnych ratios (stosunek intensywności przy wybranych długościach fal),
- **translate_sequences.py** - skrypt zawierający funkcje pomocnicze służące to translacji sekwencji aminokwasowych na reprezentacje numeryczne,

## Repozytorium zawiera też następujące katalogi:
- **Database** - tam należy umieścić surową bazę danych,
- **SQLDatabase** - do tego katalogu będą zapisywane wygenerowane SQL'owe bazy danych oraz plik .csv z wyznaczonymi ratios,
- **Sequences** - katalog zawierający sekwencje inputowe,
- **Outputs** - katalog zawierający przykładowe outputy
