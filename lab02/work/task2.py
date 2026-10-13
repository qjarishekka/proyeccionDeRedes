from math import factorial
import matplotlib.pyplot as plt

class IncompleteDualErlangModel:

    def __init__(self, Capacity:int, reservedCapacity:int, arrival_rate_1:float, arrival_rate_2:float, u:float):

        self.Capacity = Capacity
        self.reservedCapacity = reservedCapacity
        self.arrival_rate_1 = arrival_rate_1
        self.arrival_rate_2 = arrival_rate_2
        self.u = u

        self.rho1 = arrival_rate_1/u
        self.rho2 = arrival_rate_2/u
        self.calculate_P0()
        self.calculateArrayOfProbabilities()
        self.probabilityOfBlockingFirstType = self.arrayOfProbabilities[-1]
        self.probabilityOfBlockingSecondType = sum( self.arrayOfProbabilities[reservedCapacity:])
        # La media usa todos los estados desde 0 hasta C: N = sum(n * p_n).
        self.averageRequestServerd =  sum( [x *y for x ,y in zip(range(0,self.Capacity+1), self.arrayOfProbabilities  ) ]   )



    def calculate_P0(self):
        self.P0 = 0
        suma1 = 0 
        suma2 = 0
        for n in range(1,self.reservedCapacity+1):
            suma1 = suma1+ ((self.rho1 + self.rho2 )**n)/ factorial(n)

        for n in range(self.reservedCapacity+1,self.Capacity+1):
            suma2 = suma2 + (((self.rho1 + self.rho2)**self.reservedCapacity * self.rho1**(n-self.reservedCapacity))/factorial(n))
        
        # El 1 representa el estado vacío n = 0 en la constante de normalización.
        self.P0= (1 + suma1 + suma2)**-1

    def calculateArrayOfProbabilities(self):
        # La distribución debe contener todas las probabilidades: p_0, p_1, ..., p_C.
        self.arrayOfProbabilities = []
        self.arrayOfProbabilities.append(self.P0)
        

        for n in range(1,self.reservedCapacity+1):
            self.arrayOfProbabilities.append(  
                self.P0 * ((self.rho1 + self.rho2 )**n)/factorial(n) 
            )

        for n in range(self.reservedCapacity+1, self.Capacity+1):
            self.arrayOfProbabilities.append( 
                (self.P0 * ((self.rho1 + self.rho2)**self.reservedCapacity) * self.rho1**(n - self.reservedCapacity) )/ factorial(n)
            )
    def printTask2(self):
        print(f"значение разпределения вероятностей")
        for i in range(len(self.arrayOfProbabilities)):
            print(f"P[{i}]: {self.arrayOfProbabilities[i]}")

        print(f"значение вероятностей блокировка lambda1: {self.probabilityOfBlockingFirstType}")
        print(f"значение вероятностей блокировка lambda2: {self.probabilityOfBlockingSecondType}")
        print(f"значение среднего числа заявок: {self.averageRequestServerd}")                

    def drawTask3(self):
        y = []
        for i in range(int(self.arrival_rate_1)):
            model = IncompleteDualErlangModel(
                self.Capacity, 
                self.reservedCapacity, 
                i, 
                self.arrival_rate_2, 
                self.u 
                )
            
            y.append(model.probabilityOfBlockingFirstType)
        
        plt.figure(figsize=(10,5))
        plt.bar(range(int(self.arrival_rate_1)), y)
        plt.title("график зависимости вероятности блокировки от интенсивности предложенной нагрузки, создаваемой запросами первого типа")
        plt.xlabel("интенсивность поступления запросов на предоставление услуги 1")
        plt.ylabel("вероятность блокировки")
        plt.show()

    def drawTask4(self):
        step = 5
        y = []
        for i in range(0,101,step):
            increment_factor = i/100
            model = IncompleteDualErlangModel(
                self.Capacity, 
                self.reservedCapacity, 
                self.arrival_rate_1*increment_factor, 
                self.arrival_rate_2*increment_factor, 
                self.u 
                )
            
            y.append(model.probabilityOfBlockingFirstType)
        
        plt.figure(figsize=(10,5))
        plt.bar(range(len(y)), y)
        plt.title("график зависимости вероятности блокировки от интенсивности предложенной нагрузки, создаваемой запросами первого типа")
        plt.xlabel("интенсивность поступления запросов на предоставление услуги 1")
        plt.ylabel("вероятность блокировки")
        plt.show()


if __name__ == "__main__":
    print("лабораторная работа №2")
    print("Неполнодоступная двухсервисная модель Эрланга с одинаковыми")

    print("введите переменные")

    C = int(input("C: "))
    g = int(input("g: "))
    lambda1 = float(input("lambda1: "))
    lambda2 = float(input("lambda2: "))
    u = float(input("u: "))

    model = IncompleteDualErlangModel( C, g, lambda1,  lambda2, u)
    model.printTask2()
    model.drawTask3()
    model.drawTask4()
