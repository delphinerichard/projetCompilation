import sys

def program(i):
	if(lignes[i]=="debutProg"):
		debutProg(2)
	else:
		print ("Erreur : le programme ne commence pas par debutProg")

def debutProg(i):
	while (not("finProg" in lignes[i])):	
		if ("reserver" in lignes[i]):
			i += 1
		elif ("affectation" in lignes[i]):
			affectation(i)
			i += 1
		elif("add" in lignes[i]):
			addition(i)
			i += 1
		elif("empiler" in lignes[i]):
			if ("valeurPile" in lignes[i+1]):
				empiler_pile(pile,  pile[int(retrouver_parametre(lignes[i]))])
				i += 2
			else:
				empiler_pile(pile, retrouver_parametre(lignes[i]))
				i += 1
		elif("egal" in lignes[i]):
			egal(i)
			i += 1
		elif("tze" in lignes[i]):
			if(pile[int(len(pile)-1)]):
				depiler_pile(pile)			
				i += 1
			else:
				depiler_pile(pile)
				i = retrouver_parametre(lignes[i])
		elif("tra" in lignes[i]):
			i = retrouver_parametre(lignes[i])
		else:
			print ("ligne"+i+":"+lignes[i])
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
		


def affectation(i):
	nb = pile[int(len(pile)-1)]
	depiler_pile(pile)
	adresse = pile[int(len(pile)-1)]
	if (len(pile)-1>int(adresse)):
		depiler_pile(pile)
	pile[int(adresse)] = nb

def addition(i):
	nb1 = pile[int(len(pile)-1)]
	depiler_pile(pile)
	nb2 = pile[int(len(pile)-1)]
	depiler_pile(pile)
	nb3 = int(nb1)+int(nb2)
	empiler_pile(pile, nb3)

def egal(i):
	nb1 = pile[int(len(pile)-1)]
	depiler_pile(pile)
	nb2 = pile[int(len(pile)-1)]
	depiler_pile(pile)
	if(int(nb1)==int(nb2)):
		empiler_pile(pile, True)
	else:
		empiler_pile(pile, False)



def empiler_pile(pile,x):
	pile.append(x)

def depiler_pile(pile):
	pile.pop()
		

########################################################################				 	
def main():
 
	#for fichier in lignes :
		#program(f)

	program(1)

	print (pile)
			

########################################################################
pile=[]


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