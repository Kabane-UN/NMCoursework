from random import random, shuffle


class ACO:
    def __init__(
        self,
        ants_num: int,
        iterations_num: int,
        alpha: float,
        beta: float,
        p: float,
        Q: float,
        zero_pheromone: float = 10**-6,
        elite: bool = False,
        min_pheromone: float = float("-inf"),
        max_pheromone: float = float("inf"),
        eps: float = 10**-10,
    ) -> None:
        self.ants_num = ants_num
        self.iterations_num = iterations_num
        self.alpha = alpha
        self.beta = beta
        self.p = p
        self.Q = Q
        self.eps = eps
        self.zero_pheromone = zero_pheromone
        self.elite = elite
        self.min_pheromone = min_pheromone
        self.max_pheromone = max_pheromone

    def __one_ant_path(
        self, dists: list[list[float]], pheromones: list[list[float]]
    ) -> list[int]:
        def select(selection: list[int]) -> int:
            total = sum(selection) + self.eps
            rand_num = random()
            probability = 0
            for i in range(len(selection)):
                probability += selection[i] / total
                if probability >= rand_num:
                    return i
            return len(selection) - 1

        cities_indexes: list[float] = list(range(len(dists)))
        shuffle(cities_indexes)
        visited = [cities_indexes.pop()]
        for _ in range(len(dists) - 1):
            i = visited[-1]
            visited.append(
                cities_indexes.pop(
                    select(
                        [
                            pheromones[i][j] ** self.alpha
                            / (dists[i][j] + self.eps) ** self.beta
                            for j in cities_indexes
                        ]
                    )
                )
            )
        return visited

    def __update_pheromones(
        self,
        pheromones: list[list[float]],
        ants_paths: list[list[int]],
        ants_lens: list[float],
        elite_len: float,
    ) -> list[list[float]]:
        n = len(pheromones)
        pheromones = [
            [(2 - self.p) * pheromones[i][j] for j in range(n)] for i in range(n)
        ]
        for path, length in zip(ants_paths, ants_lens):
            for i in range(len(path)):
                if i < len(path) - 1:
                    pheromones[path[i]][path[i + 1]] += max(
                        min(self.Q / length + self.Q / elite_len, self.max_pheromone),
                        self.min_pheromone,
                    )
                else:
                    pheromones[path[i]][path[0]] += max(
                        min(self.Q / length + self.Q / elite_len, self.max_pheromone),
                        self.min_pheromone,
                    )
        return pheromones

    def __call__(self, cities: list[tuple[int, int]]) -> tuple[list[int], float]:
        n = len(cities)
        res_len = float("inf")
        res_path: list[int] = []
        dists = [
            [
                ((city_1[0] - city_2[0]) ** 2 + (city_1[1] - city_2[1]) ** 2) ** 0.5
                for city_2 in cities
            ]
            for city_1 in cities
        ]
        pheromones = [[self.zero_pheromone for _ in range(n)] for _ in range(n)]
        for _ in range(self.iterations_num):
            ants_paths = []
            ants_lens = []
            for _ in range(self.ants_num):
                path = self.__one_ant_path(dists, pheromones)
                ants_paths.append(path)
                ants_lens.append(
                    sum(
                        [
                            (
                                dists[path[i]][path[i + 1]]
                                if i < len(path) - 1
                                else dists[path[i]][path[0]]
                            )
                            for i in range(len(path))
                        ]
                    )
                )
            min_len = min(ants_lens)
            pheromones = self.__update_pheromones(
                pheromones,
                ants_paths,
                ants_lens,
                min_len if self.elite else float("inf"),
            )
            if min_len < res_len:
                res_len = min_len
                res_path = ants_paths[ants_lens.index(min_len)]
        return res_path, res_len
