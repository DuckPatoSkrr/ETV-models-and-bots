from ETV.sentiment_analysis import sentimentAnalysis
from collections import defaultdict


# takes the text already turned into sentences and obtains a dictionary
# where keys are pairs of words and values are how positively related they are
def checkText(sentences):
    final_dict = {}
    pairs_dict = defaultdict(list)
    for sent in sentences:
        pairs_dict = checkSentence(pairs_dict, sent)
    for pair in pairs_dict:
        if len(pairs_dict[pair]) > 0:
            final_dict[pair] = sum(pairs_dict[pair]) / len(pairs_dict[pair])
    return final_dict


# the input will be a defaultdic dictionary where the keys are the two words related
# and the values are lists of the positivity values when they both appear
def checkSentence(pairs_dict, sentence):
    if sentence is None:
        return pairs_dict
    classifier = sentimentAnalysis.Classifier()
    res = classifier.classify(sentence)
    pamount = len(res.pnouns)
    if pamount > 1:
        for i in range(pamount):
            for j in range(i + 1, pamount):
                pairs_dict[(res.pnouns[i], res.pnouns[j])].append(res.sentiment_polarity)
    return pairs_dict
