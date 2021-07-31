from misc import Bot
from misc import utils
from sentiment_analysis import sentimentAnalysis
from misc import WebSearch
import PrologManager

facts = "facts.pl"
rules = "rules.pl"

def _inferPositivity(bot, prop):
    unified = WebSearch.request(f"{prop.objct} wikipedia").header
    #bot likes or dislikes object
    if(unified in bot.likes):
        return 1
    if(unified in bot.dislikes):
        return -1

    #bot has relational likes or dislikes with object
    man = PrologManager.Manager(facts=facts,rules=rules)
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

def inferParams(bot, user):
    ret = utils.FilterParams()
    classifier = sentimentAnalysis.Classifier()
    prop = classifier.classify(user)

    ret.posFactor = _inferPositivity(bot,prop)
    #ret.keywords = _inferKeywords(bot,prop) #TODO



