import FormulaToCNF

# insert here any propositional logic formula
# creating a formula
formula = FormulaToCNF.getFormula("a -> (b v k) ^ c")
print formula.toStr()

# converting -> and <->
formula.convertToAO()
print formula.toStr()

# printing clauses
print FormulaToCNF.clausesToStr(formula.getClauses(),False)

# creating DIMACS format of formula directly from string
dimacs = FormulaToCNF.getDIMACS("(1 -> 2)v 3",False,False)
print dimacs
file = open("out.cnf", "w")
file.write(dimacs)
file.close()
