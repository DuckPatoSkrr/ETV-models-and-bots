import spacy
from spacytextblob import spacytextblob
from sentiment_analysis import Properties
import re


class Classifier:
    nlp = None
    spacy_text_blob = None

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("spacytextblob")



    def classify(self, inText):
        ret =[]
        for sentence in re.split(';|,|\.|:', inText):
            doc = self.nlp(sentence)
            sentiment_polarity = doc._.polarity
            sentiment_assessments = doc._.assessments
            sentiment_subjectivity = doc._.subjectivity
            verbs = []
            pnouns = []
            adjectives = []
            subject = ""
            objct = ""
            for i in doc:
                if i.pos_ == "PROPN":
                    pnouns.append(str(i))
                if i.pos_ == "ADJ":
                    adjectives.append(str(i))
                if i.pos_ == "VERB":
                    verbs.append(str(i))
                if i.dep_ == "nsubj":
                    subject = str(i)
                if i.dep_ == "dobj":
                    objct = str(i)

            compobj = ""
            hasCompound = False
            for i in doc:
                if i.dep_ == "compound" and str(i.head) == objct:
                    hasCompound =True
                    compobj = f"{compobj} {str(i)}"

            if hasCompound:
                objct = f"{compobj} {objct}"

            prop = Properties.Properties(sentiment_polarity, sentiment_assessments, sentiment_subjectivity, pnouns, adjectives,verbs,subject,objct)

            i = 0
            while(i < len(ret) and abs(ret[i].sentiment_polarity) > abs(prop.sentiment_polarity)):
                i+=1
            ret.insert(i,prop)

        return ret

