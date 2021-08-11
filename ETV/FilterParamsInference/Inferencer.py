from misc import Bot
from misc import utils
from sentiment_analysis import sentimentAnalysis
from misc import WebSearch
from FilterParamsInference import PrologManager



def _inferPositivity(bot, prop):
    finalObj = ""
    for i in prop:
        if i.objct and not finalObj:
            finalObj = i.objct
            break
    for i in prop:
        if i.pnouns and not finalObj:
            finalObj = i.pnouns[0]
            break
    for i in prop:
        if i.nouns and not finalObj:
            finalObj = i.nouns[0]
            break

    unified = WebSearch.request(f"{finalObj} wikipedia").header
    if unified == "":
        unified = finalObj
    unified = PrologManager.formatText(unified)
    #bot likes or dislikes object
    if(unified in bot.likes):
        return 1
    if(unified in bot.dislikes):
        return -1

    #bot has relational likes or dislikes with object
    man = PrologManager.Manager(facts=PrologManager.default_facts,rules=PrologManager.default_rules)
    maxv = 0
    dislikes = False
    for x in bot.likes:
        res = man.consult(f"show_r({PrologManager.formatText(unified)},{PrologManager.formatText(x)},P)")
        if abs(res["P"]) > maxv:
            maxv = res["P"]

    for x in bot.dislikes:
        res = man.consult(f"show_r({PrologManager.formatText(unified)},{PrologManager.formatText(x)},P)")
        if abs(res["P"]) > maxv:
            maxv = res["P"]
            dislikes = True

    return (-1 ** int(dislikes))*maxv

def _inferKeywords(bot,prop,n = 50):
    ret = []
    #TODO
    return ret

def inferParams(bot, user):
    ret = utils.FilterParams()
    classifier = sentimentAnalysis.Classifier()
    prop = classifier.classify(user)

    ret.posFactor = _inferPositivity(bot,prop)
    ret.keywords = _inferKeywords(bot,prop)

    return ret
