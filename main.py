import model

def main():

    # Get current state and control input from user

    xk = list(map(float, input("Insert xk: ").split()))
    print("The given values of xk are: ", xk)

    uk = list(map(float, input("Insert uk: ").split()))
    print("The given values of uk are: ", uk)


    fun = model.model(xk, uk[0])
    print(fun)

if __name__ == "__main__":
    main()

