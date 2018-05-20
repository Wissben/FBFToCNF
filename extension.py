import FormulaToCNF
import os
import re

def formulaIsSatisfied(formula):
    dimacs = FormulaToCNF.getDIMACS(formula)
    if dimacs.count('\n') == 1:
        return False
    outF = open("out.cnf", "w+r")
    # print dimacs
    outF.write(dimacs)
    outF.seek(0)
    os.system(" ./ubcsat -alg saps -solve -i out.cnf >result")
    res = "# Solution found for -target 0\n"
    sat = False
    with open("result", "r") as f:
        for line in f:
            if line == res:
                sat = True
    return sat


def inTh(W,formula):
    if formula == "":
        return True
    if len(W) == 0:
        return False
    Ens = list(W)
    Ens.append(n(formula))
    return not satisfied(Ens)

def satisfied(W):
    concat = ""
    for w in W:
        concat += "(" + w + ")^"
    concat = concat[0:-1]
    return formulaIsSatisfied(concat)

def default(d):
    res = re.split("(.*):(.+)/(.+)",d)
    return res[1], res[2].split(','),res[3]


def n(s):
    return "-"+s



def getExtensions(W,D):
    # print "entered!!"
    # print W
    # print D
    extensions = []
    gama = list(W)
    appliedDefault = False
    for d in D:
        # print d
        pre, justs, result = default(d)
        if inTh(gama,pre) and result not in gama: #usable
            # print "usable:::"
            app = True
            for j in justs:
                if inTh(gama,n(j)): #not applicable
                    app = False
            if app:
                appliedDefault = True
                g = list(gama)
                g.append(result) # add default result to gama
                D2 = list(D)
                D2.remove(d) # remove default from defaults set
                # print g
                # print D2
                ex = getExtensions(g,D2) # get possible extensions after applying default
                def extandable(extension):
                    for j in justs:
                        if inTh(extension,n(j)):
                            return False
                    return True

                ex = [x for x in ex if extandable(x)]
                extensions.extend(ex)
                # print "ex is: "
                # print ex

                # we suppose one of justs is false
                for j in justs:
                    E = list(gama)
                    E.append(n(j))
                    ex = getExtensions(g, D2)  # get possible extensions if default not applicable
                    rEx = [x for x in ex if n(j) in x] #E = Gama
                    # print ex
                    # print rEx
                    extensions.extend(rEx)

    # print "exited!!"
    # print appliedDefault
    # print str(W) + " is " + str(satisfied(W))
    if not appliedDefault and satisfied(W):
        return [list(W)]
    # print "extension: " + str(extensions)
    return extensions



# W set of formulas
W = ["a","a -> b", "c v a", "-c"]
W2 = ["a -> b ^ c","-t v a","d -> t","d","f -> e"]
D2 = ["b ^ d:f/f","e:p/p","f:-p/-p"]
D = ["c:d/d"]
print getExtensions(W2,D2)