import numpy as np
from casadi import *

def model(xk, uk):
    """Function of the dynamical model"""

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



def optiInit(N):
    opti = casadi.Opti()

    x = opti.variable(4, N+1)
    u = opti.variable(2, N)
    p = opti.parameter(4, 1)

    u_star = opti.parameter(2, N)

    toggle = opti.parameter() #currently unused

    return opti, x, u, p, u_star

