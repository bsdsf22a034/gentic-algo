import random
import numpy as np

# Distance matrix example (this should be replaced with your specific distance matrix)
# You can create your own distance matrix for n cities or import it from external sources
distance_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# Parameters
POPULATION_SIZE = 10
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1

# Genetic Algorithm Functions

# Fitness function (inverse of the route distance)
def calculate_fitness(route):
    total_distance = sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
    total_distance += distance_matrix[route[-1]][route[0]]  # Return to the starting city
    return 1 / total_distance  # Higher fitness for shorter routes

# Initialize population (random routes)
def initialize_population(num_cities):
    population = []
    for _ in range(POPULATION_SIZE):
        route = list(range(num_cities))
        random.shuffle(route)
        population.append(route)
    return population

# Selection using tournament selection
def tournament_selection(population, fitness_scores, k=3):
    selected = random.sample(range(len(population)), k)
    selected.sort(key=lambda i: fitness_scores[i], reverse=True)
    return population[selected[0]]

# Crossover (Partially Mapped Crossover - PMX)
def pmx_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    
    # Copy part from first parent
    child[start:end+1] = parent1[start:end+1]

    # Fill remaining positions with second parent
    for i in range(start, end+1):
        if parent2[i] not in child:
            pos = i
            while start <= pos <= end:
                pos = parent2.index(parent1[pos])
            child[pos] = parent2[i]

    for i in range(size):
        if child[i] is None:
            child[i] = parent2[i]

    return child

# Mutation (Swap Mutation)
def mutate(route):
    if random.random() < MUTATION_RATE:
        i, j = random.sample(range(len(route)), 2)
        route[i], route[j] = route[j], route[i]

# Main Genetic Algorithm
def genetic_algorithm(num_cities):
    # Initialize population
    population = initialize_population(num_cities)
    
    for generation in range(NUM_GENERATIONS):
        # Calculate fitness for each route in the population
        fitness_scores = [calculate_fitness(route) for route in population]
        
        # Create new population
        new_population = []
        for _ in range(POPULATION_SIZE // 2):
            # Selection
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            
            # Crossover
            child1 = pmx_crossover(parent1, parent2)
            child2 = pmx_crossover(parent2, parent1)
            
            # Mutation
            mutate(child1)
            mutate(child2)
            
            # Add offspring to new population
            new_population.extend([child1, child2])
        
        # Replace old population with new population
        population = new_population
    
    # Find the best route from the final population
    best_route = max(population, key=calculate_fitness)
    best_distance = 1 / calculate_fitness(best_route)
    
    return best_route, best_distance

# Run Genetic Algorithm
best_route, best_distance = genetic_algorithm(len(distance_matrix))
print("Best Route:", best_route)
print("Best Distance:", best_distance)
