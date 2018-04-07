import numpy as np
import matplotlib.pyplot as plt


def svm_decision_calculator(dataset, labels):
    #a weight vector
    w = np.zeros(len(dataset[0]))
    #learning rate for the algoritm
    learning_rate = 1
    #number of iterations
    iterations = 100000
    #a list to store the the number of errors per iteration
    errors = []

    for iteration in range(1,iterations):
        error = 0
        for i, x in enumerate(dataset):
            #if the datapoint was missclassified 
            if(labels[i]*np.dot(dataset[i],w)) < 1:
                w = w + learning_rate*((dataset[i]*labels[i]) + (-2 *(1/iteration) * w))
                error +=1
            #if the datapoint was classified properly
            else:
                w = w+ learning_rate*(-2 *(1/iteration) * w)
        errors.append(error)
    return w,errors
def main():
    #Input data - Of the form [X value, Y value, Bias term]
    points = np.array([
    [-2,4,-1],
    [4,1,-1],
    [1, 6, -1],
    [2, 4, -1],
    [6, 2, -1],
    ])

    #Associated output labels - First 2 examples are labeled '-1' and last 3 are labeled '+1'
    labels = np.array([-1,-1,1,1,1])

    #lets plot these examples on a 2D graph!
    #for each example
    for d, sample in enumerate(points):
        # Plot the negative samples (the first 2)
        if d < 2:
            plt.scatter(sample[0], sample[1], s=120, marker='_', linewidths=2)
        # Plot the positive samples (the last 3)
        else:
            plt.scatter(sample[0], sample[1], s=120, marker='+', linewidths=2)
    
    results = svm_decision_calculator(points,labels)
    #A vector that contains the A,B,C value in decision linear eqn in the format
    #Ax+By-C=0 
    w = results[0]
    # an array of y values for the decision line
    y_values = []
    #an array of x values for the decision line
    x_values = []
    #caclulate the slope for the decision line
    m =-1* w[0]/w[1]
    #calculate the b value for the decision
    b = w[2]/w[1]
    for i in range(-6,10):
        y_values.append(m*i + b)
        x_values.append(i)
    #matplot needs an array of x values and an array of y values to plot a line    
    plt.plot(x_values,y_values)
    plt.show()
                        

            
                
        

            
