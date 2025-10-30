# Planification du raccordement électrique de bâtiments
par Hamsatou Moussa Rabiou Kalla, Khadidja Berreksi, Abdenour Touat, Maria Hendel, Manon Tessier

## Introduction
Une petite ville a été touchée par des intempéries, entraînant la destruction de plusieurs infrastructures permettant le raccordement des maisons au réseau électrique. Nous avons été embauché par la mairie afin de proposer une planification pour les travaux à effectuer, dans le but de re-raccorder tous les citoyens au réseau électrique. 
L'objectif est de rétablir rapidement la connexion pour le plus grand nombre d'habitants avec le budget le plus faible possible.
### Etat des lieux
Photo de Qgis
+explication

## Résolution du problème
### Etape nettoyage et préparation des données
Une étape essentielle et nécessaire a été de nettoyer les données.
En étudiant le fichier excel fourni par le client, nous nous sommes rendus compte que des doublons étaient présents et que les données n'étaient pas présentées sous la meilleure forme possible. 
Nous avons donc décidé de supprimer les-dits doublons, de ne plus prendre en compte les batiments encore opérationnels et de créer deux fichiers à partir du dataframe initial.
De plus, suite au différentes discussions avec le client, nous avons ajouté des données telles que le type d'infrastructure (aérien, semi-aérien, fourreau) ainsi que le prix en matériaux des différents types d'infrastrutures et le temps que prend leur réparation.
Nous avons également transformé des données en multipliant par la longueur afin d'avoir le chiffre pour l'infrastructure en entier plutôt que par mêtre. 
C'est sur ce dataframe final que nous nous baserons pour le reste du projet.

### Cas d'urgence absolu: l'hospital
En étudiant les données, il est apparu qu'un des bâtiment affecté est un hospital. Avant de traiter d'autres bâtiments, nous avons décidé de prioriser la reconstruction de celui-ci. Le client nous a informé que le générateur de l'hospital ne pouvait tenir que 20 heures avant de s'épuiser. 
Or, le bâtiment nécessite 3 infrastrustures pour fonctionner: P005500, P007990 et P007447.
P005500 nécessite 26.28 heures de réparation.
P007990 nécessite 14.23 heures de réparation.
P007447 nécessite 37.41 heures de réparation.
Le client préfère être rassuré et nous informe qu'une marge de 20% de temps est préférable. Soit une limite de 16 heures pour réparer le générateur. 

### Autres cas
Le plus difficile a été de définir une métrique prenant en compte toutes les informations du client. il y a donc eu plusieurs étapes dans la construction de celle-ci:

#### Première approche naïve
Dès le début du projet, il nous est venu plusieurs questions pour le client:
- Est-ce que l'on considère que le coût de reconstruction est proportionnel à la longueur de l'infrastructure? 
- Le but est de raccorder un maximum d'habitants. Or cette donnée n'apparait pas dans les fichiers, seul le nombre de maison par batiments est présent. Peut-on considérer le nombre d'habitants comme le nombre de maisons?
- Y'a t-il des bâtiments prioritaires?
Malheureusement, pour cette première approche, le client n'était pas disponible. Nous avons donc dû faire avec nos données telles qu'elles étaient.
Nous avons donc pris pour métrique première la difficulté liée à l'infrastucture telle que:

difficulty(infra) = la longueur de l'infra / le nombre d'habitations liées à cette infra

#### Deuxième approche
La deuxième approche est venue grâce à une discussion avec le client où nous avons eu des réponses. Celui-ci nous a confirmé que le nombre d'habitants est en fait le nombre de maisons. Nous avons également réalisé que la difficulté de l'infrastructure n'est pas la meilleure métrique pour évaluer la priorité des infrastrustures. En effet, une infrastructure en amont réparée seule ne donne pas forcément accès de manière immédiate à l'électricité. Il faut donc réfléchir autrement à comment prioriser les infrastructures. 
C'est là qu'intervient la difficulté bâtiment. Pour qu'un bâtimant retrouve l'électricité, il faut impérativement que toutes les infrastructures qui mènent à ce bâtiment soient opérationnelles. Ainsi, plutôt que de prendre chaque infrastructure individuellement, nous avons décidé de mesurer la difficulté pour chaque bâtiment telle que:

difficulty(batiment) = sum(difficulty(infra) pour toutes les infrastructures menant à ce bâtiment) 

De cette manière, on peut construire un premier algorithme: 
1. On liste tous les bâtiments à réparer
2. On crée une liste vide qui va recueillir les bâtiments au fur et à mesure qu'on les répare et va ainsi correspondre à notre ordre de priorité
3. Tant que la liste des bâtiments à réparer n'est pas vide, on calcule leur difficulté de réparation, on sélectionne le bâtiment avec la difficulté la plus faible, on le "répare", c'est à dire qu'on répare toutes ses infrastructures, on le range dans la liste des priorités et on recommence

Quand tout a été réparé, on regarde la liste de priorité et on peut déterminer les différentes phases de reconstruction.

#### Troisième approche
Ce que ça a modifié dans les calculs de difficultés

#### Approche finale


#### Conclusion 
après avoir exécuté le code...
Phase 1:
Phase 2:
Phase 3:
Argument pour chaque phase

