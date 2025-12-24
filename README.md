# Projet Social Network Analysis: Communautés Hybrides
Christian KNAYZEH - Jean Patrick Habib KOFFI

PSB - MSc. Data Management 2025-2026

## Contexte
Dans ce projet, nous étudions la communauté hybrides des humains et les agents autonômes (alimentés par les modèles de langages naturels LLM) sur Twitter/X.

## Navigation du répèrtoire
```
Projet/
├──data/
| ├── processed/
| | ├── edges.csv # liste des arretes en format csv, délimité par des virgules
| | └── nodes.csv # liste des noeuds en format csv, délimité par des virgules
| ├── raw/  # données brutes en format JSON, organisé par catégorie
| | ├── Mentions/
| | ├── Profiles/
| | ├──Tweets/
| | ├──OriginalListCookie.fun.csv # liste de metadonnées des utilisateurs en format csv, délimité par des ";"
| | ├──OriginalListCookie.fun final.xlsx # liste de metadonnées des utilisateurs en format Excel (pas utilisée)
| | └──OriginalListCookie.fun.xlsx # liste de metadonnées des utilisateurs en format Excel (pas utilisée)
├── env
| └── requirements.txt # fichier txt des recommendations pour la version de Python utilisée, avec la liste des modules utilisés
├── figures # dossier pour stocker les figures générées
├── logs
| └── pipeline.log # log de l'ingestion des données brutes pour les transformer en listes d'arretes et noeuds
├── notebooks
├── scripts
| ├── build_nodes_edges.py
| ├── config.py
| ├── logger.py
| ├── parse_interactions.py
| └── parse_profiles.py
└── TP_Hybrids_communities.docx # Énoncé du projet!
```
## Les données brutes

Les données brutes sont stockées sous format JSON dans le dossier `/data/raw`
* Mentions: Les tweets contenant des mentions dans les tweets.
* Profiles: Les metadonnées de chaque utilisateur, trouvé directement sur leur page Twitter/X.
* Tweets: les metadonnées sur les tweets de chaque utilisateur.

## Les scripts

* `build_nodes_and_edges.py`: 
  * `build_nodes_and_edges`: fonction qui utilise le reste des scripts pour transformer les données brutes.
  * `save_nodes_and_edges`: fonction pour sauvegarder les listes d'arretes et noeuds dans `/data/processed/`
  
  Ce script est utilisé une seule fois pour la génération des deux listes `edges.csv` et `nodes.csv`.
* `config.py`: Ce script est utilisé pour définir les constantes globales (les repertoires des fichiers)
* `logger.py`: Ce script est pour gérer les log d'execution de `build_nodes_and_edges.py`.
* `parse_interactions.py` :
  * parse_twitter_date: fonction pour récupérer la date de chaque tweet. Retourne `None` si la date n'est pas proprement formatée.
  * `extract_edges_from_tweet`: trouve les arretes entre l'utilisateur et les mentions à partir d'un tweet. Retourne la liste des arretes généré par chaque tweet.
  * `parse_folder`: fonction pour parcourir les dossiers dans le répertoire `/data/raw/`
  * `parse_all_interactions`: fonction qui parcours les fichiers dans `/data/raw/` et utilise le reste des fonctions définies dans ce script. Retourne les utilisateurs avec leurs arretes avec leurs voisins.
* `parse_profiles.py`: 
  * `load_agents_from_profiles`: retrouve les agents autonômes dans les données brutes. Retourne un dictionnaire des agents autonômes
  * `load_agents_from_cookie_list`: retrouve les agents à partir du fichier `OriginalListCookie.fun.csv`. Retourne un dictionnaire des agents autonômes.
  * `load_all_agents`: fonction pour mettre à jour le dictionnaire des agents autonômes. Utilise une combinaison du fichier `OriginalListCookie.fun.csv` et les données brutes pour minimiser les valeurs manquantes.
