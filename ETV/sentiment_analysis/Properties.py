
class Properties:
    pnouns = []
    adjectives = []
    sentiment_polarity = 0
    sentiment_assessments = []
    sentiment_subjectivity = 0

    def __init__(self, sentiment_polarity, sentiment_assessments, sentiment_subjectivity, pnouns, adjectives):
        self.sentiment_polarity = sentiment_polarity
        self.sentiment_assessments = sentiment_assessments
        self.sentiment_subjectivity = sentiment_subjectivity
        self.pnouns = pnouns
        self.adjectives = adjectives


