#!/usr/bin/env python3
"""
word_count.py

Reads words from a file, identifies distinct words and their frequencies
using basic algorithms, handles invalid data, prints results to console
and writes them to WordCountResults.txt.
"""

import sys
import time


def is_letter(character):
    """
    Checks if a character is a letter.
    """
    return ("a" <= character <= "z") or ("A" <= character <= "Z")


def normalize_word(word):
    """
    Converts a word to lowercase.
    """
    normalized = ""
    for char in word:
        if "A" <= char <= "Z":
            normalized += chr(ord(char) + 32)
        else:
            normalized += char
    return normalized


def extract_words(text):
    """
    Extracts words from text.
    """
    words = []
    current_word = ""

    for char in text:
        if is_letter(char):
            current_word += char
        else:
            if current_word != "":
                words.append(current_word)
                current_word = ""

    if current_word != "":
        words.append(current_word)

    return words


def count_words(words):
    """
    Counts word frequencies.
    """
    distinct_words = []
    frequencies = []

    for word in words:
        found = False
        for index, existing_word in enumerate(distinct_words):
            if existing_word == word:
                frequencies[index] += 1
                found = True
                break

        if not found:
            distinct_words.append(word)
            frequencies.append(1)

    return distinct_words, frequencies


def read_file(file_path):
    """
    Reads the file content.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read(), None
    except FileNotFoundError:
        return None, "File not found."
    except OSError:
        return None, "Error reading the file."


def main():
    """
    Main function which:
    1. Runs a function to retrieve words from the file.
    2. Runs a function to make the words lower case.
    3. Counts the frequency of each word.
    4. Shows results in console and appends them to a file.
    """
    if len(sys.argv) < 2:
        print("Usage: python word_count.py fileWithData.txt")
        sys.exit(1)

    file_path = sys.argv[1]

    start_time = time.time()

    content, error = read_file(file_path)

    if error is not None:
        print(f"Error reading file: {error}")
        sys.exit(1)

    words = extract_words(content)

    normalized_words = []
    for word in words:
        normalized_words.append(normalize_word(word))

    distinct_words, frequencies = count_words(normalized_words)

    results_lines = []
    results_lines.append("WORD COUNT RESULTS\n")
    results_lines.append("Word\tFrequency\n")

    for ind, word in enumerate(distinct_words):
        results_lines.append(
            f"{word}\t{frequencies[ind]}\n"
        )

    elapsed_time = time.time() - start_time
    results_lines.append(
        f"\nExecution Time (seconds): {elapsed_time}\n"
    )

    output_text = "".join(results_lines)

    print(output_text)

    with open("WordCountResults.txt", "w", encoding="utf-8") as out_file:
        out_file.write(output_text)



if __name__ == "__main__":
    main()
