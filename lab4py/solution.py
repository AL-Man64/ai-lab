#!/usr/bin/env python3


from abc import ABC, abstractmethod
import csv
import math
from argparse import ArgumentParser, Namespace

import numpy as np


def sigmoid(x):
    return 1 / 1 + math.pow(math.e, x)


class NeuralNetwork(ABC):
    @abstractmethod
    def new_instance(self):
        pass

    @abstractmethod
    def cross(self, other):
        pass

    @abstractmethod
    def mutate(self, p: float, K: float):
        pass

    @abstractmethod
    def predict(self, data) -> float:
        pass


class NeuralNetwork5s(NeuralNetwork):
    input_count: int

    weights: list

    def __init__(self, input_count: int) -> None:
        self.input_count = input_count

        self.weights = []

        self.weights.append(np.random.normal(scale=0.01, size=(5, input_count + 1)))
        self.weights.append(np.random.normal(scale=0.01, size=(1, 6)))

    def new_instance(self) -> NeuralNetwork:
        return NeuralNetwork5s(self.input_count)

    def cross(self, other: NeuralNetwork) -> NeuralNetwork:
        if not isinstance(other, NeuralNetwork5s):
            raise Exception("Incompatible neural networks")

        child_weights = []

        for father_weights, mother_weights in zip(self.weights, other.weights):
            child_weights.append((father_weights + mother_weights) / 2)

        child = NeuralNetwork5s(self.input_count)
        child.weights = child_weights

        return child

    def mutate(self, p: float, K: float):
        if np.random.uniform(0.0, 1.0) <= p:
            self.weights[0] += np.random.normal(scale=K, size=(5, self.input_count + 1))
            self.weights[1] += np.random.normal(scale=K, size=(1, 6))

    def predict(self, data) -> float:
        Y = self.weights[0][:, 1:] @ data + self.weights[0][:, 0]
        Y = np.array([sigmoid(x) for x in Y])

        return (self.weights[1][:, 1:] @ Y + self.weights[1][:, 0])[0]


class NeuralNetwork20s(NeuralNetwork):
    input_count: int

    def __init__(self, input_count: int) -> None:
        self.input_count = input_count

        self.weights = []

        self.weights.append(np.random.normal(scale=0.01, size=(20, input_count + 1)))
        self.weights.append(np.random.normal(scale=0.01, size=(1, 21)))

    def new_instance(self) -> NeuralNetwork:
        return NeuralNetwork20s(self.input_count)

    def cross(self, other: NeuralNetwork) -> NeuralNetwork:
        if not isinstance(other, NeuralNetwork20s):
            raise Exception("Incompatible neural networks")

        child_weights = []

        for father_weights, mother_weights in zip(self.weights, other.weights):
            child_weights.append((father_weights + mother_weights) / 2)

        child = NeuralNetwork20s(self.input_count)
        child.weights = child_weights

        return child

    def mutate(self, p: float, K: float):
        if np.random.uniform(0.0, 1.0) <= p:
            self.weights[0] += np.random.normal(
                scale=K, size=(20, self.input_count + 1)
            )
            self.weights[1] += np.random.normal(scale=K, size=(1, 21))

    def predict(self, data) -> float:
        Y = self.weights[0][:, 1:] @ data + self.weights[0][:, 0]
        Y = np.array([sigmoid(x) for x in Y])

        return (self.weights[1][:, 1:] @ Y + self.weights[1][:, 0])[0]


class NeuralNetwork5s5s(NeuralNetwork):
    input_count: int

    def __init__(self, input_count: int) -> None:
        self.input_count = input_count

        self.weights = []

        self.weights.append(np.random.normal(scale=0.01, size=(5, input_count + 1)))
        self.weights.append(np.random.normal(scale=0.01, size=(5, 6)))
        self.weights.append(np.random.normal(scale=0.01, size=(1, 6)))

    def new_instance(self) -> NeuralNetwork:
        return NeuralNetwork5s5s(self.input_count)

    def cross(self, other: NeuralNetwork) -> NeuralNetwork:
        if not isinstance(other, NeuralNetwork5s5s):
            raise Exception("Incompatible neural networks")

        child_weights = []

        for father_weights, mother_weights in zip(self.weights, other.weights):
            child_weights.append((father_weights + mother_weights) / 2)

        child = NeuralNetwork5s5s(self.input_count)
        child.weights = child_weights

        return child

    def mutate(self, p: float, K: float):
        if np.random.uniform(0.0, 1.0) <= p:
            self.weights[0] += np.random.normal(scale=K, size=(5, self.input_count + 1))
            self.weights[1] += np.random.normal(scale=K, size=(5, 6))
            self.weights[2] += np.random.normal(scale=K, size=(1, 6))

    def predict(self, data) -> float:
        Y = self.weights[0][:, 1:] @ data + self.weights[0][:, 0]
        Y = np.array([sigmoid(x) for x in Y])

        X = Y

        Y = self.weights[1][:, 1:] @ X + self.weights[1][:, 0]
        Y = np.array([sigmoid(x) for x in Y])

        return (self.weights[2][:, 1:] @ Y + self.weights[2][:, 0])[0]


