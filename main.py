import sys

from population import Population
import matplotlib.pyplot as plt


def on_close(event):
    sys.exit()


if __name__ == '__main__':
    plt.ion()
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.canvas.mpl_connect('close_event', on_close)
    iterations = 1000
    mutation_rate = 0.02
    nr_individuals = 500
    pop = Population(2, mutation_rate, nr_individuals)
    for i in range(iterations):
        pop.fitness_calculation()
        pop.selection()
        pop.crossing()

        fig.clf()
        fig.add_axes(ax1)
        fig.add_axes(ax2)

        ax1.axis("off")
        ax1.title.set_text("Global Best=" + str(round((1 / pop.global_best), 3)))
        ax1.scatter(*zip(*pop.global_best_route), color='red')
        ax1.plot(*zip(*pop.global_best_route))

        ax2.axis("off")
        ax2.title.set_text("Current Best=" + str(round((1 / pop.current_best), 3)))
        ax2.scatter(*zip(*pop.current_best_route), color='red')
        ax2.plot(*zip(*pop.current_best_route))

        fig.text(0.2, 0.1, 'Iteration ' + str(i + 1) + '/' + str(iterations), horizontalalignment='center',
                 verticalalignment='center')

        fig.canvas.draw()
        fig.canvas.flush_events()

    plt.show(block=True)
    print('f')
