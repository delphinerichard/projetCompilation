#!/usr/bin/python

## 	@package tdi
# 	package pour la table des identificateurs
#

class tdi:
    def __init__(self):
        self.table = []

    #ajout d'une variable dans la TDI
    def ajoutVar(self, nom, type, portee, adresse):
        nouvelleVar = {'nom': nom, 'type': type, 'portee': portee, 'adresse': adresse}
        self.table.append(nouvelleVar)

    #ajout de l'identificateur d'une fonction dans la TDI
    def ajoutFonc(self, nom, portee, nomArg, modePassage, typeRes):
            nouvelleFonc = {'nom': nom, 'portee': portee, 'nomArg': nomArg, 'modePassage': modePassage, 'typeRes': typeRes}
            self.table.append(nouvelleFonc)

    #Ajout d'un argument dans la TDI
    def ajoutArg(self, nom, type, adresse):
        nouvelArg = {"nom": nom, "type": type, "portee": "ARG", "adresse": adresse}
        self.table.append(nouvelArg)

    #permet de vérifier si une variable est dans la TDI (pour l'instant, il faudra changer avec la portée de la variable)
    def contient(self, variable):
        for i in self.table:
            if(i["nom"] == variable):
                return True
        return False

    def isType(self, variable, type):
        if not (self.contient(variable)):
            raise Exception("La variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in self.table:
                if(i["nom"] == variable and i["type"] == type):
                    return True
            return False

    def getType(self, variable):
        if not (self.contient(variable)):
            raise Exception("La variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in self.table:
                if(i["nom"] == variable):
                    return i["type"]

    def noLignes(self, variable):
        if not (self.contient(variable)):
            raise Exception("La variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in range(0, len(self.table)-1):
                if(table[i]["nom"] == variable):
                    return i
    
    # Renvoie le type de la variable qui correspond à l'adresse en paramètre
    def typeFromAddre(self, addr):
        if(len(self.table) > addr):
            raise Exception("Il n'y a pas de variable à l'adresse {}".format(addr))
        else :
            return self.table[addr]["type"
]