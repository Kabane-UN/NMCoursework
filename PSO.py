from random import sample, random
from typing import Callable


class PSO:
    class Particle:
        def __init__(
            self, path: list[int], calc_len: Callable[[list[int]], float]
        ) -> None:
            self.path = path
            self.best_path = path
            self.calc_len = calc_len
            self.current_len = self.calc_len(self.path)
            self.best_len = self.current_len

        def set_path(self, path):
            self.path = path
            self.current_len = self.calc_len(self.path)
            if self.current_len < self.best_len:
                self.best_path = self.path
                self.best_len = self.current_len

    def __init__(
        self,
        particle_num: int,
        iterations_num: int,
        momentum: float,
        social_factor: float,
        neighborhood_factor: float,
    ) -> None:
        self.particle_num = particle_num
        self.iterations_num = iterations_num
        self.momentum = momentum
        self.social_factor = social_factor
        self.neighborhood_factor = neighborhood_factor

    def __call__(self, cities) -> tuple[list[int], float]:

        dists = [
            [
                ((city_1[0] - city_2[0]) ** 2 + (city_1[1] - city_2[1]) ** 2) ** 0.5
                for city_2 in cities
            ]
            for city_1 in cities
        ]
        calc_len = lambda path: sum(
            [
                (
                    dists[path[i]][path[i + 1]]
                    if i < len(path) - 1
                    else dists[path[i]][path[0]]
                )
                for i in range(len(path))
            ]
        )
        particles = [
            PSO.Particle(path, calc_len)
            for path in [
                sample(list(range(len(cities))), len(cities))
                for _ in range(self.particle_num)
            ]
        ]
        best_particle: PSO.Particle = None
        for _ in range(self.iterations_num):
            best_particle = min(particles, key=lambda x: x.best_len)
            for particle in particles:
                path = particle.path.copy()
                self_best = particle.best_path.copy()
                best_path = best_particle.best_path.copy()
                nearest_path = min(
                    particles, key=lambda x: abs(x.current_len - particle.current_len)
                ).path.copy()
                v = []
                for i in range(len(cities)):
                    if path[i] != self_best[i]:
                        swap = (i, self_best.index(i), self.momentum >= random())
                        v.append(swap)
                        self_best[swap[0]], self_best[swap[1]] = (
                            self_best[swap[1]],
                            self_best[swap[0]],
                        )
                    if path[i] != best_path[i]:
                        swap = (i, best_path.index(i), self.social_factor >= random())
                        v.append(swap)
                        best_path[swap[0]], best_path[swap[1]] = (
                            best_path[swap[1]],
                            best_path[swap[0]],
                        )
                    if path[i] != nearest_path[i]:
                        swap = (
                            i,
                            nearest_path.index(i),
                            self.neighborhood_factor >= random(),
                        )
                        v.append(swap)
                        nearest_path[swap[0]], nearest_path[swap[1]] = (
                            nearest_path[swap[1]],
                            nearest_path[swap[0]],
                        )
                for swap in v:
                    if swap[2]:
                        path[swap[0]], path[swap[1]] = path[swap[1]], path[swap[0]]
                particle.set_path(path)
        return best_particle.best_path, best_particle.best_len
