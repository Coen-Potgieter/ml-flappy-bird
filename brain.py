import numpy as np


STRUCTURE = [3, 5, 3, 2]


def get_empty_arr():

    weights = []
    bias = []
    for idx in range(len(STRUCTURE)):
        try:
            arr = np.zeros((STRUCTURE[idx+1], STRUCTURE[idx]))
            single_bias = [0 for i in range(STRUCTURE[idx+1])]

        except IndexError:
            pass
        else:
            weights.append(arr)
            bias.append(single_bias)

    return weights, bias


def init_params():

    weights, bias = get_empty_arr()

    for layer_idx in range(len(weights)):
        weights[layer_idx] = weights[layer_idx] + \
            (np.random.rand(weights[layer_idx].shape[0],
                            weights[layer_idx].shape[1]) - 0.5)

        for b_idx in range(len(bias[layer_idx])):
            bias[layer_idx][b_idx] += np.random.uniform(-0.5, 0.5)

    return weights, bias


def ReLU(Z):
    return np.maximum(Z, 0)


def softmax(Z):
    A = np.exp(Z) / sum(np.exp(Z))
    return A


def for_prop(inpts, weights, bias):
    act_func = ReLU
    out_func = softmax

    z = []
    a = []

    for layer_idx in range(len(weights)):

        if layer_idx == 0:
            dotted = inpts
        else:
            dotted = a[layer_idx-1]

        z.append(weights[layer_idx].dot(dotted) + bias[layer_idx])

        if layer_idx == len(weights) - 1:
            a.append(out_func(z[layer_idx]))
        else:
            a.append(act_func(z[layer_idx]))
            
    return a


def get_prediction(A2):
    return np.argmax(A2, 0)