class NeuralNetworkClient:
    nn: NeuralNetwork

    def __init__(self, nn: NeuralNetwork) -> None:
        self.nn = nn

    def new_instance(self) -> NeuralNetwork:
        return self.nn.new_instance()


class Program:
    args: Namespace

    def __init__(self) -> None:
        ap = ArgumentParser()

        ap.add_argument("--train", type=str, help="path to the training dataset")
        ap.add_argument("--test", type=str, help="path to the test dataset")
        ap.add_argument("--nn", type=str, help="the neural network achitecture")
        ap.add_argument(
            "--popsize", type=int, help="the population size of the genetic algorithm"
        )
        ap.add_argument(
            "--elitism", type=int, help="the elitism of the genetic algorithm"
        )
        ap.add_argument(
            "--p",
            type=float,
            help="the mutation probability of each chromosome element",
        )
        ap.add_argument(
            "--K",
            type=float,
            help="the standard derivation of the mutation of gaussian noise",
        )
        ap.add_argument(
            "--iter",
            type=int,
            help="the number of genetic algorithm iterations",
        )

        self.args = ap.parse_args()

    def load_data(self, path: str):
        input_data = []
        output_data = []

        first_row = True

        with open(path) as f:
            csv_reader = csv.reader(f)
            for row in csv_reader:
                if not first_row:
                    data = [float(x) for x in row]

                    input_data.append(data[0:-1])
                    output_data.append(data[-1])
                else:
                    self.target_value = row[-1]
                    first_row = False

        return (
            np.array(input_data, dtype=np.float32),
            np.array(output_data, dtype=np.float32),
        )

    def run(self):
        self.input_data, self.output_data = self.load_data(self.args.train)

        input_count = self.input_data.shape[1]

        client = NeuralNetworkClient(NeuralNetwork5s(0))

        match self.args.nn:
            case "5s":
                client = NeuralNetworkClient(NeuralNetwork5s(input_count))
            case "20s":
                client = NeuralNetworkClient(NeuralNetwork20s(input_count))
            case "5s5s":
                client = NeuralNetworkClient(NeuralNetwork5s5s(input_count))
            case _:
                Exception("Couldn't determine hardcoded architecture")

        neural_networks: list[NeuralNetwork] = []

        for _ in range(0, self.args.popsize):
            neural_networks.append(client.new_instance())

        for i in range(1, self.args.iter + 1):
            errs_by_network = []

            for network in neural_networks:
                predictions = []

                for inputs in self.input_data:
                    predictions.append(network.predict(inputs))

                predictions = np.array(predictions, dtype=np.float32)

                errs = predictions - self.output_data

                err = 0

                for single_err in errs:
                    err += single_err**2

                err /= len(errs)

                errs_by_network.append(err)

            next_gen: list[NeuralNetwork] = []

            for j, err in enumerate(errs_by_network):
                if err <= sorted(errs_by_network)[self.args.elitism - 1]:
                    next_gen.append(neural_networks[j])

            for j, err in enumerate(errs_by_network):
                if err > sorted(errs_by_network)[self.args.elitism - 1]:
                    child: NeuralNetwork = neural_networks[j].cross(next_gen[0])
                    child.mutate(self.args.p, self.args.K)
                    next_gen.append(child)

            neural_networks = next_gen

            if i % 2000 == 0:
                print(f"[Train error @{i}] {sorted(errs_by_network)[0]}")

        best = neural_networks[0]

        self.input_data, self.output_data = self.load_data(self.args.test)

        predictions = []

        for inputs in self.input_data:
            predictions.append(best.predict(inputs))

        predictions = np.array(predictions, dtype=np.float32)

        errs = predictions - self.output_data

        err = 0

        for single_err in errs:
            err += single_err**2

        err /= len(errs)

        print(f"[Test error] {err}")


if __name__ == "__main__":
    Program().run()
