
class Properties:
    pnouns = []
    adjectives = []
    verbs=[]
    sentiment_polarity = 0
    sentiment_assessments = []
    sentiment_subjectivity = 0
    subject = None
    objct = None

    def __init__(self, sentiment_polarity, sentiment_assessments, sentiment_subjectivity, pnouns, adjectives,verbs,subject, objct):
        self.sentiment_polarity = sentiment_polarity
        self.sentiment_assessments = sentiment_assessments
        self.sentiment_subjectivity = sentiment_subjectivity
        self.pnouns = pnouns
        self.adjectives = adjectives
        self.verbs = verbs
        self.subject = subject
        self.objct = objct


