import matplotlib.pyplot as plt

def SIR(days_list, susceptible_list, infected_list, recovered_list):
    # Plot the SIR graph
    plt.figure(figsize=(8, 6))
    plt.plot(days_list, susceptible_list, label="Susceptible", color="green")
    plt.plot(days_list, infected_list, label="Infected", color="red")
    plt.plot(days_list, recovered_list, label="Recovered", color="grey")

    plt.title("SIR Model")
    plt.xlabel('Days')
    plt.ylabel('Population')
    plt.legend()
    plt.grid(True)

    plt.show()