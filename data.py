import random, json


def eculidean_dist(p1: list[int], p2: list[int]):
    sum = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2
    return pow(sum, 1 / 2)


def manhattan_dist(p1: list[int], p2: list[int]):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


DIST_FUNCS = {"eculidean": eculidean_dist, "manhattan": manhattan_dist}


def Kmeans(
    K: int, data: list, dist_func: str = "eculidean"
) -> tuple[list[int], list[list[int]]]:
    assert isinstance(data, list), "data is not a list."
    assert dist_func in DIST_FUNCS.keys(), f"{dist_func} not valid."
    distance = DIST_FUNCS[dist_func]

    n_data = len(data)
    # Random assign centers
    centers = random.sample(data, k=K)

    while True:
        n_changes = 0
        labels = find_label(data, centers, dist_func)

        for label in list(set(labels)):
            group = [data[i] for i in range(n_data) if labels[i] == label]
            transposed = list(zip(*group))
            new_center = [sum(t) / len(group) for t in transposed]
            old_center = centers[label]
            # Update centers
            if distance(old_center, new_center) > 1:
                centers[label] = new_center
                n_changes += 1
        # Generate
        yield labels, centers
        # Exit
        if n_changes == 0:
            break


def find_label(data: list, centers: list, dist_func: str) -> list[int]:
    distance = DIST_FUNCS[dist_func]
    labels = [0] * len(data)

    for i, datapoint in enumerate(data):
        dists = [0] * len(centers)
        for j, center in enumerate(centers):
            dists[j] = distance(datapoint, center)
        labels[i] = dists.index(min(dists))

    return labels


def get_sample_data() -> list[list[float]]:
    with open("data.json", encoding="utf=8") as f:
        loaded = json.load(f)
        return loaded["data"]


def generate_random_data() -> list:
    """
    Generates random clustered data 2D.
    """
    NUM_POINTS = random.randint(55, 85)
    NUM_CLUSTERS = random.randint(3, 4)
    mean = [random.randint(100, 200) for _ in range(4)] + [
        random.randint(200, 400) for _ in range(4)
    ]
    random.shuffle(mean)

    data = []
    for k in range(NUM_CLUSTERS):
        for _ in range(NUM_POINTS):
            data.append(
                [random.gauss(mean[2 * k], 40), random.gauss(mean[2 * k + 1], 50)]
            )
    # print(f"{NUM_POINTS=}, {NUM_CLUSTERS=}")
    return data


def generate_grid_data() -> list:
    """
    Generates random rectangular (grid) data 2D.
    """
    NUM_RECTANGLES = 4
    end_point_pairs = [
        [[random.randint(3, 30), random.randint(3, 30)] for _ in range(2)]
        for _ in range(NUM_RECTANGLES)
    ]

    data: list[tuple] = []
    for vector in end_point_pairs:
        rect_data: list[tuple] = []
        for x in range(
            min(vector[0][0], vector[1][0]), max(vector[0][0], vector[1][0]) + 1
        ):
            for y in range(
                min(vector[0][1], vector[1][1]), max(vector[0][1], vector[1][1]) + 1
            ):
                rect_data.append((x * 15, y * 15))
        data.extend(rect_data)
    return list(set(data))


if __name__ == "__main__":
    data = generate_grid_data()
    print(data)
    ...
