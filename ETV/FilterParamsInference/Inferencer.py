from misc import Bot
from misc import utils
from sentiment_analysis import sentimentAnalysis
from misc import WebSearch
from FilterParamsInference import PrologManager
from response_generation.abbreviations import abbr_list
from response_generation.abbreviations import enders_list
from response_generation.abbreviations import starters_list



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
        res = man.consult(f"show_r({PrologManager.formatText(unified)},{PrologManager.formatText(x)},P).")
        if abs(res["P"]) > maxv:
            maxv = res["P"]

    for x in bot.dislikes:
        res = man.consult(f"show_r({PrologManager.formatText(unified)},{PrologManager.formatText(x)},P).")
        if abs(res["P"]) > maxv:
            maxv = res["P"]
            dislikes = True

    return (-1 ** int(dislikes))*maxv

def _inferKeywords(bot,prop,n = 50):
    ret = []
    man = PrologManager.Manager()

    finalObj = []
    for i in prop:
        if i.objct:
            finalObj.append(i.objct)
    for i in prop:
        if i.pnouns and not finalObj:
            finalObj.append(i.pnouns[0])
    for i in prop:
        if i.nouns and not finalObj:
            finalObj.append(i.nouns[0])

    for word in finalObj:
        ret.append(word)
        for like in bot.likes:
            res = man.consult(f"show_r({utils.unifyWord(word)},{like},P).")
            if abs(res["P"]) > 0.7:
                ret.append(utils.unifyWord(like,format_out=False))
        for like in bot.dislikes:
            res = man.consult(f"show_r({utils.unifyWord(word)},{like},P).")
            if abs(res["P"]) > 0.7:
                ret.append(utils.unifyWord(like,format_out=False))

    return ret

def _inferSlang(bot, text):
    factor = 0
    slang_words = []
    text_list = text.lower().split()

    for abbr in abbr_list:
        shortened = abbr_list[abbr][0]
        if shortened.lower() not in slang_words:
            slang_words.append(shortened.lower())
    for ender in enders_list:
        if ender.lower() not in slang_words:
            slang_words.append(ender.lower())
    for starter in starters_list:
        if starter.lower() not in slang_words:
            slang_words.append(starter.lower())

    for word in slang_words:
        if word in text_list:
            factor += 2

    if factor > 10:
        factor = 10

    return factor

def inferParams(bot, user):
    ret = utils.FilterParams()
    classifier = sentimentAnalysis.Classifier()
    prop = classifier.classify(user)

    ret.posFactor = _inferPositivity(bot,prop)
    ret.keywords = _inferKeywords(bot,prop)
    ret.slangFactor = _inferSlang(bot, user)

    return ret
