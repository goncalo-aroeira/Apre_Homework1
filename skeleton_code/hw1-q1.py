#!/usr/bin/env python

# Deep Learning Homework 1

import argparse

import numpy as np
import matplotlib.pyplot as plt

import utils


class LinearModel(object):
    def __init__(self, n_classes, n_features, **kwargs):
        self.W = np.zeros((n_classes, n_features))

    def update_weight(self, x_i, y_i, **kwargs):
        raise NotImplementedError

    def train_epoch(self, X, y, **kwargs):
        for x_i, y_i in zip(X, y):
            self.update_weight(x_i, y_i, **kwargs)

    def predict(self, X):
        """X (n_examples x n_features)"""
        scores = np.dot(self.W, X.T)  # (n_classes x n_examples)
        predicted_labels = scores.argmax(axis=0)  # (n_examples)
        return predicted_labels

    def evaluate(self, X, y):
        """
        X (n_examples x n_features):
        y (n_examples): gold labels
        """
        y_hat = self.predict(X)
        n_correct = (y == y_hat).sum()
        n_possible = y.shape[0]
        return n_correct / n_possible


class Perceptron(LinearModel):    
    def update_weight(self, x_i, y_i, **kwargs):
        """
        x_i (n_features): a single training example
        y_i (scalar): the gold label for that example
        other arguments are ignored
        """        
        y_hat = self.predict(x_i)
        # TODO nao atualiza!!!
        ## if y_hat!= 0:
        # #   print("self w",self.W, "y_i", y_i, "y_hat", y_hat)
        if y_hat != y_i:
            # self.W += y_i * x_i
            # multi class
            self.W[y_i, :] += x_i
            self.W[y_hat, :] -= x_i


class LogisticRegression(LinearModel):
    def update_weight(self, x_i, y_i, learning_rate=0.001):
        """
        x_i (n_features): a single training example
        y_i: the gold label for that example
        learning_rate (float): keep it at the default value for your plots
        """
        # Q1.1b
        
        # Get probability scores according to the model (num_labels x 1).
        label_scores = np.expand_dims(self.W.dot(x_i), axis = 1)

        # One-hot encode true label (num_labels x 1).
        y_one_hot = np.zeros((np.size(self.W, 0),1))
        y_one_hot[y_i] = 1

        # Softmax function
        # This gives the label probabilities according to the model (num_labels x 1).
        label_probabilities = np.exp(label_scores) / np.sum(np.exp(label_scores))
        
        # SGD update. W is num_labels x num_features.
        self.W = self.W + learning_rate * (y_one_hot - label_probabilities).dot(np.expand_dims(x_i, axis = 1).T)
        
        
        
class MLP(object):
    # Q3.2b. This MLP skeleton code allows the MLP to be used in place of the
    # linear models with no changes to the training loop or evaluation code
    # in main().
    def __init__(self, n_classes, n_features, hidden_size):
        # Initialize an MLP with a single hidden layer.
        # n_classes: number of output classes
        # n_features: number of input features
        # hidden_size: number of hidden units
        
        # Initialize weights with normal distribution
        # Initialize weights with normal distribution
        W1 = np.random.normal(loc=0.1, scale=0.1, size=(hidden_size, n_features))
        W2 = np.random.normal(loc=0.1, scale=0.1, size=(n_classes, hidden_size))
        
        self.weights = [W1, W2]

        # Initialize biases with zero vectors
        b1 = np.zeros(hidden_size)
        b2 = np.zeros(n_classes)
        
        self.biases = [b1, b2]
        
        self.hidden_size = hidden_size
        self.n_classes = n_classes
        self.n_features = n_features


          
        
    def backward(self, x, y, output, hiddens):
        num_layers = len(self.weights)
        g = self.relu
        z = output

        grad_z = output - y  
        
        grad_weights = []
        grad_biases = []
        
        # Backpropagate gradient computations 
        for i in range(num_layers-1, -1, -1):
            # change activation function gradient -> 1rst back : cross entropy, 2nd back, relu
            
            # Gradient of hidden parameters.
            h = x if i == 0 else hiddens[i-1]
            grad_weights.append(grad_z[:, None].dot(h[:, None].T))
            grad_biases.append(grad_z)
            
            # Gradient of hidden layer below.
            grad_h = self.weights[i].T.dot(grad_z)

            # Gradient of hidden layer below before activation.
            
            grad_z = grad_h * self.reluDerivative(h)
            
        # Making gradient vectors have the correct order
        grad_weights.reverse()
        grad_biases.reverse()
        
        return grad_weights, grad_biases

    def relu(self, x):
        return np.maximum(0, x)
        
    def reluDerivative(self, x):
        x[x<=0] = 0
        x[x>0] = 1
        return x

    def softmax(self, x):
        exp_x = np.exp(x - np.max(x))
        return exp_x / np.sum(exp_x)
        
    def forward(self, x):
        num_layers = len(self.weights)
        hiddens = []
        #print("x", x)
        # compute hidden layers
        for i in range(num_layers):
            h = x if i == 0 else hiddens[i-1]
            z = self.weights[i].dot(h) + self.biases[i]
            #print("z", z)
            #print("relu(z)", self.relu(z))
            if i < num_layers-1:  # Assuming the output layer has no activation.
                hiddens.append(self.relu(z))
                
        #print("hiddens", hiddens)
        # apply softmax to z
        #print("z", z)
        
        output = self.softmax(z)
        
        #print("output", output)
        
        #compute output
        
        return output, hiddens

    #tomas.costa@tecn...


    def compute_loss(self, output, y):
        # compute loss
        loss = -y * (np.log(output))
                
        return loss      
        
    def predict(self, X):
        # Compute the forward pass of the network. At prediction time, there is
        # no need to save the values of hidden nodes, whereas this is required
        # at training time.

        # X (n_examples x n_features)
        # return: (n_examples)
        predicted_labels = []
        for x in X:
            # Compute forward pass and get the class with the highest probability
            output, _ = self.forward(x)
            y_hat = np.argmax(output)
            predicted_labels.append(y_hat)
        predicted_labels = np.array(predicted_labels)
        print("predicted_labels", np.unique(predicted_labels))
        return predicted_labels
    
    
    def evaluate(self, X, y):
        """
        X (n_examples x n_features)
        y (n_examples): gold labels
        """
        print("evaluate")
        print("weights", self.weights)
        print("biases", self.biases)
        # Identical to LinearModel.evaluate()
        y_hat = self.predict(X)
        n_correct = (y == y_hat).sum()
        print("n_correct", n_correct)
        n_possible = y.shape[0]
        print("n_possible", n_possible)
        return n_correct / n_possible
    


    def train_epoch(self, X, y, learning_rate=0.001):
        """
        Dont forget to return the loss of the epoch.
        """
        num_layers = 2
        total_loss = 0
        print(len(X))
        print(len(y))
        iter = 0
        # For each observation and target
        for x, y in zip(X, y):
            print("iter", iter)
            iter+=1
            
            if iter == 100:
                print("x", x)
                print("y", y)
                print("weights", self.weights)
                print("biases", self.biases)
                exit()
            # Compute forward pass
            output, hiddens = self.forward(x)

            # Compute Loss and Update total loss
            loss = self.compute_loss(output, y)
            total_loss+=loss
            # Compute backpropagation
            grad_weights, grad_biases = self.backward(x, y, output, hiddens)
            
            # Update weights
            
            for i in range(num_layers):
                self.weights[i] -= learning_rate*grad_weights[i]
                self.biases[i] -= learning_rate*grad_biases[i]
                
        print("total_loss", total_loss)
                
        return total_loss
                


