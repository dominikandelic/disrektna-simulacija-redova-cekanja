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

average_waits_business = []
average_waits_civilian = []

for trial in range(500):
    ciw.seed(trial)
    Q = ciw.Simulation(N)
    Q.simulate_until_max_time(480)
    recs = Q.get_all_records()
    waits_business = [r.waiting_time for r in recs if r.customer_class == 0]
    waits_civilian = [r.waiting_time for r in recs if r.customer_class == 1]
    mean_wait_business = sum(waits_business) / len(waits_business)
    mean_wait_civilian = sum(waits_civilian) / len(waits_civilian)
    average_waits_business.append(mean_wait_business)
    average_waits_civilian.append(mean_wait_civilian)


average_mean_wait_business = sum(average_waits_business) / len(average_waits_business)
average_mean_wait_civilian = sum(average_waits_civilian) / len(average_waits_civilian)

fig, ax = plt.subplots()
ax.set_title('Distribucija prosječnih vremena čekanja (u 500 iteracija)')
ax.set_xlabel("Vrijeme čekanja (min)")
ax.set_ylabel("Frekvencija pojavljivanja (u broju iteracija)")

ax.hist(average_waits_business, label="Prosječno vrijeme čekanja za poslovne klijente", alpha = 0.5)
ax.hist(average_waits_civilian, label="Prosječno vrijeme čekanja za građanstvo", alpha = 0.5)
ax.legend()

plt.show()

print("Prosječno vrijeme čekanja za poslovne korisnike: " + str(round(average_mean_wait_business, 2)) + "minuta")
print("Prosječno vrijeme čekanja za građanstvo: " + str(round(average_mean_wait_civilian, 2)) + "minuta")
