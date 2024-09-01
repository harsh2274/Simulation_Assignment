################################################################################
#                                                                              #
#	HARSH AGRAWAL                                                                #    
#	Simulated Annealing                                                          #
#	PYTHON 3.8.0                                                                 #
#                                                                              #
################################################################################

import random
import math
import numpy as np
import matplotlib.pyplot as plt  # Importing for plotting purposes
  
# Define parameters
search_space_size = (3000, 3000)
num_service_types = 3
num_instances_per_type = 1000  # Assuming pre-loaded data (replace with actual data access)
max_cost = 1000  # Assuming a maximum cost for normalization
max_time = 15  # Assuming a maximum time (minutes)
min_time = 7  # Assuming a minimum time (minutes)



def generate_service_instance():
  service_type = random.randint(1, num_service_types)
  location = (np.random.randint(0, search_space_size[0]), np.random.randint(0, search_space_size[1]))
  cost = np.random.randint(1, max_cost + 1)
  time = np.random.rand() * (max_time - 7) + 7  # Time between 7 and 15 minutes
  fitness = (cost / max_cost) + (time / max_time)
  return {"type": service_type, "location": location, "cost": cost, "time": time, "fitness": fitness}  

# Service instance data (replace with actual data loading)
# Assuming pre-loaded data exists
instances = [generate_service_instance() for _ in range(num_service_types * num_instances_per_type)]

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
    print(total_fitness)
  return total_fitness

def simulated_annealing(initial_temperature, cooling_rate, max_iterations):
  # Generate random initial location
  current_location = (random.randint(0, search_space_size[0] - 1), random.randint(0, search_space_size[1] - 1))
  current_fitness = calculate_fitness(current_location)
  best_location = current_location
  best_fitness = current_fitness
  temperature = initial_temperature

  # List to store fitness values for convergence tracking
  fitness_history = [best_fitness]

  for iteration in range(max_iterations):
    # Generate a random neighbor location within a small search area
    new_location = (
        current_location[0] + random.randint(-10, 10),
        current_location[1] + random.randint(-10, 10)
    )
    # Ensure new location stays within search space boundaries
    new_location = (
        max(0, min(new_location[0], search_space_size[0] - 1)),
        max(0, min(new_location[1], search_space_size[1] - 1))
    )
    new_fitness = calculate_fitness(new_location)

    # Metropolis acceptance criterion
    delta_fitness = new_fitness - current_fitness
    if delta_fitness > 0 or random.random() < math.exp(delta_fitness / temperature) :  # Always accept improvement
      current_location = new_location
      current_fitness = new_fitness
    # else:
    #   # Accept worse solutions with a probability based on temperature
    #   p = math.exp(delta_fitness / temperature)
    #   if random.random() < p:
    #     current_location = new_location
    #     current_fitness = new_fitness

    # Update best solution
    if current_fitness < best_fitness:  # Minimize fitness
      best_location = current_location
      best_fitness = current_fitness
    
    fitness_history.append(best_fitness)  # Track fitness

    # Cool down temperature
    temperature *= cooling_rate

  return best_location, best_fitness, fitness_history


# Run Simulated Annealing
initial_temperature = 100
cooling_rate = 0.95
max_iterations = 50
best_location, best_fitness, fitness_history = simulated_annealing(initial_temperature, cooling_rate, max_iterations)

print("Best service instance location:", best_location)
print("Best fitness (lower is better):", best_fitness)

# Plotting the convergence fitness over iterations
plt.plot(fitness_history)
plt.title("Convergence of Fitness Over Iterations")
plt.xlabel("Iteration")
plt.ylabel("Fitness (lower is better)")
plt.show()