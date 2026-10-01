import numpy as np
from casadi import *

def model(xk, uk):
    """
    Function of the dynamical model

    dt : time step, set to 0.1s
    
    xk : state vector at time k
    uk : control input at time k

    x[0] : position
    x[1] : velocity
    x[2] : angle
    x[3] : angular velocity
    
    Return resulting state vector at time k+1
    """

    getModelPars()

    dt = 0.1

    x_acc = (uk + mc * sin(xk[2]) * (l*(xk[3]**2) + g*cos(xk[2]))) / (mk+mc*(sin(xk[2])**2))
    theta_acc = (-uk * cos(xk[2]) - mc*l*(xk[3]**2)*sin(xk[2])*cos(xk[2]) - (mk+mc)*g*sin(xk[2]) )/ (l*(mk+mc*(sin(xk[2])**2)))

    fun = xk + dt * vertcat(xk[1], 
                        x_acc, 
                        xk[3], 
                        theta_acc)

    return fun


def getModelPars():
    """Function to get the parameters of the model"""

    global mk, mc, l, g

    mk = 0.5
    mc = 0.5
    l = 0.6
    g = 9.81

## NN modeling

def addNN(xk, uk, xd, n, d):
    """
    Function to add the neural network to the model

    xk : state vector at time k
    uk : control input at time k
    n : number of neurons in the hidden layer
    d : depth of the neural network

    Return resulting state vector at time k+1
    """

    getModelPars()

    # Create randomizer for weights and biases
    # Format of weights and biases:
        # weights = [[Layer1], [Layer2], ..., [LayerN]] e.g [[n_x,z], [z,z], [z,n_y]]
        # biases = [[Layer1], [Layer2], ..., [LayerN]] e.g [[z], [z], [n_y]]
    
    n_x = np.shape(xk)[0]
    n_u = np.shape(uk)[0]

    np.random.seed(0)
    # TODO: Depth is set to 3 for now
    # TODO: Check randn
    weights = [np.random.randn(n_x, n), np.random.randn(n, n), np.random.randn(n, 1)]
    biases = [np.random.randn(n_u, n), np.random.randn(n,), np.random.randn(1,)]

    # TODO: x instead of xk, optiInit
    y = casadi_mlp(xk, weights, biases)
    y_d = casadi_mlp(xd, weights, biases)
    cost = y - y_d

    return cost


def casadi_mlp(x, weights, biases):
    """
    NN Casadi; Tanh activation

    Options are disabled for now

    Format of weights and biases:
    weights = [[Layer1], [Layer2], ..., [LayerN]] e.g [[n_x,z], [z,z], [z,n_y]]
    biases = [[Layer1], [Layer2], ..., [LayerN]] e.g [[z], [z], [n_y]]
    """

    a = x
    for W, b in zip(weights[:-1], biases[:-1]):
        z = casadi.mtimes(W, a) + b
        # a = casadi.fmax(z, 0)         # ReLU
        a = casadi.tanh(z)            # Tanh
        # a = 1 / (1 + casadi.exp(-z))     # Sigmoid
    out = casadi.mtimes(weights[-1], a) + biases[-1]
    return out



def optiInit(N):
    opti = casadi.Opti()

    x = opti.variable(4, N+1)
    u = opti.variable(2, N)
    p = opti.parameter(4, 1)

    u_star = opti.parameter(2, N)

    toggle = opti.parameter() #currently unused

    return opti, x, u, p, u_star

