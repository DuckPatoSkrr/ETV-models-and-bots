import spacy
import Properties


class Classifier:
    nlp = None
    spacy_text_blob = None

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.nlp.add_pipe("spacytextblob")



    def classify(self, inText):

        doc = self.nlp(inText)
        sentiment_polarity = doc._.polarity
        sentiment_assessments = doc._.assessments
        sentiment_subjectivity = doc._.subjectivity
        pnouns = []
        adjectives = []
        for i in doc:
            if i.pos_ == "PROPN":
                pnouns.append(str(i))
            if i.pos_ == "ADJ":
                adjectives.append(str(i))

        return Properties.Properties(sentiment_polarity, sentiment_assessments, sentiment_subjectivity, pnouns, adjectives)