def plot(epochs, train_accs, val_accs):
    plt.xlabel('Epoch')
    plt.ylabel('Accuracy')
    plt.plot(epochs, train_accs, label='train')
    plt.plot(epochs, val_accs, label='validation')
    plt.legend()
    plt.show()
    plt.savefig('images/q1_2b.png')

def plot_loss(epochs, loss):
    plt.xlabel('Epoch')
    plt.ylabel('Loss')
    plt.plot(epochs, loss, label='train')
    plt.legend()
    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('model',
                        choices=['perceptron', 'logistic_regression', 'mlp'],
                        help="Which model should the script run?")
    parser.add_argument('-epochs', default=20, type=int,
                        help="""Number of epochs to train for. You should not
                        need to change this value for your plots.""")
    parser.add_argument('-hidden_size', type=int, default=200,
                        help="""Number of units in hidden layers (needed only
                        for MLP, not perceptron or logistic regression)""")
    parser.add_argument('-learning_rate', type=float, default=0.001,
                        help="""Learning rate for parameter updates (needed for
                        logistic regression and MLP, but not perceptron)""")
    opt = parser.parse_args()

    utils.configure_seed(seed=42)

    add_bias = opt.model != "mlp"
    data = utils.load_oct_data(bias=add_bias)
    train_X, train_y = data["train"]
    dev_X, dev_y = data["dev"]
    test_X, test_y = data["test"]
    n_classes = np.unique(train_y).size
    n_feats = train_X.shape[1]

    # initialize the model
    if opt.model == 'perceptron':
        model = Perceptron(n_classes, n_feats)
    elif opt.model == 'logistic_regression':
        model = LogisticRegression(n_classes, n_feats)
    else:
        model = MLP(n_classes, n_feats, opt.hidden_size)
    epochs = np.arange(1, opt.epochs + 1)
    train_loss = []
    valid_accs = []
    train_accs = []
    
    for i in epochs:
        print('Training epoch {}'.format(i))
        train_order = np.random.permutation(train_X.shape[0])
        train_X = train_X[train_order]
        train_y = train_y[train_order]
        if opt.model == 'mlp':
            loss = model.train_epoch(
                train_X,
                train_y,
                learning_rate=opt.learning_rate
            )
        else:
            model.train_epoch(
                train_X,
                train_y,
                learning_rate=opt.learning_rate
            )
        
        train_accs.append(model.evaluate(train_X, train_y))
        print("train_accs", train_accs)
        valid_accs.append(model.evaluate(dev_X, dev_y))
        print("valid_accs", valid_accs)
        if opt.model == 'mlp':
            print('loss: {:.4f} | train acc: {:.4f} | val acc: {:.4f}'.format(
                loss, train_accs[-1], valid_accs[-1],
            ))
            train_loss.append(loss)
        else:
            print('train acc: {:.4f} | val acc: {:.4f}'.format(
                 train_accs[-1], valid_accs[-1],
            ))
    print('Final test acc: {:.4f}'.format(
        model.evaluate(test_X, test_y)
        ))

    # plot
    plot(epochs, train_accs, valid_accs)
    if opt.model == 'mlp':
        plot_loss(epochs, train_loss)


if __name__ == '__main__':
    main()
