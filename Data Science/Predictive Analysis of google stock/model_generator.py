import csv
import matplotlib.pyplot as plt

def get_stock_data(filename, dates, prices):
    '''
    A function to retrieve the stock data from the csv file
    :param filename: the name of the csv file.
    :param dates: an array that contains
    the date of each stock price in chronological order

    :param prices: an array to be filled with the prices at each day
    '''
    with open(filename, 'r') as csvfile:
        csvFileReader = csv.reader(csvfile)
        next(csvFileReader)
        for row in csvFileReader:
            dates.insert(0,row[0])
            prices.insert(0,float(row[1]))
    return 0

def calculate_error_measurement_for_eqn(m, b, points):
    '''
    A error measurement for a paticular slope and principal
    value y = mx + b. The error measurement is sum of squared error
    :param m: the slope
    :param b: the principal
    :param points: a 2d list with each data point (date,price)
    :return Error: the error measurement for that particular line of best fit 
    '''
    totalError = 0
    for point in points:
        x = point[0] #x coordinate which is date
        y = point[1] #y coordinate which is value
        totalError += (y - ((m*x) +b))**2
    return totalError/float(len(points))

def optimize_parameters(m, b, points, learning_rate):
    '''
    Function that calculates the gradient of the error measurement
    and changes the m and b value in order to reduce error.
    :param m:the slope of our line of best fit
    
    :param b:the principal amount or b value for line of best fit
    
    :param points:A 2d list with each element being (x,y) value of the
    data point
    
    :param learning_rate: the step in which the slope and principal amount
    will be updated.

    :return [new_m,new_b]: a tuple that contains the updated slope
    and principal value that would reduce error
    '''
    b_grad = 0
    m_grad = 0
    N = float(len(points))
    for point in points:
        x = point[0]
        y = point[1]
        m_grad += -(2/N) * x * ( y - ((m * x) + b))#the partial derivative of m to error
        b_grad += -(2/N) *( y - ((m * x) + b))#the partial derivative of b to error
    new_m = m - (learning_rate*m_grad)
    new_b = b - (learning_rate*b_grad)
    return [new_m,new_b]

def gradient_descent_algorithm():
    '''
    The algorithm to determine the line of best fit for google stocks.
    :return m: the slope of the line of best fit y=mx+b
    :return b:the principal value in the line of best fit (y=mx+b)
    when x=0 
    return error_margin:
    :return graph: A 2d graph that has all the prices as y and
    the day as x value in (x,y)
    '''
    dates = []
    prices = []
    get_stock_data('Data/googleOneYear.csv', dates, prices)    
    graph = []
    for i in range(len(prices)):
        graph.append([i+1, prices[i]])
    m = 1
    b = graph[0][1]
    error_margin = calculate_error_measurement_for_eqn(m, b, graph)
    for i in range(30000):
        results = optimize_parameters(m, b, graph, 0.00001)
        m=results[0]
        b=results[1]
        error_margin = calculate_error_measurement_for_eqn(m, b, graph)
    return m, b, error_margin, graph

def display_findings():
    '''
    A function that will run the gradient descent algorithm to find the
    line of best fit for google stocks in the past year.
    
    '''
    gradient_results = gradient_descent_algorithm()
    m=gradient_results[0]
    b=gradient_results[1]
    graph=gradient_results[3]
    prices=[]
    linear_fit=[]
    for i in range(len(graph)):
        prices.append(graph[i][1])
        linear_fit.append(m*i + b)

    plt.plot(prices,label = 'actual prices')
    plt.plot(linear_fit, label='linear fit y = {} x + {}'.format(m,b))
    plt.xlabel('day',fontsize=16)
    plt.ylabel('price per share',fontsize=16)
    plt.title("closing price of google stock from {} to {}".format("2017/03/23","2018/03/23"))
    plt.legend()
    plt.show()
        
        
    

        
    
    
        
    

    
    
    
                         
