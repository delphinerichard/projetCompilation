#!/usr/bin/python

## 	@package anasyn
# 	Syntactical Analyser package. 
#


#

import sys, argparse, re
import logging

import analex
from tdi import tdi

logger = logging.getLogger('anasyn')

DEBUG = False
LOGGING_LEVEL = logging.DEBUG


class AnaSynException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
                return repr(self.value)

########################################################################				 	
#### Syntactical Diagrams
########################################################################				 	

def program(lexical_analyser):
	specifProgPrinc(lexical_analyser)
	lexical_analyser.acceptKeyword("is")
	corpsProgPrinc(lexical_analyser)
	
def specifProgPrinc(lexical_analyser):
	lexical_analyser.acceptKeyword("procedure")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of program : "+ident)
	
def  corpsProgPrinc(lexical_analyser):
	code.write("\ndebutProg\n")
	if not lexical_analyser.isKeyword("begin"):
		logger.debug("Parsing declarations")
		partieDecla(lexical_analyser)
		logger.debug("End of declarations")
	lexical_analyser.acceptKeyword("begin")

	if not lexical_analyser.isKeyword("end"):
		logger.debug("Parsing instructions")
		suiteInstr(lexical_analyser)
		logger.debug("End of instructions")
	lexical_analyser.acceptKeyword("end")
	code.write("finProg")
	lexical_analyser.acceptFel()
	logger.debug("End of program")
	
def partieDecla(lexical_analyser):
	if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
		listeDeclaOp(lexical_analyser)
	if not lexical_analyser.isKeyword("begin") :
    		listeDeclaVar(lexical_analyser, 0)               

def listeDeclaOp(lexical_analyser):
	declaOp(lexical_analyser)
	lexical_analyser.acceptCharacter(";")
	if lexical_analyser.isKeyword("procedure") or lexical_analyser.isKeyword("function") :
		listeDeclaOp(lexical_analyser)

def declaOp(lexical_analyser):
	if lexical_analyser.isKeyword("procedure"):
		procedure(lexical_analyser)
	if lexical_analyser.isKeyword("function"):
		fonction(lexical_analyser)

def procedure(lexical_analyser):
	lexical_analyser.acceptKeyword("procedure")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of procedure : "+ident)
       
	partieFormelle(lexical_analyser, ident)

	lexical_analyser.acceptKeyword("is")
	identifierTable.ajoutProc(ident, numero_ligne()+2)

	corpsProc(lexical_analyser)
       

def fonction(lexical_analyser):
	lexical_analyser.acceptKeyword("function")
	ident = lexical_analyser.acceptIdentifier()
	logger.debug("Name of function : "+ident)
	
	partieFormelle(lexical_analyser, ident)
	
	lexical_analyser.acceptKeyword("return")
	typ = nnpType(lexical_analyser)
        
	lexical_analyser.acceptKeyword("is")
	identifierTable.ajoutFonc(ident, numero_ligne()+2, typ)
	corpsFonct(lexical_analyser)



