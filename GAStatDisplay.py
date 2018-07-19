import matplotlib.pyplot as plt


#  Displays a quick graph of the best Member and Average Fitness Data - because excel is bad
def graph_data(best_data, average_data):
    plt.figure()
    plt.title('Genetic Algorithm Results')
    plt.plot(best_data, label='Fitness of the Best Member')
    plt.plot(average_data, label='Average Fitness of Population')
    plt.legend()
    plt.ylabel('Fitness Values')
    plt.xlabel('Generation')
    plt.show()
