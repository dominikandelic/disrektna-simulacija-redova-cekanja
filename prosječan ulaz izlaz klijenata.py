import ciw
import matplotlib.pyplot as plt

N = ciw.create_network(
     arrival_distributions={'Class 0': [ciw.dists.Exponential(rate=0.033),
                                        ciw.dists.NoArrivals(),
                                        ciw.dists.NoArrivals()],
                            'Class 1': [ciw.dists.Exponential(rate=0.2),
                                        ciw.dists.NoArrivals(),
                                        ciw.dists.NoArrivals()]},
     service_distributions={'Class 0': [ciw.dists.Exponential(rate=1.0),
                                        ciw.dists.Deterministic(value=0.0),
                                        ciw.dists.Exponential(rate=0.033)],
                            'Class 1': [ciw.dists.Exponential(rate=1.0),
                                        ciw.dists.Exponential(rate=0.067),
                                        ciw.dists.Deterministic(value=0.0)]},
     routing={'Class 0': [[0.0, 0.0, 1.0],
                          [0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]],
              'Class 1': [[0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]]},
     number_of_servers=[1, 2, 1],
 )

mean_arrived = []
mean_exited = []

for trial in range(500):
    ciw.seed(trial)
    Q = ciw.Simulation(N)
    Q.simulate_until_max_time(480)
    mean_arrived.append(Q.nodes[0].number_of_individuals)
    mean_exited.append(Q.nodes[-1].number_of_individuals)


average__mean_arrived = sum(mean_arrived) / len(mean_arrived)
average__mean_exited = sum(mean_exited) / len(mean_exited)

print("Prosječno ušlo klijenata u sustav: " + str(round(average__mean_arrived)))
print("Prosječno izašlo klijenata iz sustava: " + str(round(average__mean_exited)))