from pyswip import Prolog
from misc import utils
from misc import customErrors

def _getVars(s):
    i = 0
    ret = []

    while i in range(len(s)):
        if (not utils.uppercase(s[i])):
            i += 1
        else:
            word = ""
            try:
                while utils.checkAlphanumeric(s[i]):
                    word += s[i]
                    i += 1
            except customErrors.InvalidCharsError:
                pass
            ret.append(word)

    return ret

class Manager():
    _prolog = None

    def __init__(self,rules = None, facts = None):
        self._prolog = Prolog()
        if not (rules is None):
            utils.checkFile(rules)
            self._prolog.consult(rules)
        if not (facts is None):
            utils.checkFile(facts)
            self._prolog.consult(facts)



    def consult(self, query, num_results = 1):
        ret = []
        variables = _getVars(query)

        i = 0
        for s in self._prolog.query(query):
            if(i == num_results):
                break
            i+=1
            for v in variables:
                ret.append(f"{v}={s[v]}")

        return ret

    def addFact(self,fact):
        self._prolog.assertz(fact)



