import ciw
import matplotlib.pyplot as plt

class CustomRouting(ciw.Node):
    def next_node(self, ind):
        if ind.customer_class == 1:
            n2 = self.simulation.nodes[2].number_of_individuals
            n3 = self.simulation.nodes[3].number_of_individuals
            if n2 < n3:
                return self.simulation.nodes[2]
            elif n3 < n2:
                return self.simulation.nodes[3]
            return ciw.random_choice([self.simulation.nodes[2], self.simulation.nodes[3]])
        else:
            return self.simulation.nodes[3]

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
              'Class 1': [[0.0, 0.5, 0.5],
                          [0.0, 0.0, 0.0],
                          [0.0, 0.0, 0.0]]},
     number_of_servers=[1, 2, 1],
 )

average_utilization_node_1 = []
average_utilization_node_2 = []
average_utilization_node_3 = []
mean_arrived = []
mean_exited = []
average_waits_business = []
average_waits_civilian = []
max_waiting_times = []


for trial in range(500):
    ciw.seed(trial)
    Q = ciw.Simulation(N, tracker=ciw.trackers.NodePopulation(), node_class=[CustomRouting, ciw.Node, ciw.Node])
    Q.simulate_until_max_time(480)
    recs = Q.get_all_records()
    node_1_queue_utilization = Q.transitive_nodes[0].server_utilisation
    node_2_queue_utilization = Q.transitive_nodes[1].server_utilisation
    node_3_queue_utilization = Q.transitive_nodes[2].server_utilisation
    average_utilization_node_1.append(node_1_queue_utilization)
    average_utilization_node_2.append(node_2_queue_utilization)
    average_utilization_node_3.append(node_3_queue_utilization)
    waits_business = [r.waiting_time for r in recs if r.customer_class == 0]
    waits_civilian = [r.waiting_time for r in recs if r.customer_class == 1]
    mean_wait_business = sum(waits_business) / len(waits_business)
    mean_wait_civilian = sum(waits_civilian) / len(waits_civilian)
    average_waits_business.append(mean_wait_business)
    average_waits_civilian.append(mean_wait_civilian)
    mean_arrived.append(Q.nodes[0].number_of_individuals)
    mean_exited.append(Q.nodes[-1].number_of_individuals)
    max_waiting_time_per_iteration = max([r.waiting_time for r in recs])
    max_waiting_times.append(max_waiting_time_per_iteration)


print("Najduže vrijeme čekanja: " + str(round(max(max_waiting_times), 2)) + "min")



average__mean_arrived = sum(mean_arrived) / len(mean_arrived)
average__mean_exited = sum(mean_exited) / len(mean_exited)

print("Prosječno ušlo klijenata u sustav: " + str(round(average__mean_arrived)))
print("Prosječno izašlo klijenata iz sustava: " + str(round(average__mean_exited)))


average_mean_wait_business = sum(average_waits_business) / len(average_waits_business)
average_mean_wait_civilian = sum(average_waits_civilian) / len(average_waits_civilian)

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

print("Prosječno vrijeme čekanja za poslovne korisnike: " + str(round(average_mean_wait_business, 2)) + "minuta")
print("Prosječno vrijeme čekanja za građanstvo: " + str(round(average_mean_wait_civilian, 2)) + "minuta")
