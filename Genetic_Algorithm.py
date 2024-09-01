################################################################################
#                                                                              #
#	HARSH AGRAWAL                                                                #    
#	Genetic Algorithm                                                            #
#	PYTHON 3.11.0                                                                #
#                                                                              #
################################################################################

import random
import numpy as np
import matplotlib.pyplot as plt

# Define parameters
num_generations = 50
population_size = 100
search_space_size = (3000, 3000)
num_service_types = 3
num_instances_per_type = 1000
max_cost = 1000  # Assuming a maximum cost for normalization
max_time = 15  # Assuming a maximum time (minutes)
min_time = 7 


def generate_service_instance():
  service_type = random.randint(1, num_service_types)  # Assuming multiple service types
  x = random.randint(0, search_space_size[0] - 1)  # Random X coordinate within search space
  y = random.randint(0, search_space_size[1] - 1)  # Random Y coordinate within search space
  cost = random.randint(1, max_cost)  # Random cost within a defined range
  time = random.randint(7,15)# Random response time
  fitness = (cost / max_cost) + (time / max_time)
  return {"type": service_type, "location": (x, y), "cost": cost, "time": time , "fitness" : fitness}

# Generate service instances (replace with actual data loading)
instances = [generate_service_instance() for _ in range(num_service_types * num_instances_per_type)]


def generate_chromosome():
  chromosome = ""
  for _ in range(len(search_space_size) * 2):  # 2 bits per dimension (X, Y)
    chromosome += str(random.randint(0, 1))
  return chromosome

def decode_chromosome(chromosome):
  x_bits, y_bits = chromosome[:len(chromosome)//2], chromosome[len(chromosome)//2:]
  x = int(x_bits, 2)
  y = int(y_bits, 2)
  return (x, y)

def calculate_fitness(location):
  global instances
  total_fitness = 0
  for service_type in range(1, num_service_types + 1):
    # Find instances of the current service type within the search space centered at the particle's position
    # (Replace with a more efficient spatial search if needed)
    service_instances = [instance for instance in instances if instance["type"] == service_type and
                         abs(instance["location"][0] - location[0]) <= search_space_size[0]  and
                         abs(instance["location"][1] - location[1]) <= search_space_size[1] ]
    if service_instances:
      # Select the instance with the highest fitness (assuming higher fitness is better)
      best_instance = max(service_instances, key=lambda i: i["fitness"])
      total_fitness += best_instance["cost"] + max_time
  return total_fitness

def roulette_wheel_selection(population):
  # Calculate total fitness
  total_fitness = sum(calculate_fitness(decode_chromosome(chromosome)) for chromosome in population)
  # Create probability wheel slices
  probability_wheel = []
  for chromosome in population:
    fitness = calculate_fitness(decode_chromosome(chromosome))
    probability = fitness / total_fitness
    probability_wheel.append(probability)
  # Perform selection (spin the wheel)
  selected_parents = []
  for _ in range(population_size):
    spin_value = random.random()
    current_sum = 0
    for i in range(len(probability_wheel)):
      current_sum += probability_wheel[i]
      if current_sum >= spin_value:
        selected_parents.append(population[i])
        break
  return selected_parents

def crossover(parent1, parent2):
  crossover_point = random.randint(1, len(parent1) - 2)
  offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
  offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
  return offspring1, offspring2

def mutation(chromosome, mutation_rate):
  new_chromosome = chromosome
  for i in range(len(chromosome)):
    if random.random() < mutation_rate:
      new_chromosome = new_chromosome[:i] + str(1 - int(chromosome[i])) + new_chromosome[i+1:]
  return new_chromosome

def genetic_algorithm():
  population = [generate_chromosome() for _ in range(population_size)]
  fitness_history = []
  for generation in range(num_generations):
    # Selection (Roulette Wheel Selection)
    parents = roulette_wheel_selection(population)
    # Crossover
    offspring = []
    for i in range(0, population_size, 2):
      offspring.extend(crossover(parents[i], parents[i + 1]))
    # Mutation
    offspring_with_mutation = []
    for chromosome in offspring:
      offspring_with_mutation.append(mutation(chromosome, mutation_rate=0.01))  # Example mutation rate
    # Combine and selection (e.g., elitism)
    new_population = roulette_wheel_selection(population + offspring_with_mutation)  # Replace with appropriate selection here (e.g., elitism)
    population = new_population
    
    # Find best solution
    best_chromosome = max(population, key=lambda c: calculate_fitness(decode_chromosome(c)))
    best_location = decode_chromosome(best_chromosome)
    best_fitness = calculate_fitness(best_location)
    fitness_history.append(best_fitness)
    print(best_fitness)

  return best_location, best_fitness, fitness_history

# Run GA and print results
best_location, best_fitness , fitness_history = genetic_algorithm()
print("Best service instance location:", best_location)
print("Best fitness (lower is better):", best_fitness)

# Plotting the convergence fitness over generations
plt.plot(fitness_history)
plt.title("Convergence of Fitness Over Generations")
plt.xlabel("Generation")
plt.ylabel("Fitness (lower is better)")
plt.show()