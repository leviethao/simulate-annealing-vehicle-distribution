from anneal import SimAnneal
import matplotlib.pyplot as plt
import random
import drawing

cards = []
vehicles = []
with open("data2.txt", "r") as f:
    ncard = int(f.readline().replace("\n", ""))
    for i in range(ncard):
        line = f.readline()
        line = [float(x.replace("\n", "")) for x in line.split(" ")]
        cards.append(line)
    print("cards = ", cards)
    
    nvehicle = int(f.readline().replace("\n", ""))
    for i in range(nvehicle):
        line = f.readline()
        line = [float(x.replace("\n", "")) for x in line.split(" ")]
        vehicles.append(line)
    print("vehicles = ", vehicles)

if __name__ == "__main__":
    # coords = [[random.uniform(-1000, 1000), random.uniform(-1000, 1000)] for i in range(100)]
    sa = SimAnneal(cards, vehicles, stopping_iter=5000)
    if sa.anneal() == True:
        # sa.visualize_routes()
        drawing.draw_simulate(sa.cards, sa.vehicles, sa.best_solution)
        sa.plot_learning()
