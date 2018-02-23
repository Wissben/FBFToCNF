from antlr4 import *
from gramLexer import gramLexer
from gramParser import gramParser
from TransformListener import TransformListener
from Formula import Formula


def getFormula(string):
    Formula.restart()
    lexer = gramLexer(InputStream(string))
    stream = CommonTokenStream(lexer)
    parser = gramParser(stream)
    transformer = TransformListener()
    parser.addParseListener(transformer)
    parser.form()

    return transformer.getFormula()


def getCNFClauses(string):
    return getFormula(string).getClauses()

def convertClausesToDIMACS(clauses,header=True,autoIdf=True):
    result = ""
    if header:
        result = "p cnf " + str(Formula.idfCount) + " " + str(len(clauses)) + "\n"
    for clause in clauses:
        s = ""
        for literal in clause:
            s += literal.getIdf(autoIdf) + " "
        result += s + "0\n"
    return result


# header = true to include DIMACS header
# autoIdf = true to auto assign identifiers from 1 to number of variables
# note if autoIdf = false, variables names must be numbers
def getDIMACS(string,header=True,autoIdf=True):
    return convertClausesToDIMACS(getCNFClauses(string),header,autoIdf)


def clausesToStr(clauses,autoIdf=True):
    result = ""
    for clause in clauses:
        if clause != clauses[0]:
            result += "^"
        result += "("+clause[0].getIdf(autoIdf)
        for i in range(1,len(clause)):
            result += "v"+clause[i].getIdf(autoIdf)
        result += ")"
    return result

