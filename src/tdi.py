#!/usr/bin/python

## 	@package tdi
# 	package pour la table des identificateurs
#

class tdi:
<<<<<<< HEAD

=======
>>>>>>> 9194d824847d43056a6a23341dd314eecbabce22
    def __init__(self):
        self.table = []

    #ajout d'une variable dans la TDI
    def ajoutVar(self, nom, type, portee, adresse):
<<<<<<< HEAD
        nouvelleVar = {'nom': nom, 'type': type, 'portee': portee, 'adresse': adresse}
        self.table.append(nouvelleVar)
=======
        if(self.contient(nom)):
            raise Exception("Le nom de cette variable est deja utilise")
        else:
            nouvelleVar = {'nom': nom, 'type': type, 'portee': portee, 'adresse': adresse}
            self.table.append(nouvelleVar)
>>>>>>> 9194d824847d43056a6a23341dd314eecbabce22

    #ajout de l'identificateur d'une fonction dans la TDI
    def ajoutFonc(self, nom, portee, nomArg, modePassage, typeRes):
            nouvelleFonc = {'nom': nom, 'portee': portee, 'nomArg': nomArg, 'modePassage': modePassage, 'typeRes': typeRes}
            self.table.append(nouvelleFonc)

    #Ajout d'un argument dans la TDI
    def ajoutArg(self, nom, type, adresse):
        nouvelArg = {'nom': nom, 'type': type, 'portee': "ARG", 'adresse': adresse}
        self.table.append(nouvelArg)

<<<<<<< HEAD
    #permet de verifier si une variable est dans la TDI (pour l'instant, il faudra changer avec la portee de la variable)
=======
    #permet de vérifier si une variable est dans la TDI (pour l'instant, il faudra changer avec la portée de la variable)
>>>>>>> 9194d824847d43056a6a23341dd314eecbabce22
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
<<<<<<< HEAD
        
    
=======

>>>>>>> 9194d824847d43056a6a23341dd314eecbabce22
    def noLigne(self, variable):
        if not (self.contient(variable)):
            raise Exception("la variable {} n'existe pas dans la table des identificateurs".format(variable))
        else:
            for i in range(0, len(self.table)-1):
<<<<<<< HEAD
                if(self.table[i]["nom"] == variable):
                    return i
                
    def afficherTable(self):
        return self.table

    #renvoie le type de la variable qui correspond a l'adresse en parametre
=======
                if(table[i]["nom"] == variable):
                    return i

>>>>>>> 9194d824847d43056a6a23341dd314eecbabce22
    def typeFromAddr(self, addr):
        if (len(self.table) > addr):
            raise Exception("Il n'y a pas de variable à l'adresse {}".format(addr))
        else:
            return self.table[addr]["type"]
<<<<<<< HEAD


=======
>>>>>>> 9194d824847d43056a6a23341dd314eecbabce22
