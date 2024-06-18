import os

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score

"""
language_code_dict = {
    "Python": "def function():",
    "Plain text": "hello bob"
}
df = pd.DataFrame(language_code_dict.items(), columns=["code", "language"])
"""


class CodeIdentifier:
    """
    This is a basic machine learning class that uses naive bayes to identify
    if the string given is either code or plain text.
    """

    def __init__(self, dataset: str = "code_identifier_dataset.csv"):
        # Load the dataset
        df = pd.read_csv(dataset)

        # Split the data into training and testing sets
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(df['code'], df['language'],
                                                                                test_size=0.2, random_state=42)

        # Convert the code snippets into a matrix of token counts
        self.vectorizer = CountVectorizer()
        x_train_counts = self.vectorizer.fit_transform(self.x_train)
        x_test_counts = self.vectorizer.transform(self.x_test)

        # Train a Naive Bayes classifier
        self.nb_classifier = MultinomialNB()
        self.nb_classifier.fit(x_train_counts, self.y_train)

        # Make predictions on the test data
        self.nb_predict_y = self.nb_classifier.predict(x_test_counts)

    def __predict_language(self, clf, vectorizer, code) -> str:

        if not code:
            return "Plain Text"
        # Preprocess the code
        code_counts = vectorizer.transform([code])

        # Make a prediction
        prediction = clf.predict(code_counts)

        return prediction[0]

    def accuracy(self) -> float:
        """
        Get the accuracy of the naive bayes model
        Returns: float, the accuracy of the classifier.
        """
        return accuracy_score(self.y_test, self.nb_predict_y)

    def identify(self, code: str) -> str:
        """
        Identify if the string given is either code or plain text.
        code: String.
        Returns: String, the identified language.
        """
        return self.__predict_language(self.nb_classifier, self.vectorizer, code)
