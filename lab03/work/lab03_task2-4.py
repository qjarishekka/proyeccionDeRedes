import os


class Model:
    def __init__(self, C, lambda1, lambda2, theta1, theta2, *, silent=False):
        self.C = C
        self.lambda1 = lambda1
        self.lambda2 = lambda2
        self.theta1 = theta1
        self.theta2 = theta2

        self.rho1 = self.lambda1 * self.theta1
        self.rho2 = self.lambda2 * self.theta2
        self.a1 = self.rho1 / self.C
        self.a2 = self.rho2 / self.C
        self.a = self.a1 + self.a2

        

        from math import factorial

        K = 40
        suma = 0

        for n1 in range(K + 1):
            for n2 in range(K - n1 + 1):
                peso = (
                    factorial(n1 + n2)
                    * self.a1**n1
                    * self.a2**n2
                    / (factorial(n1) * factorial(n2))
                )
                suma += peso

        p00 = 1 / suma

        if not silent:
            print("p(0,0) ≈", p00)


        probabilities = {}
        probabilities[(0, 0)] = p00

        for n1 in range(K + 1):
            for n2 in range(K-n1 + 1):
                probabilities[(n1, n2)] =( (self.a1 ** n1 * self.a2 **n2 )/  ( factorial(n1)  * factorial(n2) )   ) * factorial(n1+n2) * p00
                if not silent:
                    print("p(", n1, ",", n2, ") =", probabilities[(n1, n2)])




        self.N1 = lambda1 * theta1 / ((theta1* lambda1) + (theta2 * lambda2))
        self.N2 = lambda2 * theta2 / ((theta1* lambda1) + (theta2 * lambda2))

        if not silent:
            print("\nСреднее число N_i")
        if not silent:
            print(" N1 =", self.N1)
        if not silent:
            print(" N2 =", self.N2)

        self.T1 = self.N1 / lambda1
        self.T2 = self.N2 / lambda2
        if not silent:
            print("\nСреднее время T_i")
        if not silent:
            print(" T1 =", self.T1)
        if not silent:
            print(" T2 =", self.T2)


def grafic_task3(C , lambda2, theta1, theta2):
    import matplotlib.pyplot as plt

    lambdas = []
    avg_time = []

    for lambda1 in range(1, 101):
        # Стационарные результаты существуют только при нагрузке ниже пропускной способности.
        if lambda1 * theta1 + lambda2 * theta2 >= C:
            continue

        model = Model(C, lambda1, lambda2, theta1, theta2, silent=True)
        lambdas.append(lambda1)
        avg_time.append((model.T1, model.T2))



    ancho = 0.4
    plt.plot(lambdas,
            [t[0] for t in avg_time], label="T1")
    plt.plot(lambdas,
            [t[1] for t in avg_time],  label="T2")
    plt.xlabel("Интенсивность поступления запросов λ₁")
    plt.ylabel("Среднее время обслуживания запроса")
    plt.title("Зависимость среднего времени обслуживания от λ₁ (устойчивый режим)")
    plt.legend()
    plt.show()

def grafic_task4(C , lambda2, theta1, theta2):
    import matplotlib.pyplot as plt

    lambdas = []
    avg_time = []

    for lambda1 in range(1, 101):
        # Стационарные результаты существуют только при нагрузке ниже пропускной способности.
        if lambda1 * theta1 + lambda2 * theta2 >= C:
            continue

        model = Model(C, lambda1, lambda2, theta1, theta2, silent=True)
        lambdas.append(lambda1)
        avg_time.append((model.N1, model.N2))


    ancho = 0.4
    plt.plot(lambdas,
            [t[0] for t in avg_time], label="N1")
    plt.plot(lambdas,
            [t[1] for t in avg_time], label="N2")
    plt.xlabel("Интенсивность поступления запросов λ₁")
    plt.ylabel("среднего числа обслуживаемых запросов")
    plt.title("Зависимость среднего числа обслуживаемых запросов от λ₁ (устойчивый режим)")
    plt.legend()
    plt.show()



if(__name__ == "__main__"):

    C = 0
    lambda1 = 0
    lambda2 = 0
    theta1 = 0
    theta2 = 0

    print("\nпрограмма моделирования Двухсервисной модели с эластичным трафиком\n")
    C = int(input("введите значение для C: "))
    lambda1 = int(input("введите значение для lambda1: "))
    lambda2 = int(input("введите значение для lambda2: "))
    theta1 = float(input("введите значение для theta1: "))
    theta2 = float(input("введите значение для theta2: "))

    model = Model(C, lambda1, lambda2, theta1, theta2)

    grafic_task3(C, lambda2, theta1, theta2)
    grafic_task4(C, lambda2, theta1, theta2)



