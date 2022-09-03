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

average_utilization_node_1 = []
average_utilization_node_2 = []
average_utilization_node_3 = []

for trial in range(500):
    ciw.seed(trial)
    Q = ciw.Simulation(N)
    Q.simulate_until_max_time(480)
    recs = Q.get_all_records()
    node_1_queue_utilization = Q.transitive_nodes[0].server_utilisation
    node_2_queue_utilization = Q.transitive_nodes[1].server_utilisation
    node_3_queue_utilization = Q.transitive_nodes[2].server_utilisation
    average_utilization_node_1.append(node_1_queue_utilization)
    average_utilization_node_2.append(node_2_queue_utilization)
    average_utilization_node_3.append(node_3_queue_utilization)

average_mean_utilization_node_1 = sum(average_utilization_node_1) / len(average_utilization_node_1)
average_mean_utilization_node_2 = sum(average_utilization_node_2) / len(average_utilization_node_2)
average_mean_utilization_node_3 = sum(average_utilization_node_3) / len(average_utilization_node_3)

fig, ax = plt.subplots()
ax.set_title('Distribucija iskorištenosti čvorova (u 500 iteracija)')
ax.set_xlabel("Iskorištenost čvora")
ax.set_ylabel("Frekvencija pojavljivanja (u broju iteracija)")

ax.hist(average_utilization_node_1, label="Prosječna iskorištenost čvora 1", alpha = 0.5)
ax.hist(average_utilization_node_2, label="Prosječna iskorištenost čvora 2", alpha = 0.5)
ax.hist(average_utilization_node_3, label="Prosječna iskorištenost čvora 3", alpha = 0.5)
ax.legend()

plt.show()

print("Prosječna iskorištenost čvora 1: " + str(round(average_mean_utilization_node_1, 4) * 100) + "%")
print("Prosječna iskorištenost čvora 2: " + str(round(average_mean_utilization_node_2, 4) * 100) + "%")
print("Prosječna iskorištenost čvora 3: " + str(round(average_mean_utilization_node_3, 4) * 100) + "%")