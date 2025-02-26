import json
import matplotlib.pyplot as plt
from collections import Counter


def load_json(file_path):
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def extract_numbers(data):
    numbers = []
    for value in data.values():
        try:
            num = int(value)
            if -1 <= num <= 99:
                numbers.append(num)
        except ValueError:
            continue
    return numbers


def count_occurrences(numbers):
    return Counter(numbers)


def plot_full_range(counter):
    x = list(range(-1, 100))
    y = [counter[num] for num in x]

    plt.figure(figsize=(12, 6))
    plt.bar(x, y, color="skyblue", edgecolor="black")
    plt.yscale("log")

    plt.title("Training Frequency of Numbers")
    plt.xlabel("Number")
    plt.ylabel("Log Frequency")
    plt.xticks(range(-1, 100, 5))
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


def plot_single_digits(counter):
    digit_counter = Counter()
    for num, count in counter.items():
        if num == -1:
            continue
        for digit in str(num):
            digit_counter[int(digit)] += count

    x = list(range(0, 10))
    y = [digit_counter[num] for num in x]

    plt.figure(figsize=(8, 6))
    plt.bar(x, y, color="lightgreen", edgecolor="black")
    plt.title("Training Frequency of Single-Digit Numbers")
    plt.xlabel("Number")
    plt.ylabel("Frequency")
    plt.xticks(range(0, 10))
    plt.grid(axis="y", linestyle="--", alpha=0.7)
    plt.show()


def main():
    file_path = "./data/SoccerNet/train/train_gt.json"

    data = load_json(file_path)
    numbers = extract_numbers(data)
    counter = count_occurrences(numbers)

    plot_full_range(counter)
    plot_single_digits(counter)


if __name__ == "__main__":
    main()
