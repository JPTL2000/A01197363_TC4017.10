#!/usr/bin/env python3
"""
convert_numbers.py

Reads numbers from a file, converts them to binary and hexadecimal, 
handles invalid data, prints results to
console and writes them to ConvertionResults.txt.
"""

import sys
import time


def read_numbers(file_path):
    """
    Reads numbers from a file and handles invalid data.
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
                    number = int(value)
                    numbers.append(number)
                except ValueError:
                    errors.append(
                        f"Invalid data at line {line_num}: '{value}'"
                    )
    except FileNotFoundError:
        print(f"Error: File not found -> {file_path}")
        sys.exit(1)

    return numbers, errors


def to_binary(number):
    """
    Converts an integer to binary.
    """
    if number == 0:
        return "0"

    is_negative = number < 0
    number = abs(number)

    digits = []

    while number > 0:
        remainder = number % 2
        digits.append(str(remainder))
        number = number // 2

    binary = ""
    for i in range(len(digits) - 1, -1, -1):
        binary += digits[i]

    if is_negative:
        binary = "-" + binary

    return binary


def to_hexadecimal(number):
    """
    Converts an integer to hexadecimal.
    """
    if number == 0:
        return "0"

    hex_chars = "0123456789ABCDEF"
    is_negative = number < 0
    number = abs(number)

    digits = []

    while number > 0:
        remainder = number % 16
        digits.append(hex_chars[remainder])
        number = number // 16

    hexadecimal = ""
    for i in range(len(digits) - 1, -1, -1):
        hexadecimal += digits[i]

    if is_negative:
        hexadecimal = "-" + hexadecimal

    return hexadecimal


def main():
    """
    Main function which:
    1. Runs function to retrieve numbers from file.
    2. Runs functions to transform numbers into binary and hexadecimal
    3. Shows results in console and appends them to a file.
    """
    if len(sys.argv) < 2:
        print("Usage: python convert_numbers.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    start_time = time.time()

    numbers, errors = read_numbers(file_path)

    results_lines = []
    results_lines.append("NUMBER CONVERSION RESULTS\n")
    results_lines.append("Decimal\tBinary\tHexadecimal\n")

    for number in numbers:
        binary = to_binary(number)
        hexadecimal = to_hexadecimal(number)
        results_lines.append(
            f"{number}\t{binary}\t{hexadecimal}\n"
        )

    elapsed_time = time.time() - start_time
    results_lines.append(
        f"\nExecution Time (seconds): {elapsed_time}\n"
    )

    output_text = "".join(results_lines)

    print(output_text)

    if errors:
        print("ERRORS FOUND:")
        for error in errors:
            print(error)

    with open("ConvertionResults.txt", "w", encoding="utf-8") as out_file:
        out_file.write(output_text)

        if errors:
            out_file.write("\nERRORS FOUND:\n")
            for error in errors:
                out_file.write(error + "\n")


if __name__ == "__main__":
    main()
