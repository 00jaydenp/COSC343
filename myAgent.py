import numpy as np
import matplotlib.pyplot as plt
import csv
import random


playerName = "myAgent"
nPercepts = 75  #This is the number of percepts
nActions = 5    #This is the number of actionss
avgFitData= []

# # Train against random for 5 generations, then against self for 1 generations
trainingSchedule = [('random', 100)]

# # This is the class for your creature/agent

class MyCreature:



    def __init__(self):
        # You should initialise self.chromosome member variable here (whatever you choose it
        # to be - a list/vector/matrix of numbers - and initialise it with some random
        # values

        self.chromosome = []
        self.chromosome = np.random.rand(17)
        self.fitness = 0
        # .
        # .
        # .
        #pass This is just a no-operation statement - replace it with your code

    """
    AgentFunction which maps percepts to actions via chromosomes. 
    Creature Map, Food Map, and Wall Map have their own iterations, and depending on the index of the maps
    an action is mapped to a value of a chromosome.
    """
    def AgentFunction(self, percepts):
        actions = np.zeros(nActions)
        creature_map = percepts[:, :, 0]  # 5x5 map with information about creatures and their size
        food_map = percepts[:, :, 1]  # 5x5 map with information about strawberries
        wall_map = percepts[:, :, 2]

        # You should implement a model here that translates from 'percepts' to 'actions'
        # through 'self.chromosome'.
        #
        # The 'actions' variable must be returned and it must be a 5-dim numpy vector or a
        # list with 5 numbers.
        #
        # The index of the largest numbers in the 'actions' vector/list is the action taken
        # with the following interpretation:
        # 0 - move left
        # 1 - move up
        # 2 - move right
        # 3 - move down
        # 4 - eat
        #
        # Different 'percepts' values should lead to different 'actions'.  This way the agent
        # reacts differently to different situations.
        #
        # Different 'self.chromosome' should lead to different 'actions'.  This way different
        # agents can exhibit different behaviour.

        # .
        # .
        # .
        for row in range(5):
            for col in range(5):
                if food_map[2][2] == 1:
                    actions[4] += self.chromosome[3]/3
                if food_map[row][col] == 1:
                    if row < 2:
                        actions[0] += self.chromosome[0]
                    if row > 2:
                        actions[2] += self.chromosome[1]
                    if col > 2:
                        actions[3] += self.chromosome[2]
                    if col < 2:
                        actions[1] += self.chromosome[4]
                if creature_map[row][col] < 1:
                    if row <= 1:
                        actions[0] += self.chromosome[5]
                    if row >= 3:
                        actions[2] += self.chromosome[6]
                    if col >= 3:
                        actions[3] += self.chromosome[7]
                    if col <= 1:
                        actions[1] += self.chromosome[8]
                if creature_map[row][col] >1:
                    if row <= 1:
                        actions[2] += self.chromosome[13]
                    if row >= 3:
                        actions[0] += self.chromosome[14]
                    if col >= 3:
                        actions[1] += self.chromosome[15]
                    if col <= 1:
                        actions[3] += self.chromosome[16]
                if wall_map[row][col] ==1:
                    if row <= 1:
                        actions[2] += self.chromosome[9]
                    if row >= 3:
                        actions[0] += self.chromosome[10]
                    if col >= 3:
                        actions[1] += self.chromosome[11]
                    if col <= 1:
                        actions[3] += self.chromosome[12]
        return actions

"""
Assigns the new generation of creatures and calculates fitness.
Uses elitism, tournament select and mutation 
"""
def newGeneration(old_population):

