import random
from typing import List
from main import Task
from main import graph

Genome = List[Task]
Population = List[Genome]


def generate_genome(tasks: List[Task]):
    for task in tasks:
        task.received_throughput = [0] * len(task.vertices)
        start_nodes = set()

        for i, vertex in enumerate(task.vertices):
            if vertex.start in start_nodes:
                continue

            start_nodes.add(vertex.start)
            task.received_throughput[i] = random.randint(1, task.replica + 1)


def generate_population(size: int, tasks: List[Task]):
    return [generate_genome(tasks) for _ in range(size)]

def fitness_function(genome : Genome) -> int:
    yield
