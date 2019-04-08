from sklearn.neural_network import MLPClassifier

from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix
import numpy as np

from sklearn.model_selection import train_test_split
from sys import path
path.append("./models/")

from numpy import genfromtxt

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.metrics import precision_recall_fscore_support
from sklearn.metrics import confusion_matrix

import numpy as np

class mlp:



    @staticmethod
    def load_data(datasets):
        """
        This helper function loads the dataset saved in the CSV file
        and returns 4 numpy arrays containing the training set inputs
        and labels, and the testing set inputs and labels.
        """

        # Load the training data from the CSV file
        # global training_data
        training_data = np.genfromtxt("dataset.txt", delimiter=',', dtype=np.int32)
        #input_data = np.genfromtxt('input.txt', delimiter=',', dtype=np.int32)

        """
        Each row of the CSV file contains the features collected on a website
        as well as whether that website was used for phishing or not.
        We now separate the inputs (features collected on each website)
        from the output labels (whether the website is used for phishing).
        """

        # Extract the inputs from the training data array (all columns but the last one)
        inputs = training_data[:, :-1]

        # Extract the outputs from the training data array (last column)
        outputs = training_data[:, -1]

        # Separate the training (first 2,000 websites) and testing data (last 456)

        training_inputs, testing_inputs, training_outputs, testing_outputs = train_test_split(inputs, outputs, test_size=0.10, random_state=42)

        classifier = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(5, 2), random_state=1)
        classifier.fit(training_inputs, training_outputs)

        # Return the four arrays
        #return training_inputs, training_outputs, testing_inputs, testing_outputs , input_data
        return classifier.predict([datasets])

if __name__ == '__main__':
    print("APT: Training a decision tree to detect phishing websites")

    None