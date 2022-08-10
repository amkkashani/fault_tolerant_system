import random
import time
from functools import partial
from typing import List, Tuple
import random
import main
from main import Task
from main import Graph
from main import Node
from main import Cluster

import main

Genome = List[Task]
Population = List[Genome]
FitnessFunc = callable([[Genome], int])
PopulateFunc = callable([[], Population])
SelectionFunc = callable([[Population, FitnessFunc], Tuple[Genome, Genome]])
CrossoverFunc = callable([[Genome, Genome], Tuple[Genome, Genome]])
MutationFunc = callable([[Genome], Genome])

size_of_population = 50


def generate_genome(tasks: List[Task]):
    graph = main.setup_graph_and_clusters()
    random.seed(time.time())
    for task in tasks:
        task.received_throughput = [0] * len(task.vertices)
        start_nodes = set()

        for i, vertex in enumerate(task.vertices):
            if vertex.end == "-2":
                continue  # it is end node and no need to get resource

            start_nodes.add(vertex.start)
            random_replica = random.randint(1, task.replica + 1)
            accepted_replica = task.demand_throughput(vertex.end, task.usage, random_replica, graph)
            task.received_throughput[i] = accepted_replica

    return tasks


def generate_population(size: int, tasks: List[Task]):
    return [generate_genome(tasks) for _ in range(size)]


def fitness(genome: Genome) -> int:
    points = 0
    for task in genome:
        points += task.ford_fulkerson()
    return points


def selection_pair(population: Population, fitnessFunction: FitnessFunc) -> Population:
    return random.choices(
        population=population,
        weights=[fitnessFunction(genome) for genome in population],
        k=15
    )


def single_point_cross_over(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    graph_a = main.setup_graph_and_clusters()
    graph_b = main.setup_graph_and_clusters()
    a_copy = copy_genome_empty_predections(a)
    b_copy = copy_genome_empty_predections(b)
    for i, task in enumerate(a):
        for j, vertex in enumerate(task.vertices):
            if random.randint(0, 2) == 0:  # 50% 50%  result is 1 or 0
                a_copy[i].demand_throughput(vertex.end, a[i].received_throughput[j], a[i].replica, graph_a)
                b_copy[i].demand_throughput(vertex.end, b[i].received_throughput[j], b[i].replica, graph_b)
            else:
                a_copy[i].demand_throughput(vertex.end, b[i].received_throughput[j], a[i].replica, graph_a)
                b_copy[i].demand_throughput(vertex.end, a[i].received_throughput[j], b[i].replica, graph_b)

    return a_copy, b_copy


def mutation(genome: Genome, rnd_range: int = 1):
    new_Graph = main.setup_graph_and_clusters()
    genome_copy = copy_genome_empty_predections(genome)
    for i, task in enumerate(genome):
        for j, vertex in enumerate(task.vertices):
            rnd = random.randint(-1 * rnd_range, rnd_range + 1)
            genome_copy[i].demand_throughput(vertex.end, genome[i].received_throughput[j] + rnd, genome[i].replica,
                                             new_Graph)

    return genome_copy


def copy_genome_empty_predections(genome: Genome) -> Genome:
    tasks = []
    for task in genome:
        tasks.append(task.make_a_copy_with_no_defualt_throw_put())
    return tasks


def run_evolution(
        fitness_func: FitnessFunc,
        # fitness_limit : int ,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_cross_over,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100,
) -> tuple[Population, int]:
    population = generate_population(size_of_population,
                                     main.setup_tasks(main.number_of_clusters, main.number_of_tasks))

    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

        # if fitness_func(population[0]) >= fitness_limit:
        #     break

        next_generation = population[0:2]

        for j in range(int(len(population) / 2) - 1):
            parents = selection_pair(population, fitness_func)
            off_spring_a, off_spring_b = crossover_func(parents[0], parents[1])
            off_spring_a = mutation(off_spring_a)
            off_spring_b = mutation(off_spring_b)
            next_generation += [off_spring_a, off_spring_b]

        population = next_generation[0:size_of_population]
        print(i)
        print(fitness_func(population[0]))

    population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)

    return population, i
