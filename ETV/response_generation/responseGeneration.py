import random
import re

import gpt_2_simple as gpt2
from sentiment_analysis import sentimentAnalysis
from response_generation.abbreviations import abbr_list
from response_generation.abbreviations import enders_list
from response_generation.abbreviations import starters_list


def _maxPoints(list):
    max = list[0]
    for i in list:
        if i[1] > max[1]:
            max = i

    return max[0]


def _duple(input):  # transform a list of str to a list of duples [("text",0),...]
    output = []
    for i in input:
        output.append((i, 0))
    return output


def _pipePositivity(input, posFactor):
    if (posFactor is None):
        return input
    classifier = sentimentAnalysis.Classifier()
    outList = []
    for duple in input:
        prop = classifier.classify(duple[0])
        res = 0
        for i in prop:
            res += 10 - (abs(posFactor - i.sentiment_polarity) * 5)
        res /= len(prop)
        outList.append((duple[0], duple[1] + res))

    return outList


# formats text making it more informal the higher the slang factor is (factor must be between 0 and 10)
# changes done include: abbreviating expressions, adding emotes, more or less capital letters or copying/removing punctuation marks
def _pipeSlang(input, slangFactor):
    if (slangFactor is None):
        return input

    # make sure slang factor stays between 0 and 10
    slangFactor = min(10, max(0, slangFactor))

    outList = []
    startWordChance = slangFactor * 3  # max chance of 30% at factor 10
    endWordChance = slangFactor * 6  # max chance of 60% at factor 10

    enders_total = 0
    for ender in enders_list:
        enders_total += enders_list[ender]

    starters_total = 0
    for starter in starters_list:
        starters_total += starters_list[starter]

    for duple in input:
        text = duple[0]

        if len(text) <= 1:
            outList.append((text, duple[1]))
            continue

        # Try to add
        if random.randint(0, 99) < startWordChance:  # Start
            # Extra chance for more slang if word is added
            slangFactor = min(10, slangFactor + 1)
            word_index = random.randint(1, starters_total)
            for starter in starters_list:
                word_index -= starters_list[starter]
                if word_index <= 0:
                    if len(text) > 2:
                        if not text[1].isupper():
                            text = text[0].lower() + text[1:]
                    text = starter + " " + text
                    break

        if random.randint(0, 99) < endWordChance:  # end
            # Extra chance for more slang if word is added
            slangFactor = min(10, slangFactor + 1)
            word_index = random.randint(1, enders_total)
            for ender in enders_list:
                word_index -= enders_list[ender]
                if word_index <= 0:
                    if len(text) > 0:
                        last = len(text) - 1
                        if text[last] == '.':
                            text = text[0:last]
                    text = text + " " + ender
                    break

        # Try to replace
        for abbr in abbr_list:
            replaceChance = slangFactor * abbr_list[abbr][1]
            if random.randint(0, 99) < replaceChance:
                text = text.replace(f" {abbr} ", f" {abbr_list[abbr][0]} ")

        # Remove symbols
        symbol_chance = slangFactor * 6  # max chance of 60% at factor 10
        dotless_chance = slangFactor * 2 # max chance of 20% at factor 10
        # Remove dots
        if random.randint(0, 99) < dotless_chance:
            slangFactor = min(10, slangFactor + 2)
            text = text.replace(".", "")
        elif random.randint(0, 49) < symbol_chance:
            if len(text) > 0:
                last = len(text) - 1
                if text[last] == '.':
                    text = text[0:last]
        # Remove apostrophe
        if random.randint(0, 99) < symbol_chance:
            slangFactor = min(10, slangFactor + 1)
            text = text.replace("\'", "")
        # Remove commas
        if random.randint(0, 99) < symbol_chance:
            slangFactor = min(10, slangFactor + 1)
            text = text.replace(",", "")

        # Capital letters? Hell no
        lowercase_chance = slangFactor * 8  # max chance of 80% at factor 10
        if random.randint(0, 99) < lowercase_chance:
            text = text.lower()

        # Let's add some typos too
        typo_chance = slangFactor - 5
        if len(text) > 2:
            swapped = False
            for i in range(1, len(text) - 1):
                if swapped:
                    swapped = False
                    continue
                if random.randint(0, 499) < typo_chance:
                    if text[i].isalpha() and text[i+1].isalpha():
                        text = text[:i] + text[i+1].lower() + text[i].lower() + text[i+2:]
                        swapped = True

        outList.append((text, duple[1]))

    return outList


def _pipeFormat(input, nchars):  # format text, this doesn't change the puntuation
    if (nchars == -1):
        return input
    outList = []
    for duple in input:
        output = ""
        splitedInput = re.split(';|,|\.|:|\?|!',duple[0])
        i = 0
        while (len(output) + len(splitedInput[i]) < nchars and i < len(splitedInput)):
            output += splitedInput[i] + "."
            i += 1

        output = output.replace("\n\n", " ")
        if not output:
            outList.append((output, -1000))
        else:
            outList.append((output, duple[1]))

    return outList


def _pipeKeywords(input,
                  keywords):  # gives points for each keyword that appears. Amount of each keyword does NOT matter, better for short texts
    if len(keywords) == 0:
        return input

    outList = []
    for duple in input:
        appearances = 0
        for word in keywords:
            if duple[0].find(word) > -1:
                appearances += 1
        score = (appearances * 10) / len(keywords)
        outList.append((duple[0], duple[1] + score))
    return outList


def _pipeKeywordCount(input,
                      keywords):  # gives points the more times keywords appear. Repeated keywords also add points. Can be useful for long texts
    if len(keywords) == 0:
        return input

    outList = []
    auxList = []
    maxScore = 0
    for duple in input:
        appearances = 0
        text_array = duple[0].split()
        for word in keywords:
            appearances += text_array.count(word)
        if appearances > maxScore:
            maxScore = appearances
        auxList.append((duple[0], duple[1], appearances))
    for aux in auxList:
        score = 0
        if maxScore > 0:
            score = (aux[2] * 10) / maxScore
        outList.append((aux[0], aux[1] + score))
    return outList


def _processedText(input, nchars, positivityFactor, keywords, slangFactor):  # filters the output of the model
    output = _duple(input)
    output = _pipeFormat(output, nchars)
    output = _pipePositivity(output, positivityFactor)
    output = _pipeSlang(output, slangFactor)
    output = _pipeKeywords(output, keywords)
    return _maxPoints(output)


def generateResponse(model,
                     posFactor,
                     keyWords,
                     nchars,
                     number_of_responses,
                     slangFactor,
                     prefix=None):
    sess = gpt2.start_tf_sess()
    gpt2.load_gpt2(sess, run_name=model.name)

    i = 0
    textGenerated = []
    while i < number_of_responses:
        nor = number_of_responses % 15
        if(not nor):
            nor = 15

        textGenerated += gpt2.generate(sess, prefix=prefix, run_name=model.name,
                                  nsamples=nor, batch_size=nor,
                                  return_as_list=True, length=nchars)
        i += nor
    return _processedText(textGenerated, nchars, posFactor, keyWords, slangFactor)