#     # This function should return a list of 'new_agents' that is of the same length as the
#     # list of 'old_agents'.  That is, if previous game was played with N agents, the next game
#     # should be played with N agents again.

    # This function should also return average fitness of the old_population
    N = len(old_population)

    # Fitness for all agents
    fitness = np.zeros(N)


    # This loop iterates over your agents in the old population - the purpose of this boiler plate
    # code is to demonstrate how to fetch information from the old_population in order
    # to score fitness of each agent
    for n, creature in enumerate(old_population):
        """
        This is where the fitness is calculated, it first promotes exploration and rewards movement and eating.
        That value is then multiplied by the creature size to the power of a number specified by the amount a
        creature travelled.
        """

        # creature is an instance of MyCreature that you implemented above, therefore you can access any attributes
        # (such as `self.chromosome').  Additionally, the objects has attributes provided by the
        # game enginne:
        #
        # creature.alive - boolean, true if creature is alive at the end of the game
        # creature.turn - turn that the creature lived to (last turn if creature survived the entire game)
        # creature.size - size of the creature
        # creature.strawb_eats - how many strawberries the creature ate
        # creature.enemy_eats - how much energy creature gained from eating enemies
        # creature.squares_visited - how many different squares the creature visited
        # creature.bounces - how many times the creature bounced

        # .
        # .
        # .
        creature.fitness += creature.squares_visited
        creature.fitness += creature.strawb_eats *10
        creature.fitness += creature.enemy_eats *20
        creature.fitness += creature.size
        if creature.alive == False:
            creature.fitness = creature.fitness/1.3

        # Add the fitness to the population fitness list.

        # Give the fitness attribute of the individual creature its fitness value.
        # This is used for sorting after selection.



        # This fitness functions just considers length of survival.  It's probably not a great fitness
        # function - you might want to use information from other stats as well
        fitness[n] = creature.fitness


    # At this point you should sort the agent according to fitness and create new population
    """
    Here the current or 'old' population is put into a new array, and then that array is sorted in descending order in
    terms of fitness of the creatures.
    """
    population = []
    for creature in old_population:
        population.append(creature)
    population.sort(key=lambda x: x.fitness, reverse=True)  # sort population in descending order of fitness

    length = len(population) #Used to split list in half to get top 50%
    middle_index = length//2
    population= population[:middle_index]

    new_population = list()

    for n in range(N):


        # Create new creature
        # Tournament selection is used to select two parents, and then they are crossed over and mutated
        new_creature = MyCreature()

        # Form of elitism that takes the fittest creature and clones it 3 times
        if n < 3:
            new_creature.chromosome = population[0].chromosome
        else:
            c1,c2 = tournament_selection(population)

            new_creature.chromosome = crossover(c1, c2)
            new_creature.chromosome = mutate(new_creature)



        # Here you should modify the new_creature's chromosome by selecting two parents (based on their
        # fitness) and crossing their chromosome to overwrite new_creature.chromosome

        # Consider implementing elitism, mutation and various other
        # strategies for producing new creature.

        # .
        # .
        # .

        # Add the new agent to the new population
        new_population.append(new_creature)

    # At the end you neet to compute average fitness and return it along with your new population
    avg_fitness = np.mean(fitness)



    avgFitData.append(avg_fitness)

    # Plotting fitness data
    plt.close('all')
    plt.figure()
    plt.xlabel('Epochs')
    plt.ylabel('Average fitness')
    plt.plot(avgFitData)
    plt.show()
    return (new_population, avg_fitness)

"""
Tournament selection, which selects the top 50% of the population,
then from that subset 8 individuals are chosen and the fittest out of them is returned.
"""
def tournament_selection(population):
    duplicate = True
    while duplicate == True:
        parents = random.choices(population, k=5)
        parents = sorted(parents, key=lambda agent: agent.fitness, reverse=True)
        if parents[0] != parents[1]:
            duplicate = False


    return parents[0], parents[1]

"""
Crossover method that implements single point crossover
"""
def crossover(creature1, creature2):
    crosspoint = random.randint(0, 16)
    i = 0
    N = len(creature1.chromosome)
    new_chromosome = np.zeros(N)
    for n in range(N):
        if i < crosspoint:
            new_chromosome[i] = creature1.chromosome[i]
        else:
            new_chromosome[i] = creature2.chromosome[i]
        i += 1
    return new_chromosome

"""
Mutation method that randomly mutates a gene with a value between 0,1
"""
def mutate(creature):
    new_chromosome = creature.chromosome
    if random.randint(0, 100) < 1:
        mutation = random.uniform(0, 1)
        new_chromosome[random.randint(0,16)] = mutation
    return new_chromosome


