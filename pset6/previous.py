import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # create list object
        self.positives = set()
        # open file path passed in
        with open(positives) as lines:
            # iterate through list
            for i in lines:
                # skip comments
                if str(i).startswith(';') != True:
                    # add to list and omit spaces
                    self.positives.add(str(i).strip())

        # repeat for negatives
        self.negatives = set()
        with open(negatives) as lines:
            for n in lines:
                if str(n).startswith(';') != True:
                    self.negatives.add(str(n).strip())


    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        # pass tokenized text to variable
        score = 0
        for n in tokens:
            if str.lower(n) in self.positives:
                score += 1
        for i in tokens:
            if str.lower(i) in self.negatives:
                score -= 1
        # return overall score
        return (score)
