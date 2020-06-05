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
            nouvelleVar = {'nom': nom, 'type': type, 'portee': portee}
            self.table.append(nouvelleVar)

 
    #ajout de l'identificateur d'une fonction dans la TDI
    # nom: nom de la fonction ; nomArg: tableau avec les noms des arguments de la fonction - pabesoin a priori, typeRes: type du resultat ; ligneDepart : la ligne de depart dans code.txt
    def ajoutFonc(self, nom, ligneDepart, typeRes):
            nouvelleFonc = {'nom': nom, 'type':'FONCTION', 'ligneDepart': ligneDepart, 'typeRes': typeRes}
            self.table.append(nouvelleFonc)

    #Ajout d'un argument dans la TDI
    #nom: nom de l'argument ; type: son type ; modePassage: in ou in/out ; fonction: le nom de la fonction d'origine
    def ajoutArg(self, nom, type, modePassage, fonction):
        nouvelArg = {'nom': nom, 'type': type, 'modePassage': modePassage, 'fonction': fonction}
        self.table.append(nouvelArg)

        #Ajout d'une procedure dans la TDI
        #nom: nom de la procedure ; ligneDepart : la ligne de depart dans code.txt
    def ajoutProc(self, nom, ligneDepart):
        nouvelleProc = {'nom': nom, 'type':'PROCEDURE', 'ligneDepart': ligneDepart}
        self.table.apend(nouvelleProc)

    #permet de verifier si une variable est dans la TDI (pour l'instant, il faudra changer avec la portee de la variable)
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
                if(self.table[i]["nom"] == variable):
                    return i
                
    def afficherTable(self):
        return self.table

    #renvoie le type de la variable qui correspond a l'adresse en parametre
    def typeFromAddr(self, addr):
        if (len(self.table) > addr):
            raise Exception("Il n'y a pas de variable a l'adresse {}".format(addr))
        else:
            return self.table[addr]["type"]


    def getLigneDepart(self, variable):
        if not (self.contient(variable)):
            raise Exception("la variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in self.table:
                if((i["type"] == "PROCEDURE" or i["type"] == "FONCTION") and i["nom"] == variable):
                    return i["ligneDepart"]
