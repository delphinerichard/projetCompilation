# Projet de Compilation

## Manon Doyelle, Killian Levyn, Marie Peter, Louis-Maxime Piton, Delphine Richard - Informatique 2

### Juin 2020

Ce git est dédié au projet de compilation du groupe DodoCorp. Vous trouverez ci-après les instructions pour lancer le programme.

## Prérequis 

* Un PC sous Windows ou Linux avec Python 3

## Lancement du programme :

Pour lancer le programme, aller dans la console 

``` ./compilateur.sh [adresse du fichier .nno à tester] ​```

## Structure du projet

Le projet repose sur les programmes suivants :

* ```analex.py``` est l'analyseur lexical du compilateur. Ce fichier était fourni et nous ne l'avons pas modifié.
* ```anasyn.py``` est l'analyseur syntaxique du compilateur, qui lit le programme .nno et produit un fichier ```code.txt``` contenant le code compilé
* ```machine_virtuelle.py``` est la machine virtuelle qui permet d'exécuter le code compilé dans ```code.txt``
* ```tdi.py``` contient les méthodes nécessaires à la manipulation de la table des identificateurs