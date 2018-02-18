import numpy as np
import matplotlib.pyplot as plt


# Generates a vector containing random angles ranging from 0 to pi
def random_angle_generator(N):
    angle_array = np.random.uniform(0, np.pi, size=N)
    return angle_array


# converts the generated angles into x-positions
def position_converter(angle_array, x_0, y_0):
    position_array = np.zeros(len(angle_array))
    for i in range(len(angle_array)):
        if angle_array[i] == 0:
            angle_array[i] = 0.001
            position_array[i] = x_0 - y_0 / np.tan(angle_array[i])

        elif angle_array[i] == 2 * np.pi:
            angle_array[i] = np.pi - 0.001
            position_array = x_0 + abs(y_0 / np.tan(angle_array[i]))

        elif angle_array[i] == np.pi / 2:
            angle_array[i] = np.pi / 2 - 0.001
            position_array[i] = x_0 - y_0 / np.tan(angle_array[i])

        elif angle_array[i] > np.pi / 2 and angle_array[i] != np.pi:
            position_array[i] = x_0 + abs(y_0 / np.tan(angle_array[i]))

        elif angle_array[i] < np.pi / 2 and angle_array[i] != 0:
            position_array[i] = x_0 - y_0 / np.tan(angle_array[i])

    return position_array


def posterior(position_array, x_0, y_0):
    # using a flat prior, the x_0 input is not necessary since an arbitrary limit/range can be used
    limit = np.arange(-100 + x_0, 100 + x_0)
    log_array = np.zeros((np.size(limit), np.size(position_array)))
    posterior_array = np.zeros(np.size(limit))

    for i in range(np.size(limit)):
        for k in range(0, np.size(position_array)):
            log_array[i][k] = - np.log(np.power(y_0, 2) + np.power(position_array[k] - (limit[i]), 2))

    for i in range(np.size(limit)):
        posterior_array[i] = np.sum(log_array[i])  # sums up all the log terms for a fixed alpha

    return posterior_array, limit

def log_posterior_2(x, y, position_array):

    Z = np.zeros((np.size(y), (np.size(x))))
    Z_temp = np.zeros(np.size(position_array))

    #print("size of y = ")
    #print(np.size(y))
    #print(" ")
    #print(" ")

    for j in np.arange(np.size(y)):
        for i in np.arange(np.size(x)):
            for k in np.arange(np.size(position_array)):
                Z_temp[k] = - np.log(np.power(y[j], 2) + np.power(position_array[k] - x[i], 2))
            #print(i)
            #print(j)
            #print("  ")
            #print("  ")
            Z[j][i] = np.sum(Z_temp)


    return Z



def posterior_2(position_array, x_0, y_0):
    # the x_0 and y_0 input is not necessary since an arbitrary limit/range can be used
    limit_x = np.arange(-50 + x_0, 50 + x_0)
    limit_y = np.arange(- 30 + y_0, 50 + y_0)
    x = limit_x
    y = limit_y
    X, Y = np.meshgrid(x, y)
    #Z = np.power(X, 2) + np.power(Y, 2 )
    Z = log_posterior_2(x, y, position_array)


    plt.figure()
    plt.contour(X, Y, Z, colors='black');
    plt.show()


'''The function below estimated posterior without taking the log, this will result in posterior --> 0 as the data set
    increases ( which is incorrect).

    likelihood_matrix = np.zeros((np.size(limit), np.size(position_array)))
    posterior_array = np.zeros(len(limit))
    for i in range(np.size(limit)):
            for j in range(0,len(position_array)):
                likelihood_matrix[i][j] = y_0/(np.pi*(np.power(y_0, 2) + np.power((position_array[j] - limit[i]), 2)))
    for i in range(0, np.size(limit)):
        posterior_array[i] = np.prod(likelihood_matrix[i][:])'''


def light_house(x_0, y_0, N):
    angle_array = random_angle_generator(N)
    position_array = position_converter(angle_array, x_0, y_0)
    hist_range = [x_0 - 500, x_0 + 500]

    posterior_array, limit = posterior(position_array, x_0, y_0)

    position_average = np.sum(position_array) / N

    '''making subplots'''

    '''Finding maximum value of posterior'''
    '''
    posterior_max = np.argmax(posterior_array)  # returns the index for the maximum value in posterior_array
    position_max = limit[posterior_max]  # finds the x-position for the best estimate

    plt.style.use('ggplot')
    fig, axes = plt.subplots(2, sharex=True)
    ax1, ax2 = axes.ravel()
    ax1.hist(position_array, 'fd', hist_range, normed=False, weights=None, density=None)

    ax2.plot(limit, posterior_array)

    ax1.set_title('Light house: data histogram and posterior graph')
    ax1.set_xlabel('Positions along the shore')
    ax1.set_ylabel('Counts')

    ax2.set_xlabel('Positions along the shore')
    ax2.set_ylabel('Posterior graph')

    ax2.vlines(position_average, -500, 100, colors='g')

    ax1.legend((N, round(position_average)), loc='upper right', shadow=True)
    ax2.legend((position_max, (round(position_average))), loc='upper right', shadow=True)

    fig.tight_layout()
    plt.show()
    '''

    posterior_2(position_array, x_0, y_0)

#######################################################################################################################
# light_house-function input parameters : (x_0,y_0,N)
# x_0,y_0= position of light house, N = number of data

light_house(0, 30, 100)






