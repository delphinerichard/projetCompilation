#!/usr/bin/python

## 	@package tdi
# 	package pour la table des identificateurs
#

class tdi:
    def __init__(self):
        self.table = []

    #ajout d'une variable dans la TDI
    #nom: nom de la variable ; type: type de la variable ; portee: main ou nom de la fonction dans laquelle elle est declaree 
    def ajoutVar(self, nom, type, portee):
        if(self.contient(nom)):
            raise Exception("Le nom de cette variable est deja utilise")
        else:
            nouvelleVar = {'nom': nom, 'type': type, 'portee': portee, 'fonctionOrigine': fonctionOrigine}
            self.table.append(nouvelleVar)

    #ajout de l'identificateur d'une fonction dans la TDI
    # nom: nom de la fonction ; nomArg: tableau avec les noms des arguments de la fonction - pabesoin a priori, typeRes: type du résultat
    def ajoutFonc(self, nom, typeRes):
            nouvelleFonc = {'nom': nom, 'type':'FONCTION' 'portee': portee, 'nomArg': nomArg, 'modePassage': modePassage, 'typeRes': typeRes}
            self.table.append(nouvelleFonc)

    #Ajout d'un argument dans la TDI
    #nom: nom de l'argument ; type: son type ; modePassage: in/out ; fonction: le nom de la fonction d'origine
    def ajoutArg(self, nom, type, modePassage, fonction):
        nouvelArg = {'nom': nom, 'type': type, 'portee': "ARG", 'adresse': adresse}
        self.table.append(nouvelArg)

    #permet de vérifier si une variable est dans la TDI (pour l'instant, il faudra changer avec la portée de la variable)
    def contient(self, variable):
        for i in self.table:
            if(i["nom"] == variable):
                return True
        return False

    def isType(self, variable, type):
        if not (self.contient(variable)):
            raise Exception("la variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in self.table:
                if(i["nom"] == variable and i["type"] == type):
                    return True
            return False

    def getType(self, variable):
        if not (self.contient(variable)):
            raise Exception("la variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in self.table:
                if(i["nom"] == variable):
                    return i["type"]

    def noLigne(self, variable):
        if not (self.contient(variable)):
            raise Exception("la variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in range(0, len(self.table)):
                if(table[i]["nom"] == variable):
                    return i

    #renvoie le type de la variable qui correspond a l'adresse en parametre
    def typeFromAddr(self, addr):
        if (len(self.table) > addr):
            raise Exception("Il n'y a pas de variable à l'adresse {}".format(addr))
        else:
            return self.table[addr]["type"]
