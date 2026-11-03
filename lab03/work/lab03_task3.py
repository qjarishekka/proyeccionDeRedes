import matplotlib.pyplot as plt


def grafic_task3_results(probabilities, K, N1, N2, T1, T2, E1, E2):
    plt.figure(figsize=(12, 8))
    plt.subplot(2, 2, 1)
    plt.title("Probabilities p(n1, n2)")
    plt.xlabel("n1")
    plt.ylabel("n2")
    for i in range(K + 1):
        for j in range(K - i + 1):
            plt.text(i, j, f"{probabilities[(i, j)]:.4f}", ha='center', va='center')
    plt.xlim(-0.5, K + 0.5)
    plt.ylim(-0.5, K + 0.5)
    plt.grid()

    plt.subplot(2, 2, 2)
    plt.title("Average number of requests N_i")
    plt.bar(["N1", "N2"], [N1, N2])
    plt.ylabel("Average number of requests")

    plt.subplot(2, 2, 3)
    plt.title("Average time T_i")
    plt.bar(["T1", "T2"], [T1, T2])
    plt.ylabel("Average time")

    plt.subplot(2, 2, 4)
    plt.title("Blocking probabilities E_i")
    plt.bar(["E1", "E2"], [E1, E2])
    plt.ylabel("Blocking probabilities")

    plt.tight_layout()
    plt.show()
