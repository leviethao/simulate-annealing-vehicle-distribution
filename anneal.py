import math
import random
import visualize_tsp
import matplotlib.pyplot as plt
from random import sample


class SimAnneal(object):
    def __init__(self, cards, vehicles, T=-1, alpha=-1, stopping_T=-1, stopping_iter=-1):
        self.cards = cards
        self.vehicles = vehicles
        self.N = len(vehicles)
        self.T = math.sqrt(self.N) if T == -1 else T
        self.T_save = self.T  # save inital T to reset if batch annealing is used
        self.alpha = 0.995 if alpha == -1 else alpha
        self.stopping_temperature = 1e-8 if stopping_T == -1 else stopping_T
        self.stopping_iter = 100000 if stopping_iter == -1 else stopping_iter
        self.iteration = 1

        self.nodes = [i for i in range(self.N)]

        self.best_solution = None # format of [[card, vehicle]]
        self.best_fitness = float("Inf")
        self.fitness_list = []

    def calc_v_of_cards(self):
        v = 0
        for card in self.cards:
            v += card[4]
        return v
    
    def get_solution(self):
        # shuffle nodes
        shuffle = list(self.nodes)
        random.shuffle(shuffle)
        # print("shuffle: ", shuffle)

        solution = [] # [[card, vehicle]]
        v = 0
        for icard in range(len(self.cards)):
            selected_node = None
            for node in shuffle:
                # if v of vehicle < v of card => continue        
                if self.vehicles[node][2] >= self.cards[icard][4]:
                    solution.append([icard, node])
                    selected_node = node
                    v += self.vehicles[node][2]
                    break
            if selected_node == None:
                return None # solution not found
            shuffle.remove(selected_node)
        return solution
    
    def ensure_get_solution(self):
        n_loop = 1000
        for i in range(n_loop):
            solution = self.get_solution()
            if (solution != None):
                return solution
        return None

    def initial_solution(self):
        """
        get an initial solution random from nodes.
        """
        solution = self.ensure_get_solution()
        # print("init solution: ", solution)

        if solution == None:
            return None, None

        cur_fit = self.fitness(solution)
        if cur_fit < self.best_fitness:  # If best found so far, update best fitness
            self.best_fitness = cur_fit
            self.best_solution = solution
        self.fitness_list.append(cur_fit)
        return solution, cur_fit

    def dist(self, icard, ivehicle):
        """
        Euclidean distance between two nodes.
        """
        card, vehicle = self.cards[icard], self.vehicles[ivehicle]
        pickup_dist = math.sqrt((card[0] - vehicle[0]) ** 2 + (card[1] - vehicle[1]) ** 2)
        delivery_dist = math.sqrt((card[0] - card[2]) ** 2 + (card[1] - card[3]) ** 2)
        dist = pickup_dist + delivery_dist
        return dist

    def diff_v (self, icard, ivehicle):
        card, vehicle = self.cards[icard], self.vehicles[ivehicle]
        return vehicle[2] - card[4]

    def fitness(self, solution):
        """
        Total cost of the current solution.
        """
        cur_fit = total_dist = total_v_diff = 0 
        for s in solution:
            total_dist += self.dist(s[0], s[1]) # s[0] is index of card, s[1] is index of vehicle
            total_v_diff += self.diff_v(s[0], s[1])
        
        # print("total_dist = ", total_dist, "; total_v_diff = ", total_v_diff)
        cur_fit = 0.7 * total_dist + 0.3 * total_v_diff
        return cur_fit

    def p_accept(self, candidate_fitness):
        """
        Probability of accepting if the candidate is worse than current.
        Depends on the current temperature and difference between candidate and current.
        """
        return math.exp(-abs(candidate_fitness - self.cur_fitness) / self.T)

    def accept(self, candidate):
        """
        Accept with probability 1 if candidate is better than current.
        Accept with probabilty p_accept(..) if candidate is worse.
        """
        candidate_fitness = self.fitness(candidate)
        if candidate_fitness < self.cur_fitness:
            self.cur_fitness, self.cur_solution = candidate_fitness, candidate
            if candidate_fitness < self.best_fitness:
                self.best_fitness, self.best_solution = candidate_fitness, candidate
        else:
            if random.random() < self.p_accept(candidate_fitness):
                self.cur_fitness, self.cur_solution = candidate_fitness, candidate

    def anneal(self):
        """
        Execute simulated annealing algorithm.
        """
        # Initialize with the greedy solution.
        self.cur_solution, self.cur_fitness = self.initial_solution()
        if self.cur_solution == None:
            print("Solution not found!")
            return False # Solution not found

        print("Starting annealing.")
        while self.T >= self.stopping_temperature and self.iteration < self.stopping_iter:
            candidate = self.ensure_get_solution()
            self.accept(candidate)
            self.T *= self.alpha
            self.iteration += 1

            self.fitness_list.append(self.cur_fitness)

        print("Best fitness obtained: ", self.best_fitness)
        print("Best solution: ", self.best_solution)
        improvement = 100 * (self.fitness_list[0] - self.best_fitness) / (self.fitness_list[0])
        print(f"Improvement over random heuristic: {improvement : .2f}%")
        return True # Solution found

    def batch_anneal(self, times=10):
        """
        Execute simulated annealing algorithm `times` times, with random initial solutions.
        """
        for i in range(1, times + 1):
            print(f"Iteration {i}/{times} -------------------------------")
            self.T = self.T_save
            self.iteration = 1
            self.cur_solution, self.cur_fitness = self.initial_solution()
            self.anneal()

    # def visualize_routes(self):
    #     """
    #     Visualize the TSP route with matplotlib.
    #     """
    #     self.cur_solution, self.cur_fitness = self.initial_solution()
    #     visualize_tsp.plotTSP([self.cur_solution], self.coords)

    def plot_learning(self):
        """
        Plot the fitness through iterations.
        """
        plt.plot([i for i in range(len(self.fitness_list))], self.fitness_list)
        plt.ylabel("Fitness")
        plt.xlabel("Iteration")
        plt.show()
