import ciw

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