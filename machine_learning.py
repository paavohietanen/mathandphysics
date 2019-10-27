from mathematical_objects import Matrix
from math import exp, log

'''
Credit: Thomas Countz, https://medium.com/@thomascountz/19-line-line-by-line-python-perceptron-b6f113b161f3
(numpy replaced with self-made library)
'''


class Perceptron_edited(object):

    def __init__(self, no_of_inputs, threshold=100, learning_rate=1):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.weights = Matrix([], 1, no_of_inputs).transpose()
        self.misclassifications = []
        self.outputs = []

    def predict(self, inputs):
        summation = (inputs.transpose() * self.weights)
        if summation[0][0] >= 0:
            activation = 1
        else:
            activation = -1
        return activation

    def train(self, training_inputs, labels):
        for _ in range(self.threshold):
            self.misclassifications = []
            self.outputs = []
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                print(_, ": PREDICTION IS", prediction, "WITH INPUTS", "["+str(inputs[0])+","+str(inputs[1])+"]", "CLASSIFIED AS", label[0] - prediction == 0)
                self.weights += self.learning_rate * ((label[0] - prediction)/2) * inputs
                if prediction != label[0]:
                    self.misclassifications.append(1)
                    print("FALSE")
                else:
                    self.misclassifications.append(0)
                self.outputs.append(prediction)
            print(_, ": WEIGHTS ARE", "["+str(self.weights[0])+","+str(self.weights[1])+"]")

import numpy as np


class Perceptron(object):

    def __init__(self, no_of_inputs, threshold=100, learning_rate=1):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.weights = np.zeros(no_of_inputs)

    def predict(self, inputs):
        summation = np.dot(inputs, self.weights)
        if summation >= 0:
            activation = 1
        else:
            activation = -1
        return activation

    def train(self, training_inputs, labels):
        for _ in range(self.threshold):
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                print(_, ": PREDICTION IS", prediction, "WITH INPUTS", inputs, "CLASSIFIED AS", label - prediction == 0)
                self.weights += self.learning_rate * ((label - prediction)/2) * inputs
                print(_, ": WEIGHTS ARE", self.weights)


class PerceptronBiased(object):

    def __init__(self, no_of_inputs, threshold=100, learning_rate=1):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.weights = np.zeros(no_of_inputs + 1)

    def predict(self, inputs):
        summation = np.dot(inputs, self.weights[1:]) + self.weights[0]
        if summation >= 0:
            activation = 1
        else:
            activation = -1
        return activation

    def train(self, training_inputs, labels):
        for _ in range(self.threshold):
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                print(_, ": PREDICTION IS", prediction, "WITH INPUTS", inputs, "CLASSIFIED AS", label-prediction == 0)
                self.weights[1:] += self.learning_rate * (label - prediction)/2 * inputs
                self.weights[0] += self.learning_rate * (label - prediction)/2
                print(_, ": WEIGHTS ARE", self.weights)


class PerceptronBiasedEdited(object):

    def __init__(self, no_of_inputs, threshold=100, learning_rate=1):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.weights = Matrix([], 1, no_of_inputs + 1).transpose()
        self.misclassifications = []
        self.outputs = []

    def predict(self, inputs):
        summation = (inputs.transpose() * Matrix(self.weights[1:])) + Matrix([[self.weights[0][0]]])
        if summation[0][0] >= 0:
            activation = 1
        else:
            activation = -1
        return activation

    def train(self, training_inputs, labels):
        for _ in range(0, self.threshold):
            self.misclassifications = []
            self.outputs = []
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                #print(_, ": PREDICTION IS", prediction, "WITH INPUTS", "["+str(inputs[0])+","+str(inputs[1])+"]", "CLASSIFIED AS", label[0] - prediction == 0)
                #print("ASSIGNING", inputs[0][0], "ON", self.weights[2][0])
                self.weights[0][0] += self.learning_rate * (label[0] - prediction) / 2
                self.weights[1][0] += self.learning_rate * ((label[0] - prediction)/2) * inputs[0][0]
                self.weights[2][0] += self.learning_rate * ((label[0] - prediction) / 2) * inputs[1][0]
                self.weights[3][0] += self.learning_rate * ((label[0] - prediction) / 2) * inputs[2][0]
                if prediction != label[0]:
                    self.misclassifications.append(1)
                else:
                    self.misclassifications.append(0)
                self.outputs.append(prediction)

