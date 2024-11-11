import numpy as np
import pandas as pd

data = pd.read_csv('binary.csv')

one_hot_data = pd.concat([data, pd.get_dummies(data['rank'], prefix='rank', dtype=int)], axis=1)
one_hot_data = one_hot_data.drop('rank', axis=1)

# Copying our data
processed_data = one_hot_data[:]

# Scaling the columns
processed_data['gre'] = processed_data['gre']/800
processed_data['gpa'] = processed_data['gpa']/4.0

sample = np.random.choice(processed_data.index, size=int(len(processed_data)*0.9), replace=False)
train_data, test_data = processed_data.iloc[sample], processed_data.drop(sample)

features = train_data.drop('admit', axis=1)
targets = train_data['admit']
features_test = test_data.drop('admit', axis=1)
targets_test = test_data['admit']

def sigmoid(x):
    """
    Calculate sigmoid
    """
    return 1 / (1 + np.exp(-x))

def update_weights(weights, features, targets, learnrate):
  """
  Complete a single epoch of gradient descent and return updated weights
  """
  del_w = np.zeros(weights.shape)
  # Loop through all records, x is the input, y is the target
  for x, y in zip(features.values, targets):
      # Calculate the output of f(h) by passing h (the dot product
      # of x and weights) into the activation function (sigmoid).
      output = sigmoid(np.dot(x, weights))

      # Calculate the error by subtracting the network output
      # from the target (y).
      error = y - output

      # Calculate the error term by multiplying the error by the
      # gradient. Recall that the gradient of the sigmoid f(h) is
      # f(h)*(1−f(h)) so you do not need to call any additional
      # functions and can simply apply this formula to the output and
      # error you already calculated.
      error_term = error  *output*  (1 - output)

      # Update the weight step by multiplying the error term by
      # the input (x) and adding this to the current weight step.
      del_w += error_term * x

  # Update the weights by adding the learning rate times the
  # change in weights divided by the number of records.
  n_records = features.shape[0]
  weights += learnrate * del_w / n_records
  
  return weights

def gradient_descent(features, targets, epochs=5, learnrate=0.5):
    """
    Perform the complete gradient descent process on a given dataset
    """
    # Use to same seed to make debugging easier
    np.random.seed(42)
    
    # Initialize loss and weights
    last_loss = None
    n_features = features.shape[1]
    weights = np.random.normal(scale=1/n_features**.5, size=n_features)

    # Repeatedly update the weights based on the number of epochs
    for e in range(epochs):
        weights = update_weights(weights, features, targets, learnrate)

        # Printing out the MSE on the training set every 10 epochs.
        # Initially this will print the same loss every time. When all of
        # the TODOs are complete, the MSE should decrease with each
        # printout
        if e % (epochs / 10) == 0:
            out = sigmoid(np.dot(features, weights))
            # print(out)
            loss = np.mean((out - targets) ** 2)
            if last_loss and last_loss < loss:
                print("Train loss: ", loss, "  WARNING - Loss Increasing")
            else:
                print("Train loss: ", loss)
            last_loss = loss
            
    return weights

# Calculate accuracy on test data

weights = gradient_descent(features, targets)
tes_out = sigmoid(np.dot(features_test, weights))
predictions = tes_out > 0.5
accuracy = np.mean(predictions == targets_test)
print("Prediction accuracy: {:.3f}".format(accuracy))
