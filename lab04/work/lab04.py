from math import exp, fsum, isfinite, lgamma, log
from numbers import Integral
from pathlib import Path


class Model:
    def __init__(self, C, g, lambda1, lambda2, mu1, mu2):
        if isinstance(C, bool) or not isinstance(C, Integral) or C < 0:
            raise ValueError("C должно быть целым числом не меньше 0.")
        if isinstance(g, bool) or not isinstance(g, Integral) or not 0 <= g <= C:
            raise ValueError("g должно быть целым числом: 0 <= g <= C.")

        self.C = int(C)
        self.g = int(g)
        self.lambda1 = float(lambda1)
        self.lambda2 = float(lambda2)
        self.mu1 = float(mu1)
        self.mu2 = float(mu2)

        if not all(isfinite(value) for value in
                   (self.lambda1, self.lambda2, self.mu1, self.mu2)):
            raise ValueError("Интенсивности должны быть конечными числами.")
        if self.lambda1 < 0 or self.lambda2 < 0:
            raise ValueError("lambda1 и lambda2 должны быть не меньше 0.")
        if self.mu1 <= 0 or self.mu2 <= 0:
            raise ValueError("mu1 и mu2 должны быть больше 0.")

        self.rho1 = self.lambda1 / self.mu1
        self.rho2 = self.lambda2 / self.mu2
        self.calculateProbabilities()
        self.calculateResults()

    def calculateProbabilities(self):
        logRho1 = log(self.lambda1) - log(self.mu1) if self.lambda1 else None
        logRho2 = log(self.lambda2) - log(self.mu2) if self.lambda2 else None
        logWeights = {}

        # Логарифмы предотвращают переполнение степеней и факториалов.
        for n1 in range(self.g + 1):
            for n2 in range(self.C - n1 + 1):
                if (self.lambda1 == 0 and n1 > 0 or
                        self.lambda2 == 0 and n2 > 0):
                    logWeights[(n1, n2)] = float("-inf")
                    continue

                weight1 = n1 * logRho1 if n1 else 0.0
                weight2 = n2 * logRho2 if n2 else 0.0
                logWeights[(n1, n2)] = (
                    weight1 + weight2 - lgamma(n1 + 1) - lgamma(n2 + 1)
                )

        maxWeight = max(logWeights.values())
        weights = {state: exp(value - maxWeight)
                   for state, value in logWeights.items()}
        totalWeight = fsum(weights.values())
        self.probabilities = {state: value / totalWeight
                              for state, value in weights.items()}
        self.P0 = self.probabilities[(0, 0)]

    def calculateResults(self):
        self.E1 = fsum(p for (n1, n2), p in self.probabilities.items()
                       if n1 == self.g or n1 + n2 == self.C)
        self.E2 = fsum(p for (n1, n2), p in self.probabilities.items()
                       if n1 + n2 == self.C)
        self.N1 = fsum(n1 * p for (n1, n2), p in self.probabilities.items())
        self.N2 = fsum(n2 * p for (n1, n2), p in self.probabilities.items())
        self.N = self.N1 + self.N2

    def printTask10(self):
        print("\nРаспределение вероятностей:")
        for (n1, n2), probability in self.probabilities.items():
            print(f"p({n1}, {n2}) = {probability:.10g}")

        print(f"\nСумма вероятностей: {fsum(self.probabilities.values()):.12f}")
        print(f"Вероятность блокировки типа 1: {self.E1:.10g}")
        print(f"Вероятность блокировки типа 2: {self.E2:.10g}")
        print(f"Среднее число заявок типа 1: {self.N1:.10g}")
        print(f"Среднее число заявок типа 2: {self.N2:.10g}")
        print(f"Среднее общее число заявок: {self.N:.10g}")


def calculateSeries(model, lambdas, arrivalType=1):
    if arrivalType not in (1, 2):
        raise ValueError("arrivalType должно быть 1 или 2.")

    results = {"E1": [], "E2": [], "N1": [], "N2": [], "N": []}
    for arrivalRate in lambdas:
        lambda1 = arrivalRate if arrivalType == 1 else model.lambda1
        lambda2 = arrivalRate if arrivalType == 2 else model.lambda2
        current = Model(model.C, model.g, lambda1, lambda2,
                        model.mu1, model.mu2)
        results["E1"].append(current.E1)
        results["E2"].append(current.E2)
        results["N1"].append(current.N1)
        results["N2"].append(current.N2)
        results["N"].append(current.N)
    return results