class LogRegression(object):

    def __init__(self, no_of_inputs, threshold=1000, learning_rate=0.01):
        self.threshold = threshold
        self.learning_rate = learning_rate
        self.weights = np.zeros(no_of_inputs)

    def predict(self, inputs):
        fii = 1/(1+ exp(np.dot(inputs, self.weights)) )
        if fii >= 0.8:
            activation = 1
        else:
            activation = -1
        return activation

    def train(self, training_inputs, labels):
        for _ in range(self.threshold):
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                print(_, ": PREDICTION IS", prediction, "WITH INPUTS", inputs, "CLASSIFIED AS", label-prediction == 0)
                self.weights += self.learning_rate * ((label - prediction)/2) * inputs
            print(_, ": WEIGHTS ARE", self.weights)


class GradientDescentSSVMNumpy(object):

    def __init__(self, no_of_inputs, threshold=100, balancing_para=1, step_size=0.1):
        self.threshold = threshold
        self.balancing_para = balancing_para
        self.step_size = step_size
        self.weights = np.zeros(no_of_inputs)

    def predict(self, inputs):
        summation = np.dot(inputs, self.weights)
        if summation >= 0:
            activation = 1
        else:
            activation = -1
        return activation

    def train(self, training_inputs, labels):
        for _ in range(self.threshold):
            for inputs, label in zip(training_inputs, labels):
                prediction = self.predict(inputs)
                print(_, ": PREDICTION IS", prediction, "WITH INPUTS", inputs, "CLASSIFIED AS", label - prediction == 0)
                self.weights += self.learning_rate * ((label - prediction)/2) * inputs
                print(_, ": WEIGHTS ARE", self.weights)


class GradientDescentSSVM(object):

    def __init__(self, no_of_inputs, threshold=100, balancing_para=1, step_size=0.1):
        self.threshold = threshold
        self.balancing_para = balancing_para
        self.step_size = step_size
        self.weights = Matrix([], 1, no_of_inputs).transpose()

    def predict(self, inputs):
        summation = self.weights.transpose()* inputs
        print("Step 2.: Calculating w^Tx:", summation)
        if summation[0][0] >= 0:
            activation = 1
        else:
            activation = -1
        return activation

    def compute_updating_direction(self, inputs, y):
        g = y * self.weights.transpose() * inputs
        print("Step 4.: yw^Tx is", g,", therefore...\n")
        if g[0][0] < 1:
            direction = -y * inputs + self.balancing_para*self.weights
        else:
            direction = self.balancing_para*self.weights
        print("Step 5.: ...direction is\n", direction)
        return direction

    def train(self, training_inputs, labels):
        for _ in range(self.threshold):
            print("Step 0.: Iterating through training data")
            for inputs, label in zip(training_inputs, labels):
                print("Step 1.: Training with a datapoint\n", inputs)
                prediction = self.predict(inputs) # measuring w^Tx
                if label[0] == prediction: # In gradient descent we also apply weights when correct classification
                    y = label[0]
                else:
                    y = -1 * label[0]
                print("Step 3.: Did we misclassify? Sign of y is", y, "\n")
                direction = self.compute_updating_direction(inputs, y)
                self.weights -= self.step_size * direction
                print("Step 6.: AND the new W is:\n", self.weights, "\n************")


