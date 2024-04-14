import random
import numpy as np
from tkinter import messagebox

#define class particle

class Particle :
    def __init__ (self,position) :
        self.position = position
        self.velocity = np.zeros_like(position)
        self.best_position = position 
        self.best_fitness = float ('inf')

def PSO(ObjF,Pop_Size,D,MaxT):
    swarn_best_position = None 
    swarn_best_fitness = float("inf")
    particles = []

    #position initialization 
    for itr in range(Pop_Size) :
        position = np.random.uniform(0,300,D)
        particle = Particle(position)
        particles.append(particle)

    #fitness update 
    fitness = ObjF(position)
    
    if fitness < swarn_best_fitness :
        swarn_best_fitness = fitness
        swarn_best_position = position 

        particle.best_position = position
        particle.best_fitness = fitness

    #PSO Main Loop 

    for itr in range(MaxT):
        for particle in particles : 
            #update velocity  
            w = 0.8 
            c1 = 1.2 
            c2 = 1.2 

            r1 = random.random()
            r2 = random.random()

            #velocity calculation
            particle.velocity = (w*particle.velocity+c1*r1*(particle.best_position-particle.position)+c2*r2*(swarn_best_position-particle.position))
            
            #new position
            new_position = particle.position + particle.velocity
            particle.position += particle.velocity

            #Evaluate Fitness 
            fitness = ObjF(particle.position)

            #Update PBest
            if fitness < particle.best_fitness : 

                particle.best_position = particle.position
                particle.best_fitness = fitness

            #Update GBest 
            if fitness < swarn_best_fitness:
                swarn_best_fitness = fitness
                swarn_best_position = particle.position

    return swarn_best_position , swarn_best_fitness

# Function to generate a random service instance
def generate_service_instance():
  service_type = random.randint(1, num_service_types)
  location = (np.random.randint(0, search_space_size[0]), np.random.randint(0, search_space_size[1]))
  cost = np.random.randint(1, max_cost + 1)
  time = np.random.rand() * (max_time - 7) + 7  # Time between 7 and 15 minutes
  fitness = (cost / max_cost) + (time / max_time)
  return {"type": service_type, "location": location, "cost": cost, "time": time, "fitness": fitness}
         
# Function to calculate particle fitness (Approach 2: Finding highest fitness in search space area)
def calculate_particle_fitness(position):
  # Assuming service instance data is pre-loaded (replace with actual data access)
  global instances
  total_fitness = 0
  for service_type in range(1, num_service_types + 1):
    # Find instances of the current service type within the search space centered at the particle's position
    # (Replace with a more efficient spatial search if needed)
    service_instances = [instance for instance in instances if instance["type"] == service_type and
                         abs(instance["location"][0] - position[0]) <= search_space_size[0] // 10 and
                         abs(instance["location"][1] - position[1]) <= search_space_size[1] // 10]
    if service_instances:
      # Select the instance with the highest fitness (assuming higher fitness is better)
      best_instance = max(service_instances, key=lambda i: i["fitness"])
      total_fitness += best_instance["cost"] + max_time
  return total_fitness


Objective_Function = {
    'F1' : "generate_service_instance" ,
}

#Parameters 
Pop_Size = 100 # Population size : No. of Particles  
MaxT = 100 # No. of Iterations
D = 2 # Dimention
rows, cols = 300, 300 # Search Space Dimentions 
category_counts = {1: 100, 2: 100, 3: 100} # Category Counts
num_service_types = 3
num_instances_per_type = 100
max_cost = 1000 # Assuming a maximum cost for normalization
max_time = 15  # Assuming a maximum time (minutes) for normalization
search_space_size = (300, 300)

# Generate service instances (replace with actual data loading)

instances = [generate_service_instance() for _ in range(num_service_types * num_instances_per_type)]

#Iteration over the ObjF using PSO 


for funName, ObjF in Objective_Function.items() :
    best_position , best_fitness = PSO (calculate_particle_fitness,Pop_Size,D,MaxT)


Output = "Best Position " + str (best_position) + "\n"
Output += "Best Fitness " + str (best_fitness) + '\n'
Output += "\n"

messagebox.showinfo("PSO RESULT",Output)
