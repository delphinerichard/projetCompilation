import sys
#import tdi
from tdi import tdi


def program(i, errors) :
    if(lignes[i]=="debutProg") :
        debutProg(2, errors)
    else :
        errors = True
        print ("Erreur : le programme ne commence pas par debutProg")
        

def debutProg(i, errors):
    while ((not("finProg" in lignes[i])) and (errors == False)):
        # Reserve de la place pour les variables	
        if ("reserver" in lignes[i]):
            reserver(retrouver_parametre(lignes[i]))
            i += 1

        # Operations unaires	
        elif("moins" == lignes[i]):
            moins()
            i += 1
        elif("non" == lignes[i]):
            not_logique()
            i += 1

        # Affecte une valeur a une variable
        elif ("affectation" == lignes[i]):
            tmp = affectation()
            if (tmp == -1):
                errors = True
            i += 1

        # Operateurs binaires
        elif("add" == lignes[i]):
            addition()
            i += 1
        elif("mult" == lignes[i]):
            mult()
            i += 1
        elif("div" == lignes[i]):
            div()
            i += 1
        elif("sous" == lignes[i]):
            sous()
            i += 1
        elif("et" == lignes[i]):
            and_logique()
            i += 1
        elif("ou" == lignes[i]):
            or_logique()
            i += 1

        # Operation d'empilement
        elif("empiler" in lignes[i]):
            if ("valeurPile" == lignes[i+1]):
                empiler_pile(pile,  pile[int(retrouver_parametre(lignes[i]))])
                i += 2
            else:
                empiler_pile(pile, retrouver_parametre(lignes[i]))
                i += 1

        # Tests booleens
        elif("egal" == lignes[i]):
            egal()
            i += 1
        elif("infeg" == lignes[i]):
            infeg()
            i += 1
        elif("sup" == lignes[i]):
            sup()
            i += 1
        elif("diff" == lignes[i]):
            diff()
            i += 1

        # If et for et while
        elif("tze" in lignes[i]):
            if(pile[int(len(pile)-1)]):
                depiler_pile(pile)			
                i += 1
            else:
                depiler_pile(pile)
                i = retrouver_parametre(lignes[i])
        elif("tra" in lignes[i]):
            i = retrouver_parametre(lignes[i])

        # Entree et sortie du programme
        elif("put" == lignes[i]):
            (b, tmp) = put()
            if (b == False): # Il y a eu une erreur
                errors = True
            else :
                print(tmp)
            i += 1
        elif("get" == lignes[i]):
            tmp = get()
            if (tmp == -1):
                errors = True
            i += 1

        # Erreurs
        else:
            print("ligne",i,":",lignes[i])
            i += 1


def retrouver_parametre(ligne):
    tab = []
    compteur = False
    for i in ligne:
        if(i == ")"):
            compteur = False
        if(compteur):
            tab.append(i)
        if(i == "("):
            compteur = True
    nb = 0
    for j in range(len(tab)):
        nb += int(tab[j])*(10**(len(tab)-1-j))
    return nb


def reserver(i):
    for i in range(0, i):
        empiler_pile(pile, None)

def moins():
    b = pile[int(len(pile)-1)]
    depiler_pile(pile)
    empiler_pile(pile, -b)

def not_logique():
    b = pile[int(len(pile)-1)]
    depiler_pile(pile)
    empiler_pile(pile, (b+1)%2)

def and_logique():
    b1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    b2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    if(b1 and b2):
        empiler_pile(pile, 1)
    else:
        empiler_pile(pile, 0)

def or_logique():
    b1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    b2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    if(b1 or b2):
        empiler_pile(pile, 1)
    else:
        empiler_pile(pile, 0)

def affectation():
    # On ne peut avoir que des booléens ou des entiers relatifs 
    elt = pile[int(len(pile)-1)] # elt est donc soit un bool, soit un int
    depiler_pile(pile)
    adresse = pile[int(len(pile)-1)] # adresse est l'adresse de la variable dans laquelle on veut ranger elt
    if (len(pile)-1>int(adresse)): # On vérifie si l'adresse est valide
        depiler_pile(pile)
    # On vérifie si les types de la variable et de l'élément sont compatibles
    if ((elt == "True") or (elt == "true") or (elt == "False") or (elt == "false")) : # elt est un booléen
        # Il faut donc que la variable dépilée soit un booléen
        if(MaTDI.typeFromAddr(adresse) == bool) :
            pile[int(adresse)] = elt
            return 0
        else :
            print("Error : Les types de la variable et de l'élément à affecter ne sont pas compatibles")
            return -1
    else : # elt est un entier
        if(MaTDI.typeFromAddr(adresse) == bool) :
            print("Error : Les types de la variable et de l'élément à affecter ne sont pas compatibles")
            return -1
        else :
            pile[int(adresse)] = elt
            return 0

def addition():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb3 = int(nb1)+int(nb2)
    empiler_pile(pile, nb3)

def diff():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb3 = int(nb1)!=int(nb2)
    empiler_pile(pile, nb3)

def div():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb3 = nb2/nb1
    print(nb1, nb2, nb3)
    empiler_pile(pile, nb3)

def sous():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb3 = int(nb2)-int(nb1)
    empiler_pile(pile, nb3)

def mult():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb3 = int(nb1)*int(nb2)
    empiler_pile(pile, nb3)

def egal():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    if(int(nb1)==int(nb2)):
        empiler_pile(pile, True)
    else:
        empiler_pile(pile, False)

def infeg():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    if(int(nb2)<=int(nb1)):
        empiler_pile(pile, True)
    else:
        empiler_pile(pile, False)

def sup():
    nb1 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    nb2 = pile[int(len(pile)-1)]
    depiler_pile(pile)
    if(int(nb2)>int(nb1)):
        empiler_pile(pile, True)
    else:
        empiler_pile(pile, False)

def put():
    elt = pile[int(len(pile)-1)] # Donne l'élément en sommet de pile
    
    if(MaTDI.isType(elt, bool)) : # L'élément en sommet de pile est un booléen ; on retourne une erreur
        print("Error : On ne peut pas appliquer l'instruction put à un booléen")
        return (False, -1)

    else : # L'élément en sommet de pile n'est pas un booléen
        depiler_pile(pile) # On dépile l'élément en sommet de pile
        return (True, elt)

def get():
    x = input("Tapez une entree puis appuyez sur entree\n")
    if (x == "True" or x == "true") :
        # On interdit le booléen True pour cette instruction
        print("Error : On ne peut pas appliquer l'instruction get à un booléen")
        return -1
    elif (x == "False" or x == "false") :
        # On interdit le booléen False pour cette instruction
        print("Error : On ne peut pas appliquer l'instruction get à un booléen")
        return -1
    else :
        empiler_pile(pile, int(x))
    affectation()
    return 0


def empiler_pile(pile,x):
    pile.append(x)

def depiler_pile(pile):
    pile.pop()
    

########################################################################				 	
def main():
 
    #for fichier in lignes :
        #program(f)

    errors = False

    program(1, errors)

    if (errors == False) :
        # On n'affiche la pile que si aucune erreur n'a été soulevée par le programme
        print (pile)
        

########################################################################
pile=[]
MaTDI = tdi()


filename = sys.argv[1]

f = None
try:
    f = open(filename, 'r')
except:
    print("Error: can\'t open input file!")

fichier_entier = f.read()
lignes = fichier_entier.split("\n")

if __name__ == "__main__":
    main() 