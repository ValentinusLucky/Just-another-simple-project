import model

def main():

    # Get current state and control input from user

    # xk = list(map(float, input("Insert xk: ").split()))
    # print("The given values of xk are: ", xk)

    # uk = list(map(float, input("Insert uk: ").split()))
    # print("The given values of uk are: ", uk)

    # fun = model.model(xk, uk[0])
    # print(fun)

    # Test area: give preset
    xk = [0.0, 0.0, 0.0, 0.0]
    uk = [0.0]
    xd = [0.1, 0.1, 0.1, 0.1]

    model.addNN(xk, uk, xd, 5, 3)


if __name__ == "__main__":
    main()

