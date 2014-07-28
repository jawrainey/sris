class Sentiment:
    """
    Used to determine the sentiment (positive/negative) for a given message.
    """
    def determine_sentiment(self, message):
        """
        Determines the sentiment (positive or negative) of a given message.

        Note: this is extremely slow as TextBlob lazily loads the
        NLTK movie review corpus for training. To understand how it works visit:
        https://github.com/sloria/TextBlob/blob/master/textblob/en/sentiments.py

        TODO:
          - Use a NaiveBayesClassifier to load the movie review data once
          - Use the labelled messages to improve the classifier.
          - Add a more intelligent 'feature extractor' for better accuracy
            (currently uses a simple bag of words model).
          - To further improve the accuracy of the NBA I need to train
            it with a large labelled corpora -- ideally Twitter data.

        Args:
            message (str): the patients message to determine the sentiment from.

        Returns:
            str: 'pos' or 'neg' as determined by the classifier.
        """
        from textblob import TextBlob
        from textblob.sentiments import NaiveBayesAnalyzer
        blob = TextBlob(message, analyzer=NaiveBayesAnalyzer())
        return blob.sentiment.classification