def finishPlot(fig, savePath, show):
    import matplotlib.pyplot as plt

    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    if savePath is not None:
        savePath = Path(savePath)
        savePath.parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(savePath, dpi=180)
    if show:
        plt.show()
    else:
        plt.close(fig)
    return fig


def grafic_task11(model, lambdas, arrivalType=1, savePath=None, show=True):
    import matplotlib.pyplot as plt

    lambdas = list(lambdas)
    results = calculateSeries(model, lambdas, arrivalType)
    fixedType = 2 if arrivalType == 1 else 1
    fixedRate = model.lambda2 if arrivalType == 1 else model.lambda1

    fig = plt.figure(figsize=(10, 5))
    plt.plot(lambdas, results["E1"], label=r"$\beta_1$")
    plt.plot(lambdas, results["E2"], label=r"$\beta_2$")
    plt.title("Зависимость вероятностей блокировки от интенсивности поступления\n"
              + fr"$C={model.C},\ g={model.g},\ \lambda_{fixedType}={fixedRate:g},"
                fr"\ \mu_1={model.mu1:g},\ \mu_2={model.mu2:g}$")
    plt.xlabel(fr"$\lambda_{arrivalType}$, заявок / ед. времени")
    plt.ylabel("Вероятность блокировки")
    plt.ylim(0, 1)
    return finishPlot(fig, savePath, show)


def grafic_task12(model, lambdas, arrivalType=1, savePath=None, show=True):
    import matplotlib.pyplot as plt

    lambdas = list(lambdas)
    results = calculateSeries(model, lambdas, arrivalType)
    fixedType = 2 if arrivalType == 1 else 1
    fixedRate = model.lambda2 if arrivalType == 1 else model.lambda1

    fig = plt.figure(figsize=(10, 5))
    plt.plot(lambdas, results["N1"], label=r"$\overline{N}_1$")
    plt.plot(lambdas, results["N2"], label=r"$\overline{N}_2$")
    plt.plot(lambdas, results["N"], label=r"$\overline{N}$")
    plt.title("Зависимость среднего числа заявок от интенсивности поступления\n"
              + fr"$C={model.C},\ g={model.g},\ \lambda_{fixedType}={fixedRate:g},"
                fr"\ \mu_1={model.mu1:g},\ \mu_2={model.mu2:g}$")
    plt.xlabel(fr"$\lambda_{arrivalType}$, заявок / ед. времени")
    plt.ylabel("Среднее число обслуживаемых заявок")
    plt.ylim(0, max(model.C, 1))
    return finishPlot(fig, savePath, show)


if __name__ == "__main__":
    print("Лабораторная работа №4")
    print("Неполнодоступная двухсервисная модель Эрланга с резервированием")

    try:
        C = int(input("C: "))
        g = int(input("g: "))
        lambda1 = float(input("lambda1: "))
        lambda2 = float(input("lambda2: "))
        mu1 = float(input("mu1: "))
        mu2 = float(input("mu2: "))

        model = Model(C, g, lambda1, lambda2, mu1, mu2)
        model.printTask10()

        defaultMax = max(10.0, lambda1, lambda2)
        lambdaMax = float(input(f"Максимальная интенсивность [{defaultMax:g}]: ")
                          or defaultMax)
        numberOfPoints = int(input("Число точек на графике [101]: ") or 101)
        if not isfinite(lambdaMax) or lambdaMax <= 0 or numberOfPoints < 2:
            raise ValueError("Максимум должен быть больше 0, число точек — не меньше 2.")
        lambdas = [lambdaMax * (i / (numberOfPoints - 1))
                   for i in range(numberOfPoints)]
    except (ValueError, OverflowError) as error:
        raise SystemExit(f"Ошибка входных данных: {error}")

    imagePath = Path(__file__).resolve().parent.parent / "image"
    for arrivalType in (1, 2):
        grafic_task11(model, lambdas, arrivalType,
                      imagePath / f"blocking_lambda{arrivalType}.png")
        grafic_task12(model, lambdas, arrivalType,
                      imagePath / f"mean_lambda{arrivalType}.png")
