# TP Bac - INFEM, partie Temps réel

Le TP Bac porte sur la synchronisation à l'aide de sémaphores. L'application porte sur la synchronisation entre 10 voitures et un bac.

Les fichiers sont organisés:

* `tpBac.py`: fichier à modifier: indiquer le code principal du bac et des voitures
* `sys/`: mécanisme de synchronisation avec les sémaphore, indépendamment de l'application
* `bac/`: fichiers internes pour l'application complète.

## Installation

Le fichier requiert **Python 3** (testé avec Python 3.6.9, 3.8.5 et 3.11.2) et dépend de 2 bibliothèques externes:

```sh
pip install PyQt5 fysom
```

## Exécution
Après avoir modifier le fichier `tpBac.py`, il faut *exécuter*, soit par un double-clic, soit en ligne de commande:

```
python3 tpBac.py
```
