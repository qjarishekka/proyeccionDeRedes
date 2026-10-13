from task2 import IncompleteDualErlangModel

model = IncompleteDualErlangModel( 7,3, 20,  30,5)

# print(model.P0)
# for i in range(len(model.arrayOfProbabilities)):
#     print(f"probability P[{i}]: {model.arrayOfProbabilities[i]}")

# print(model.probabilityOfBlockingFirstType)
# print(model.probabilityOfBlockingSecondType)
# print(model.averageRequestServerd)
# print(sum(model.arrayOfProbabilities))
model.printTask2()
model.drawTask3()
model.drawTask4()




# p = model.arrayOfProbabilities[2:4]

# for i in p:
#     print(i)

