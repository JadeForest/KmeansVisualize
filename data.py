import random

def Kmeans(K:int, data:list) -> 'tuple[list[int], list[list[int]]]':
    assert isinstance(data, list), 'data is not a list.'

    n_data = len(data)
    # Random assign centers
    centers = random.sample(data, k=K)

    while True:
        n_changes = 0
        labels = find_label(data, centers)

        for label in list(set(labels)):
            group = [data[i] for i in range(n_data) if labels[i]==label]
            transposed = list(zip(*group))
            new_center = [sum(t)/len(group) for t in transposed]
            old_center = centers[label]
            # Update centers
            if eculidean_dist(old_center,new_center) > 1:
                centers[label] = new_center
                n_changes += 1
        # Generate
        yield labels, centers
        # Exit
        if n_changes == 0:
            break

    # return labels, centers


def eculidean_dist(p1:'list[int]', p2:'list[int]'):
    sum = (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2
    return pow(sum, 1/2)


def find_label(data:list, centers:list) -> 'list[int]':
    labels = [0] * len(data)

    for i in range(len(data)):
        dists = [0] * len(centers)
        for j in range(len(centers)):
            dists[j] = eculidean_dist(data[i],centers[j])
        labels[i] = dists.index( min(dists) )

    return labels


def get_sample_data() -> list:
    with open('data.txt',encoding='utf=8') as f:
        return eval(f.read())

def generate_data() -> list:
    '''
        Generates random clustered data 2D.
    '''
    data = []
    mu = [random.randint(100,200) for i in range(4)]\
        + [random.randint(200,400) for i in range(4)]
    random.shuffle(mu)
    for k in range(random.randint(3,4)):
        for p in range(random.randint(45,55)):
            data.append(
                [random.gauss(mu[2*k],30),random.gauss(mu[2*k+1],30)]
            )

    return data


if __name__ == '__main__':
    data = get_sample_data()
    for labels, centers in Kmeans(3, data):
        print(labels)
        print()
        print(centers)
        print()
    ...