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
     number_of_servers=[1, 3, 1],
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
    Q = ciw.Simulation(N)
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


print("Najdu??e vrijeme ??ekanja: " + str(round(max(max_waiting_times), 2)) + "min")



average__mean_arrived = sum(mean_arrived) / len(mean_arrived)
average__mean_exited = sum(mean_exited) / len(mean_exited)

print("Prosje??no u??lo klijenata u sustav: " + str(round(average__mean_arrived)))
print("Prosje??no iza??lo klijenata iz sustava: " + str(round(average__mean_exited)))


average_mean_wait_business = sum(average_waits_business) / len(average_waits_business)
average_mean_wait_civilian = sum(average_waits_civilian) / len(average_waits_civilian)

average_mean_utilization_node_1 = sum(average_utilization_node_1) / len(average_utilization_node_1)
average_mean_utilization_node_2 = sum(average_utilization_node_2) / len(average_utilization_node_2)
average_mean_utilization_node_3 = sum(average_utilization_node_3) / len(average_utilization_node_3)

fig, ax = plt.subplots()
ax.set_title('Distribucija iskori??tenosti ??vorova (u 500 iteracija)')
ax.set_xlabel("Iskori??tenost ??vora")
ax.set_ylabel("Frekvencija pojavljivanja (u broju iteracija)")

ax.hist(average_utilization_node_1, label="Prosje??na iskori??tenost ??vora 1", alpha = 0.5)
ax.hist(average_utilization_node_2, label="Prosje??na iskori??tenost ??vora 2", alpha = 0.5)
ax.hist(average_utilization_node_3, label="Prosje??na iskori??tenost ??vora 3", alpha = 0.5)
ax.legend()

plt.show()

print("Prosje??na iskori??tenost ??vora 1: " + str(round(average_mean_utilization_node_1, 4) * 100) + "%")
print("Prosje??na iskori??tenost ??vora 2: " + str(round(average_mean_utilization_node_2, 4) * 100) + "%")
print("Prosje??na iskori??tenost ??vora 3: " + str(round(average_mean_utilization_node_3, 4) * 100) + "%")

print("Prosje??no vrijeme ??ekanja za poslovne korisnike: " + str(round(average_mean_wait_business, 2)) + "minuta")
print("Prosje??no vrijeme ??ekanja za gra??anstvo: " + str(round(average_mean_wait_civilian, 2)) + "minuta")