def corpsProc(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	code.write("tra\n")
	lieu_tra = numero_ligne()
	suiteInstr(lexical_analyser)
	code.write("retourProc\n")
	modif_ligne(lieu_tra, "tra("+str(numero_ligne()+1)+")")
	lexical_analyser.acceptKeyword("end")

def corpsFonct(lexical_analyser):
	if not lexical_analyser.isKeyword("begin"):
		partieDeclaProc(lexical_analyser)
	lexical_analyser.acceptKeyword("begin")
	code.write("tra\n")
	lieu_tra = numero_ligne()
	suiteInstrNonVide(lexical_analyser)
	modif_ligne(lieu_tra, "tra("+str(lieu_retour+1)+")")
	lexical_analyser.acceptKeyword("end")

def partieFormelle(lexical_analyser, nom):
	lexical_analyser.acceptCharacter("(")
	if not lexical_analyser.isCharacter(")"):
		listeSpecifFormelles(lexical_analyser, 0, nom)
	lexical_analyser.acceptCharacter(")")

def listeSpecifFormelles(lexical_analyser, compteurArg, nom):
	specif(lexical_analyser, compteurArg, nom)
	if not lexical_analyser.isCharacter(")"):
		lexical_analyser.acceptCharacter(";")
		listeSpecifFormelles(lexical_analyser, compteurArg+1, nom)

def specif(lexical_analyser, compteurArg, nom):
	listeIdent(lexical_analyser, [])
	lexical_analyser.acceptCharacter(":")
	if lexical_analyser.isKeyword("in"):
		mde = mode(lexical_analyser)
                
	typeVar = nnpType(lexical_analyser)
	for i in range (len(liste)):
		identifierTable.ajoutArg(liste[i], typeVar, mde, nom, compteurArg)


def mode(lexical_analyser):
	lexical_analyser.acceptKeyword("in")
	if lexical_analyser.isKeyword("out"):
		lexical_analyser.acceptKeyword("out")
		logger.debug("in out parameter")
		return ("in out")                
	else:
		logger.debug("in parameter")
		return ("in")

def nnpType(lexical_analyser):
	typeVar = ""
	if lexical_analyser.isKeyword("integer"):
		lexical_analyser.acceptKeyword("integer")
		typeVar = "integer"
		logger.debug("integer type")
	elif lexical_analyser.isKeyword("boolean"):
		lexical_analyser.acceptKeyword("boolean")
		typeVar = "boolean"
		logger.debug("boolean type")
	else:
		msg = "Error : Une variable doit avoir un type connu ('integer' ou 'boolean') a sa declaration."
		logger.error(msg)
		raise AnaSynException(msg)
	return typeVar

def partieDeclaProc(lexical_analyser):
	listeDeclaVar(lexical_analyser, 0)

def listeDeclaVar(lexical_analyser, compteurVar):
	declaVar(lexical_analyser, compteurVar)
	if lexical_analyser.isIdentifier():
		listeDeclaVar(lexical_analyser, compteurVar+1)

def declaVar(lexical_analyser, compteurVar):
	listeIdent(lexical_analyser, [])
	code.write("reserver("+str(compteur+1)+")\n")
	lexical_analyser.acceptCharacter(":")
	logger.debug("now parsing type...")
	typeVar = nnpType(lexical_analyser)
	for i in range(len(liste)):
		identifierTable.ajoutVar(liste[i], typeVar, "main", i+compteurVar)
	lexical_analyser.acceptCharacter(";")

def listeIdent(lexical_analyser, listeident):
	global compteur
	global liste
	ident = lexical_analyser.acceptIdentifier()
	listeident.append(ident)
	liste = listeident
	logger.debug("identifier found: "+str(ident))
	if lexical_analyser.isCharacter(","):
		compteur += 1
		lexical_analyser.acceptCharacter(",")
		listeIdent(lexical_analyser, listeident)

def suiteInstrNonVide(lexical_analyser):
	instr(lexical_analyser)
	if lexical_analyser.isCharacter(";"):
		lexical_analyser.acceptCharacter(";")
		suiteInstrNonVide(lexical_analyser)

def suiteInstr(lexical_analyser):
	if not lexical_analyser.isKeyword("end"):
		suiteInstrNonVide(lexical_analyser)

def instr(lexical_analyser):
	if lexical_analyser.isKeyword("while"):
		boucle(lexical_analyser)
	elif lexical_analyser.isKeyword("if"):
		altern(lexical_analyser)
	elif lexical_analyser.isKeyword("get") or lexical_analyser.isKeyword("put"):
		es(lexical_analyser)
	elif lexical_analyser.isKeyword("return"):
		retour(lexical_analyser)
	elif lexical_analyser.isIdentifier():
		ident = lexical_analyser.acceptIdentifier()
		typeIdent = identifierTable.getType(ident)
		if lexical_analyser.isSymbol(":="):
			if (identifierTable.getModePassage(ident) == "in out"):
				code.write("empilerParam("+str(identifierTable.getAdresse(ident))+")\n")
			else :
				if (identifierTable.getModePassage(ident) == "in"):
					code.write("empilerAd("+str(identifierTable.getAdresse(ident))+")\n")
				else :
					code.write("empiler("+str(identifierTable.getAdresse(ident))+")\n")
			lexical_analyser.acceptSymbol(":=")
			typeElt = expression(lexical_analyser)
			if(typeIdent != typeElt) :
				msg = "Error : On ne peut affecter un element à une variable d'un type different."
				logger.error(msg)
				raise AnaSynException(msg)
			code.write("affectation\n")
			logger.debug("parsed affectation")
		elif lexical_analyser.isCharacter("("):
			lexical_analyser.acceptCharacter("(")

			code.write("reserverBloc\n")
			compteurArg =1
			if not lexical_analyser.isCharacter(")"):
				listePe(lexical_analyser)
				compteurArg +=1

			lexical_analyser.acceptCharacter(")")
			logger.debug("parsed procedure call")
			code.write("traStat("+str(identifierTable.getLigneDepart(ident))+","+str(compteurArg)+")\n")

		else:
			logger.error("Expecting procedure call or affectation!")
			raise AnaSynException("Expecting procedure call or affectation!")
		
	else:
		logger.error("Unknown Instruction <"+ lexical_analyser.get_value() +">!")
		raise AnaSynException("Unknown Instruction <"+ lexical_analyser.get_value() +">!")


def listePe(lexical_analyser):
	typeElt = expression(lexical_analyser)
	if lexical_analyser.isCharacter(","):
		lexical_analyser.acceptCharacter(",")
		listePe(lexical_analyser)

def expression(lexical_analyser):
	logger.debug("parsing expression: " + str(lexical_analyser.get_value()))

	typeElt = exp1(lexical_analyser)
	if lexical_analyser.isKeyword("or"):
		# On doit avoir des booleens
		if(typeElt != 'boolean') : 
			msg = "Error : On ne peut faire une instruction 'or' qu'avec des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		lexical_analyser.acceptKeyword("or")
		typeElt2 = exp1(lexical_analyser)
		if(typeElt2 != 'boolean') : 
			msg = "Error : On ne peut faire une instruction 'or' qu'avec des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		code.write("ou\n")
		# Si on a bien deux booleens, on aura une expression booleenne
		typeElt = 'boolean'
	return typeElt
        
def exp1(lexical_analyser):
	logger.debug("parsing exp1")
	
	typeElt = exp2(lexical_analyser)
	if lexical_analyser.isKeyword("and"):
		# On doit avoir des booleens
		if(typeElt != 'boolean') : 
			msg = "Error : On ne peut faire une instruction 'and' qu'avec des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		lexical_analyser.acceptKeyword("and")
		typeElt2 = exp2(lexical_analyser)
		if(typeElt2 != 'boolean') : 
			msg = "Error : On ne peut faire une instruction 'and' qu'avec des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		code.write("et\n")
		# S'il y a un and, on aura une expression booleenne
		typeElt = 'boolean'
	return typeElt
        
def exp2(lexical_analyser):
	logger.debug("parsing exp2")
	typeElt = exp3(lexical_analyser)
	if	lexical_analyser.isSymbol("<") or \
		lexical_analyser.isSymbol("<=") or \
		lexical_analyser.isSymbol(">") or \
		lexical_analyser.isSymbol(">="):
		if(typeElt != 'integer') : # On n'a pas un entier
			msg = "Error : On ne peut faire des tests d'inferiorite ou de superiorite qu'entre des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		op = opRel(lexical_analyser)
		typeElt2 = exp3(lexical_analyser)
		if(typeElt != 'integer') : # On n'a pas un entier
			msg = "Error : On ne peut faire des tests d'inferiorite ou de superiorite qu'entre des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		code.write(str(op))
		# Une comparaison renvoyant un booleen, notre element devient un booleen
		typeElt = 'boolean'
	elif lexical_analyser.isSymbol("=") or \
		lexical_analyser.isSymbol("/="): 
		op = opRel(lexical_analyser)
		typeElt2 = exp3(lexical_analyser)
		# Les deux elements doivent etre du meme type pour pouvoir comparer
		if(typeElt != typeElt2) :
			msg = "Error : On ne peut faire des tests d'egalite avec des elements de types differents."
			logger.error(msg)
			raise AnaSynException(msg)
		code.write(str(op))
		# Une comparaison renvoyant un booleen, notre element devient un booleen
		typeElt = 'boolean'
	return typeElt
	
def opRel(lexical_analyser):
	logger.debug("parsing relationnal operator: " + lexical_analyser.get_value())
        
	if	lexical_analyser.isSymbol("<"):
		lexical_analyser.acceptSymbol("<")
		return "inf\n"
        
	elif lexical_analyser.isSymbol("<="):
		lexical_analyser.acceptSymbol("<=")
		return "infeg\n"
        
	elif lexical_analyser.isSymbol(">"):
		lexical_analyser.acceptSymbol(">")
		return "sup\n"
        
	elif lexical_analyser.isSymbol(">="):
		lexical_analyser.acceptSymbol(">=")
		return "supeg\n"
        
	elif lexical_analyser.isSymbol("="):
		lexical_analyser.acceptSymbol("=")
		return "egal\n"
        
	elif lexical_analyser.isSymbol("/="):
		lexical_analyser.acceptSymbol("/=")
		return "diff\n"
        
	else:
		msg = "Unknown relationnal operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def exp3(lexical_analyser):
	logger.debug("parsing exp3")
	typeElt = exp4(lexical_analyser)	
	if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-"):
		if(typeElt != 'integer') : # On n'a pas un entier
			msg = "Error : On ne peut faire des additions ou des soustractions qu'entre des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		op = opAdd(lexical_analyser)
		typeElt2 = exp4(lexical_analyser)
		if(typeElt2 != 'integer') : # On n'a pas un entier
			msg = "Error : On ne peut faire des additions ou des soustractions qu'entre des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		code.write(str(op)+"\n")
	return typeElt

def opAdd(lexical_analyser):
	logger.debug("parsing additive operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("+"):
		lexical_analyser.acceptCharacter("+")
		return ("add")
	elif lexical_analyser.isCharacter("-"):
		lexical_analyser.acceptCharacter("-")
		return("sous")
                
	else:
		msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def exp4(lexical_analyser):
	logger.debug("parsing exp4")
        
	typeElt = prim(lexical_analyser)	
	if lexical_analyser.isCharacter("*") or lexical_analyser.isCharacter("/"): 
		# On ne peut faire les operations que sur des entiers
		if (typeElt != 'integer'):
			msg = "Error : On ne peut faire des multiplications ou des divisions qu'entre des entiers."
			logger.error(msg)
			raise AnaSynException(msg)
		else :
			op = opMult(lexical_analyser)
			typeElt2 = prim(lexical_analyser)
			if(typeElt2 != 'integer') :
				msg = "Error : On ne peut faire des multiplications ou des divisions qu'entre des entiers."
				logger.error(msg)
				raise AnaSynException(msg)
			code.write(str(op)+"\n")
	return typeElt
	

def opMult(lexical_analyser):
	logger.debug("parsing multiplicative operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("*"):
		lexical_analyser.acceptCharacter("*")
		return "mult"
                
	elif lexical_analyser.isCharacter("/"):
		lexical_analyser.acceptCharacter("/")
		return "div"
                
	else:
		msg = "Unknown multiplicative operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def prim(lexical_analyser):
	logger.debug("parsing prim")
	op = ""
	if lexical_analyser.isCharacter("+") or lexical_analyser.isCharacter("-") or lexical_analyser.isKeyword("not"):
		op = opUnaire(lexical_analyser)
	typeElt = elemPrim(lexical_analyser)
	if(op != ""):
		code.write(str(op))
	return typeElt

def opUnaire(lexical_analyser):
	logger.debug("parsing unary operator: " + lexical_analyser.get_value())
	if lexical_analyser.isCharacter("+"):
		lexical_analyser.acceptCharacter("+")
		return "plus\n"
                
	elif lexical_analyser.isCharacter("-"):
		lexical_analyser.acceptCharacter("-")
		return "moins\n"
                
	elif lexical_analyser.isKeyword("not"):
		lexical_analyser.acceptKeyword("not")
		return "non\n"
                
	else:
		msg = "Unknown additive operator <"+ lexical_analyser.get_value() +">!"
		logger.error(msg)
		raise AnaSynException(msg)

def elemPrim(lexical_analyser): # Cette fonction renvoie le type de l'element primitif analyse ('integer' ou 'boolean')
	logger.debug("parsing elemPrim: " + str(lexical_analyser.get_value()))
	if lexical_analyser.isCharacter("("):
		lexical_analyser.acceptCharacter("(")
		typeElt = expression(lexical_analyser)
		lexical_analyser.acceptCharacter(")")
		return typeElt
	elif lexical_analyser.isInteger() :
		valeur(lexical_analyser)
		return 'integer'
	elif lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false") :
		valeur(lexical_analyser)
		return 'boolean'
	elif lexical_analyser.isIdentifier():
		ident = lexical_analyser.acceptIdentifier()
		typeIdent = identifierTable.getType(ident)
		if lexical_analyser.isCharacter("("):			# Appel fonct
			lexical_analyser.acceptCharacter("(")
			code.write("reserverBloc\n")
			compteur =0
			if not lexical_analyser.isCharacter(")"):
				compteur +=1
				listePe(lexical_analyser)

			lexical_analyser.acceptCharacter(")")
			logger.debug("parsed procedure call")
			code.write("traStat("+str(identifierTable.getLigneDepart(ident))+","+str(compteur)+")\n")
			logger.debug("Call to function: " + ident)
		else:
			logger.debug("Use of an identifier as an expression: " + ident)
			if (identifierTable.getModePassage(ident) == "in out"):
				code.write("empilerParam("+str(identifierTable.getAdresse(ident))+")\n")
			else :
				if (identifierTable.getModePassage(ident) == "in"):
					code.write("empilerAd("+str(identifierTable.getAdresse(ident))+")\n")
				else :
					code.write("empiler("+str(identifierTable.getAdresse(ident))+")\n")
			code.write("valeurPile\n")
		return typeIdent
	else:
		logger.error("Unknown Value!")
		raise AnaSynException("Unknown Value!")

def valeur(lexical_analyser):
	if lexical_analyser.isInteger():
		entier = lexical_analyser.acceptInteger()
		code.write("empiler("+str(entier)+")\n")
		logger.debug("integer value: " + str(entier))
		return "integer"
	elif lexical_analyser.isKeyword("true") or lexical_analyser.isKeyword("false"):
		vtype = valBool(lexical_analyser)
		return vtype
	else:
		logger.error("Unknown Value! Expecting an integer or a boolean value!")
		raise AnaSynException("Unknown Value ! Expecting an integer or a boolean value!")

def valBool(lexical_analyser):
	if lexical_analyser.isKeyword("true"):
		lexical_analyser.acceptKeyword("true")
		code.write("empiler(1)\n")	
		logger.debug("boolean true value")
                
	else:
		logger.debug("boolean false value")
		lexical_analyser.acceptKeyword("false")
		code.write("empiler(0)\n")	
        
	return "boolean"

def es(lexical_analyser):
	logger.debug("parsing E/S instruction: " + lexical_analyser.get_value())
	if lexical_analyser.isKeyword("get"):
		lexical_analyser.acceptKeyword("get")
		lexical_analyser.acceptCharacter("(")
		ident = lexical_analyser.acceptIdentifier()
		# On teste si l'identifieur est bien un entier
		if (identifierTable.getType(ident) == 'integer') :
			code.write("empiler("+str(identifierTable.getAdresse(ident))+")\n")
			lexical_analyser.acceptCharacter(")")
			code.write("get\n")
			logger.debug("Call to get "+ident)
		else :
			msg = "Error : On ne peut pas appliquer l'instruction get à un booléen."
			logger.error(msg)
			raise AnaSynException(msg)
	elif lexical_analyser.isKeyword("put"):
		lexical_analyser.acceptKeyword("put")
		lexical_analyser.acceptCharacter("(")
		typeElt = expression(lexical_analyser)
		lexical_analyser.acceptCharacter(")")
		if(typeElt == 'boolean') : 
			msg = "Error : On ne peut pas appliquer l'instruction put à un booléen."
			logger.error(msg)
			raise AnaSynException(msg)
		code.write("put\n")
		logger.debug("Call to put")
	else:
		logger.error("Unknown E/S instruction!")
		raise AnaSynException("Unknown E/S instruction!")

def boucle(lexical_analyser):
	logger.debug("parsing while loop: ")
	lexical_analyser.acceptKeyword("while")

	lieu_debut = numero_ligne()+1
	typeElt = expression(lexical_analyser)
	if(typeElt != 'boolean'):
		msg = "Error : On ne peut pas appliquer l'instruction while sur une condition non booleenne."
		logger.error(msg)
		raise AnaSynException(msg)

	code.write("tze\n")
	lieu_tze = numero_ligne()

	lexical_analyser.acceptKeyword("loop")
	suiteInstr(lexical_analyser)

	code.write("tra("+str(lieu_debut)+")\n")
	lieu_fin = numero_ligne()+1
	
	modif_ligne(lieu_tze, "tze("+str(lieu_fin)+")")

	lexical_analyser.acceptKeyword("end")
	logger.debug("end of while loop ")

def altern(lexical_analyser):
	sinon = False
	logger.debug("parsing if: ")
	lexical_analyser.acceptKeyword("if")
	typeElt = expression(lexical_analyser)
	if(typeElt != 'boolean'):
		msg = "Error : On ne peut pas appliquer l'instruction if sur une condition non booleenne."
		logger.error(msg)
		raise AnaSynException(msg)

	code.write("tze\n")

	lieu_tze = numero_ligne()

	lexical_analyser.acceptKeyword("then")
	suiteInstr(lexical_analyser)

	if lexical_analyser.isKeyword("else"):
		sinon = True
		lexical_analyser.acceptKeyword("else")
		code.write("tra\n")
		lieu_tra = numero_ligne()
		modif_ligne(lieu_tze, "tze("+str(lieu_tra+1)+")")
		suiteInstr(lexical_analyser)
       
	lexical_analyser.acceptKeyword("end")

	lieu_end = numero_ligne()+1
	if(sinon):
		modif_ligne(lieu_tra, "tra("+str(lieu_end)+")")
	else:
		modif_ligne(lieu_tze, "tze("+str(lieu_end)+")")
	logger.debug("end of if")

def retour(lexical_analyser):
	global lieu_retour
	logger.debug("parsing return instruction")
	lexical_analyser.acceptKeyword("return")
	expression(lexical_analyser)
	code.write("retourFonc\n")
	lieu_retour = numero_ligne()

def numero_ligne():
	global code
	code.close()
	code_r = open("tests/code.txt", 'r')
	code_entier=code_r.read()
	lignes = code_entier.split("\n")
	ligne = len(lignes)-2
	code_r.close()
	code = open("tests/code.txt", 'a')
	return ligne

def modif_ligne(ligne, texte):
	global code
	code.close()
	code_r = open("tests/code.txt", 'r')
	code_entier=code_r.read()
	lignes = code_entier.split("\n")
	lignes[int(ligne)] = str(texte)
	code_r.close()
	code = open("tests/code.txt", 'w')
	for i in range (len(lignes)-1):
		code.write(str(lignes[i])+"\n")



	

########################################################################				 	
def main():
 	
	parser = argparse.ArgumentParser(description='Do the syntactical analysis of a NNP program.')
	parser.add_argument('inputfile', type=str, nargs=1, help='name of the input source file')
	parser.add_argument('-o', '--outputfile', dest='outputfile', action='store', \
                default="", help='name of the output file (default: stdout)')
	parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0')
	parser.add_argument('-d', '--debug', action='store_const', const=logging.DEBUG, \
                default=logging.INFO, help='show debugging info on output')
	parser.add_argument('-p', '--pseudo-code', action='store_const', const=True, default=False, \
                help='enables output of pseudo-code instead of assembly code')
	parser.add_argument('--show-ident-table', action='store_true', \
                help='shows the final identifiers table')
	args = parser.parse_args()


	filename = args.inputfile[0]
	f = None
	try:
		f = open(filename, 'r')
	except:
		print("Error: can\'t open input file!")
		return
		
	outputFilename = args.outputfile
	
  	# create logger      
	LOGGING_LEVEL = args.debug
	logger.setLevel(LOGGING_LEVEL)
	ch = logging.StreamHandler()
	ch.setLevel(LOGGING_LEVEL)
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
	ch.setFormatter(formatter)
	logger.addHandler(ch)

	if args.pseudo_code:
		True#
	else:
		False#

	lexical_analyser = analex.LexicalAnalyser()
	
	lineIndex = 0
	for line in f:
		line = line.rstrip('\r\n')
		lexical_analyser.analyse_line(lineIndex, line)
		lineIndex = lineIndex + 1
	f.close()
	

	# launch the analysis of the program
	lexical_analyser.init_analyser()
	program(lexical_analyser)
		
	if args.show_ident_table:
			print("------ IDENTIFIER TABLE ------")
			print(str(identifierTable.afficherTable()))
			print("------ END OF IDENTIFIER TABLE ------")


	if outputFilename != "":
			try:
					output_file = open(outputFilename, 'w')
			except:
					print("Error: can\'t open output file!")
					return
	else:
			output_file = sys.stdout

	# Outputs the generated code to a file
	#instrIndex = 0
	#while instrIndex < codeGenerator.get_instruction_counter():
	#        output_file.write("%s\n" % str(codeGenerator.get_instruction_at_index(instrIndex)))
	#        instrIndex += 1
		
	if outputFilename != "":
			output_file.close() 

	code.close()

########################################################################
code = open("tests/code.txt", "w")
lieu_retour = 0
code.truncate(0)
compteur =0
liste = []
identifierTable = tdi()
			 

if __name__ == "__main__":
    main() 