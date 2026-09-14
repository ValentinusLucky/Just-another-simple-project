import model

def main():

    print("Insert xk")
    xk = input()

    print("Insert uk")
    uk = input()

    model.model(xk, uk)

if __name__ == "__main__":
    main()