class AdaBoost(object):

        def __init__(self, no_of_inputs, no_of_learners, no_of_examples, threshold=100):
            self.no_of_inputs = no_of_inputs
            self.no_of_learners = no_of_learners
            self.no_of_iterations = no_of_examples
            self.weights = Matrix([[1]*no_of_examples]).transpose() / no_of_examples
            self.base_learners = [PerceptronBiasedEdited(no_of_inputs, threshold=threshold)] * no_of_learners

        def calculate_weighted_error(self, misclassifications):
            numerator = 0
            denominator = 0
            print("THERE ARE", misclassifications.count(1), "MISCLASSIFICATIONS")
            for i in range(0, self.weights.m):
                numerator += self.weights[i][0]*misclassifications[i]
                denominator += self.weights[i][0]
            return numerator / denominator

        def calculate_normalization_factor(self, alpha, misclassifications, max_misclass):
            sum = 0
            for i in range(0, self.no_of_inputs):
                sum += self.weights[i][0] + exp(-alpha*misclassifications[i])

            return sum

        def pick_example(self, misclassifications):
            maximum = 0
            index = 0
            for i in range(0, self.no_of_inputs):
                if misclassifications[i] == 1:
                    if self.weights[i][0] > maximum:
                        index = i
            return index

        def train(self, training_inputs, labels):
            for t in range(self.no_of_learners):
                self.base_learners[t].train(training_inputs, labels)
                misclassifications = self.base_learners[t].misclassifications
                epsilon = self.calculate_weighted_error(misclassifications)
                max_misclass = self.pick_example(misclassifications)
                print("EPSILON IS ", epsilon)
                if epsilon > 0.5:
                    break
                alpha = 0.5*log( (1-epsilon) / epsilon)
                print("ALPHA IS", alpha)
                #for i in range(0, len(training_inputs)):
                z = self.calculate_normalization_factor(alpha, misclassifications, max_misclass)
                self.weights[max_misclass][0] = (self.weights[max_misclass][0]* exp(-alpha*misclassifications[max_misclass]))/z
                print("WEIGHTS ARE", self.weights)





'''training_inputs = []
training_inputs.append(np.array([0.8, 0.1]))
training_inputs.append(np.array([0.7, 0.2]))
training_inputs.append(np.array([0.9, 0.3]))
training_inputs.append(np.array([0.3, 0.8]))
training_inputs.append(np.array([0.1, 0.7]))
training_inputs.append(np.array([0.1, 0.9]))
#training_inputs.append(np.array([0.4, 0.4]))

labels = np.array([-1,-1,-1,1,1,1])

perceptron = Perceptron(2)
perceptron.train(training_inputs, labels)

#####

training_inputs = []
training_inputs.append(np.array([0.8, 0.1]))
training_inputs.append(np.array([0.7, 0.2]))
training_inputs.append(np.array([0.9, 0.3]))
training_inputs.append(np.array([0.3, 0.8]))
training_inputs.append(np.array([0.1, 0.7]))
training_inputs.append(np.array([0.1, 0.9]))
training_inputs.append(np.array([0.4, 0.4]))

labels = np.array([-1,-1,-1,1,1,1,-1])

perceptron = Perceptron_biased(2)
perceptron.train(training_inputs, labels)

#####

logistic = LogRegression(2)
logistic.train(training_inputs, labels)

#####

training_inputs = []
training_inputs.append(Matrix([[0.8], [0.1]]))
training_inputs.append(Matrix([[0.7], [0.2]]))
training_inputs.append(Matrix([[0.9], [0.3]]))
training_inputs.append(Matrix([[0.3], [0.8]]))
training_inputs.append(Matrix([[0.1], [0.7]]))
training_inputs.append(Matrix([[0.1], [0.9]]))

labels = Matrix([[-1],[-1],[-1],[1],[1],[1]])

perceptron = Perceptron_edited(2)
perceptron.train(training_inputs, labels)'''

'''training_inputs = []
training_inputs.append(Matrix([[0], [1]]))
training_inputs.append(Matrix([[2], [1]]))
training_inputs.append(Matrix([[2], [-1]]))
training_inputs.append(Matrix([[0], [-1]]))
training_inputs.append(Matrix([[-2], [-1]]))
training_inputs.append(Matrix([[-2], [1]]))

labels = Matrix([[1],[1],[1],[-1],[-1],[-1]])

svm = GradientDescentSSVM(2, threshold=1)
svm.train(training_inputs, labels)'''
training_inputs = []
labels = []
x1 = [.1,.2,.4,.8, .8, .05,.08,.12,.33,.55,.66,.77,.88,.2,.3,.4,.5,.6,.25,.3,.5,.7,.6]
x2 = [.2,.65,.7,.6, .3,.1,.4,.66,.77,.65,.68,.55,.44,.1,.3,.4,.3,.15,.15,.5,.55,.2,.4]
labels_raw =[1,1,1,1,1,1,1,1,1,1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

for i in range(0, len(x1)):
    training_inputs.append(Matrix([[x1[i]], [x2[i]], [1]]))
    print(training_inputs[i])
    labels.append([labels_raw[i]])
print(training_inputs)
#ada = AdaBoost(3, 4, len(training_inputs), threshold=201)
#ada.train(training_inputs, labels)

