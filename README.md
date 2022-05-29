# Introduction

## Problème de flot maximum
Le problème de flot maximum consiste à trouver, dans un réseau de flot, un flot réalisable depuis une source unique et vers un puits unique qui soit maximum.

## Problème du flot de coût minimum

Le problème du flot de coût minimum consiste à trouver la manière la plus économe d'utiliser
un réseau de transport tout en satisfaisant les contraintes de production et de demande des nœuds du réseau.

# Flot maximum

Pour résoudre le problème du flot maximum nous allons utiliser l'algorithme de Ford-Fulkerson.
Le principe est le suivant : Tant qu'il existe un chemin entre la source et le puits dans le graphe
résiduel, il faut envoyer le minimum des capacités résiduelles sur ce chemin.
Dans l'algo, l'utilisation de BFS est nécessaire pour savoir s'il existe un chemin de s à t et
ainsi faire les opérations sur les arêtes pour les mettre à jour. Si un chemin existe alors nous
cherchons le flot minimum de t à s dans le chemin que nous avons trouver. Une fois trouver, ce
flot est ajouté au flot maximum. Une deuxième passe de t à s est nécessaire pour mettre à jour
les flots et cela va provoquer la saturation de certaines arêtes.
Dans le graphe ci-dessous nous pouvons voir un exemple applicatif de l'algo qui tourne du
nœud 1 au nœud 6.
On peut dire que le flot maximum est la somme du flot de la coupe minimum qui dans notre
cas est 0 → 2, 0 → 1 donc 15 + 8 = 23, ce graphe à un flot maximum de 23.

![graph-example](./img/max-flow.png)

# Flot maximum de coût minimum

Pour le problème du flot de coût minimum le principe est presque le même, a la place d'utiliser
BFS nous utilisons un algorithme de plus court chemin nommé Bellman-Ford qui permet de
détecter les cycles négatifs. Le principe est le suivant : tant qu'il existe un plus court chemin de
s a t, on cherche le flot minimum du chemin et on l'ajoute au flot maximum. Ensuite on met a
jour les capacités de flot et on rajoute le coût de l'arête fois le flot minimal du plus court chemin
actuel.

![graph-min-cost](./img/min-cost-max-flow.png)

# Coupe minimum

Une coupe minimum d'un graphe est un ensemble de sommets contenant un nombre minimal
d'arêtes. Lors du déroulement des algos de flot maximum nous allons ajouter dans une liste toutes
les arêtes qui sont saturés pour ensuite pouvoir déterminer la coupe minimum.
Pour trouver la coupe minimum d'un graphe il va falloir chercher parmi nos arcs saturés s'il
existe un chemin de s à u et s'il n'existe pas de chemin de s à v, si cette condition est validé alors
cet arc fait partie de la coupe minimum.