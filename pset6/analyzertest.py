import nltk

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""
        self.positives = list()
        # open file path passed in
        with open(positives) as lines:
            # iterate through list
            for i in lines:
                # skip comments
                if str.startswith != ';':
                    # add to list and omit spaces
                    self.positives.append(str.strip("\n"))
        # repeat for negatives
        self.negatives = list()
        with open(negatives) as copy:
            for n in copy:
                if str.startswith != ';':
                    self.negatives.append(str.strip("\n"))
        


    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""
        tokenizer = nltk.tokenize.TweetTokenizer()
        tokens = tokenizer.tokenize(text)
        # pass tokenized text to variable
        #getting typeerror
        with open(self.positives) as lines:
            # set score
            score = 0
            #iterate over tokens(str.lower)
            for line in lines:
                if line == tokens(str.lower) 
                    score += 1
                for i in self.negatives:
                    if i == line(str.lower):
                        score -= 1
        # return overall score
        return (score)



