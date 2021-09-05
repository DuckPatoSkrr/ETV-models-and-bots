from misc.utils import unifyWord
from sentiment_analysis import sentimentAnalysis
from collections import defaultdict
import re


# takes the text and obtains a dictionary
# where keys are pairs of words and values are how positively related they are
# then turns that dictionary into prolog facts
def generateFacts(corpus_file):
    final_dict = {}
    pairs_dict = defaultdict(list)
    load_chunk = lambda f: ' '.join(f.readlines(1024))

    with open(corpus_file, "r") as file:
        chunk = load_chunk(file)
        while chunk:
            text = chunk.lower()
            for sentence in re.split(';|,|\.|:', text):
                pairs_dict = checkSentence(pairs_dict, sentence)
            chunk = load_chunk(file)

    for pair in pairs_dict:
        if len(pairs_dict[pair]) > 0:
            final_dict[pair] = sum(pairs_dict[pair]) / len(pairs_dict[pair])

    dictToFacts(final_dict)


# the input will be a defaultdic dictionary where the keys are the two words related
# and the values are lists of the positivity values when they both appear
def checkSentence(pairs_dict, sentence):
    if sentence is None:
        return pairs_dict
    classifier = sentimentAnalysis.Classifier()
    res = classifier.classify(sentence)
    pnouns = []
    for prop in res:
        pnouns.extend(prop.pnouns)
    pamount = len(pnouns)
    if pamount > 1:
        for i in range(pamount):
            pnouns[i] = unifyWord(pnouns[i])
        for i in range(pamount):
            for j in range(i + 1, pamount):
                pairs_dict[(pnouns[i], pnouns[j])].append(res.sentiment_polarity)
    return pairs_dict


# turns a dictionary of relations into prolog facts
def dictToFacts(text_dict):
    dict_aux = {}
    delete_lines = []
    default_facts = r"./FilterParamsInference/facts.pl"

    # first we read the facts file and get a list of the lines
    r_file = open(default_facts, "r")
    lines = r_file.readlines()
    r_file.close()

    # now we delete the lines with term relationship rules
    # and store them in our aux dictionary
    for i in range(0, len(lines)):
        if lines[i].startswith("relacionTerm"):
            line_list = lines[i].split("\"");
            value_aux = line_list[4][1:].split(")");
            dict_aux[(line_list[1], line_list[3])] = float(value_aux[0])
            delete_lines.append(i)

    # we make sure to delete the lines after looping through them to not mess with the loop
    for i in range(0, len(delete_lines)):
        del lines[i]

    # now we combine this aux dictionary with the obtained from the text
    # if the same key exists in both, we keep the newer ones, so the ones from text_dict
    for pair in text_dict:
        dict_aux[pair] = text_dict[pair]

    # we have our final values in dict_aux, time to add them to facts.pl
    w_file = open(default_facts, "w+")

    # first, we add the old lines that we did not delete back
    for line in lines:
        w_file.write(line)

    # now we add the new rules
    for pair in dict_aux:
        text_line = "relacion(\"{0}\",\"{1}\",{2}).".format(pair[0], pair[1], dict_aux[pair])
        w_file.write(text_line)

    w_file.close()
