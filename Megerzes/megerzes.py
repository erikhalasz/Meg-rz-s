import pandas as pd
from collections import Counter
from re import findall

# Define a class for sentiment analysis
class SentiMentalDictionary():
    def __init__(self, text):
        # Split the input text into words, convert to uppercase, and find all occurrences of the pattern '[A-Z]+'
        self.text = findall('[A-Z]+', text.upper())  
        # Initialize sets for different types of words
        self.sentiments = {'Negative': set(), 'Positive': set(), 'Uncertainty': set(), 'Litigious': set(), 'Strong_Modal': set(), 'Weak_Modal': set(), 'Constraining': set()}
        self.load_data()  # Load the data when the class is instantiated

    # Method to load data from a CSV file and populate the word sets
    def load_data(self):
        df = pd.read_csv('words.csv', index_col=0)  # Load data from CSV
        # Populate word sets based on CSV data
        for word in df.index:
            for sentiment in self.sentiments:
                if df[sentiment][word] == 1:
                    self.sentiments[sentiment].add(word)

    # Method to analyze the sentiment of the text
    def get_sentiment(self):
        word_counts = Counter(self.text)  # Count the occurrence of each word in the text
        # Count positive and negative words
        positive = sum(word_counts[word] for word in self.sentiments['Positive'] | self.sentiments['Strong_Modal'] if word in word_counts)
        negative = sum(word_counts[word] for word in self.sentiments['Negative'] | self.sentiments['Uncertainty'] | self.sentiments['Litigious'] | self.sentiments['Weak_Modal'] | self.sentiments['Constraining'] if word in word_counts)
        # Determine the overall sentiment based on the counts of positive and negative words
        if (positive - negative) > 0:
            return "Positive"
        elif (positive - negative) < 0:
            return "Negative"
        else:
            return None  # Return None if the counts are equal

# Example usage of the class
example1 = SentiMentalDictionary("This is a positive example")
print(example1.get_sentiment())  # Print the sentiment of the example text