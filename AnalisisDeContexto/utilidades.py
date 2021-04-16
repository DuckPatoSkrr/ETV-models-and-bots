import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
class DocProperties:
    def __init__(self):
        pnouns = []
        adjectives = []

    pnouns = []
    adjetives = []
    sentiment_polarity = 0
    sentiment_assessments = []
    sentiment_subjectivity = 0

    def classify(self, inText):
        nlp = spacy.load("en_core_web_sm")

        spacy_text_blob = SpacyTextBlob()
        doc = nlp(inText)
        spacy_text_blob = spacy_text_blob(doc)

        self.sentiment_polarity = spacy_text_blob._.sentiment.polarity
        self.sentiment_assessments = spacy_text_blob._.sentiment.assessments
        self.sentiment_subjectivity = spacy_text_blob._.sentiment.subjectivity

        for i in doc:
            if i.pos_ == "PROPN":
                self.pnouns.append(i)
            if i.pos_ == "ADJ":
                self.adjetives.append(i)

