#!/usr/bin/env python3
"""
compute_statistics.py

Reads a file with numeric values, computes descriptive statistics
using basic algorithms, handles invalid data,
prints results to console and writes them to StatisticsResults.txt.
"""

import sys
import time


def read_numbers(file_path):
    """
    Reads numbers from a file.
    Invalid data is reported but does not stop execution.
    """
    numbers = []
    errors = []

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            for line_num, line in enumerate(file, start=1):
                value = line.strip()
                if value == "":
                    continue
                try:
                    number = float(value)
                    numbers.append(number)
                except ValueError:
                    errors.append(
                        f"Invalid data at line {line_num}: '{value}'"
                    )
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        sys.exit(1)

    return numbers, errors


def compute_mean(data):
    """
    Function to compute the mean value of a list of numbers
    
    :param data: list of numbers
    """
    total = 0.0
    count = 0
    for value in data:
        total += value
        count += 1
    return total / count if count > 0 else 0.0


def compute_median(data):
    """
    Function to compute the median value of a list of numbers
    
    :param data: list of numbers
    """
    sorted_data = sorted(data)
    n = len(sorted_data)

    if n == 0:
        return 0.0

    mid = n // 2
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2.0
    return sorted_data[mid]


def compute_mode(data):
    """
    Function to compute the mode value of a list of numbers
    
    :param data: list of numbers
    """
    frequency = {}
    for value in data:
        if value in frequency:
            frequency[value] += 1
        else:
            frequency[value] = 1

    max_count = 0
    modes = []
    for value, count in frequency.items():
        if count > max_count:
            max_count = count
            modes = [value]
        elif count == max_count:
            modes.append(value)

    if max_count == 1:
        return None
    return modes


def compute_variance(data, mean):
    """
    Function to compute the variance value of a list of numbers
    
    :param data: list of numbers
    :param mean: mean of the list of numbers
    """
    total = 0.0
    n = len(data)
    if n == 0:
        return 0.0

    for value in data:
        diff = value - mean
        total += diff * diff

    return total / n


def compute_std_dev(variance):
    """
    Function to compute the standard deviation of a list of numbers
    
    :param variance: variance of the list of numbers
    """
    return variance ** 0.5


def main():
    """
    Main function which:
    1. Runs function to retrieve numbers from file.
    2. Runs function to get the descriptive statistics.
    3. Shows results in console and appends them to a file.
    """
    if len(sys.argv) < 2:
        print("Usage: python compute_statistics.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    start_time = time.time()

    numbers, errors = read_numbers(file_path)

    if len(numbers) == 0:
        print("No valid numeric data found.")
        sys.exit(1)

    mean = compute_mean(numbers)
    median = compute_median(numbers)
    mode = compute_mode(numbers)
    variance = compute_variance(numbers, mean)
    std_dev = compute_std_dev(variance)

    elapsed_time = time.time() - start_time

    results = []
    results.append("DESCRIPTIVE STATISTICS RESULTS\n")
    results.append(f"Total valid numbers: {len(numbers)}\n")
    results.append(f"Mean: {mean}\n")
    results.append(f"Median: {median}\n")

    if mode is None:
        results.append("Mode: No mode\n")
    else:
        results.append(f"Mode: {mode}\n")

    results.append(f"Variance: {variance}\n")
    results.append(f"Standard Deviation: {std_dev}\n")
    results.append(f"Execution Time (seconds): {elapsed_time}\n")

    if errors:
        results.append("\nERRORS FOUND:\n")
        for error in errors:
            results.append(error + "\n")

    output_text = "".join(results)

    print(output_text)

    with open("StatisticsResults.txt", "w", encoding="utf-8") as out_file:
        out_file.write(output_text)


if __name__ == "__main__":
    main()
