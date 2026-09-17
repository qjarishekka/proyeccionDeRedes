
from math import factorial
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import argparse

def functionPn(rho1, rho2, C, n):
    summa = 0
    for i in range(C+1):
        summa += (rho1 + rho2) ** i / factorial(i)

    return (rho1 + rho2) ** n / factorial(n) / summa

def netSimulator(data):

    C = data["C"]
    L1 = data["L1"]
    L2 = data["L2"]
    U = data["U"]

    rho1 = L1/U
    rho2 = L2/U
    E = 0
    aceptedQuerysAverage = 0
    Pdistribution = []
    for i in range(C+1):

        Pn = functionPn(rho1, rho2, C, i)
        Pdistribution.append(Pn)
        aceptedQuerysAverage += i * Pn

        if i == C:
            E = Pn
            B = (((L1/(L1+L2)) * E) , ((L2/(L1 + L2)) *E))
        

    return E, Pdistribution, aceptedQuerysAverage, B

def drawPlots( data:pd.DataFrame, column:str, type:int):


    titles = {
    1:"график зависимости вероятности блокировки\n от интенсивности поступления запросов на обслуживание.",
    2:"график зависимости среднего числа обслуживаемых\n запросов от интенсивности поступления запросов на предоставление услуги."
    }

    labelsY = {
       1: "вероятности блокировки",
        2:"среднего числа обслуживаемых запросов"
    }
    labelsX = {
        1:"интенсивности поступления запросов на обслуживание.",
        2:"интенсивности поступления запросов на предоставление услуги."
    }

    
    plt.figure(figsize=(10, 5))
    plt.bar(data["L"] , data[ column] )
    plt.title( titles[type] )
    plt.xlabel(labelsX[type] )
    plt.ylabel(labelsY[type])
    #plt.text(5, 0.1, f"E = {E}", fontsize=10, verticalalignment='top', bbox=estilo_recuadro)
    #plt.text(5, 0.05, f"Average Accepted Queries = {aceptedQuerysAverage}", fontsize=10, verticalalignment='top', bbox=estilo_recuadro)
    plt.show()






#E, Pdistribution, aceptedQuerysAverage = netSimulator(10, 5, 3, 20)

print("программа моделирования насыщения сети")

C = 0
while(C <= 0):
    C = int( input("введите значение C\n"))
    if (C <=0):
        print("C должно быт больше 0")

L1 = 2
while(L1>1 or L1<=0):
    L1 = float(input("введите соотношение между L1 и L2\nнапримет 0.2\n"))
    if L1 > 1: 
        print("неправильное значение")

U = 0
while(U <= 0):
    U = float(input("введите здачение U\n"))
    if(U == 0):
        print("U должно быт больше 0")

numberOfSimulation = int(input("введите максимальный L\n"))


data = {
    "simulation_N": [i + 1 for i in range(numberOfSimulation)],
    "L1": [ (i+1)*L1 for i in range(numberOfSimulation) ],
    "L2": [ (i+1)*(1-L1) for i in range(numberOfSimulation)],
    "C": np.full(numberOfSimulation,C),
    "U": np.full(numberOfSimulation, U ),
    "E": np.zeros(numberOfSimulation),
    "N": np.zeros(numberOfSimulation),
    "B1":np.zeros(numberOfSimulation),
    "B2":np.zeros(numberOfSimulation)

}

data["L"] = np.array(data["L1"]) + np.array(data["L2"])
Pdistributions = []

for i in range(numberOfSimulation):
    simulation_data = {
        "C": data["C"][i],
        "L1": data["L1"][i],
        "L2": data["L2"][i],
        "U": data["U"][i]
    }

    E, Pdistribution, aceptedQuerysAverage, B = netSimulator(simulation_data)

    data["E"][i] = E
    data["N"][i] = aceptedQuerysAverage
    data["B1"][i] = B[0]
    data["B2"][i] = B[1]
    Pdistributions.append (Pdistribution)
    


dt = pd.DataFrame(data)
Pdistributions = pd.DataFrame(Pdistributions)



print("data:\n",dt)
print("\nPn:",Pdistributions)

drawPlots(dt, "E",type=1)
drawPlots(dt,"N", type=2)


