#!/usr/bin/env python3
"""
compute_sales.py

Computes total sales cost using a price catalogue and sales record in JSON.
Prints results to console and writes them to SalesResults.txt.
"""

import sys
import time
import json


def load_json(file_path):
    """
    Load JSON data from a file.
    Returns data and error message when finding exceptions.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file), None
    except FileNotFoundError:
        return None, f"File not found: {file_path}"
    except json.JSONDecodeError:
        return None, f"Invalid JSON format in file: {file_path}"
    except OSError:
        return None, f"Error reading file: {file_path}"


def build_price_catalogue(catalogue, sales):
    """
    Build a dictionary aggregating a list of
    product name, quantity & price by sale ID.

    :param catalogue: catalogue list
    :param sales: sales list
    """
    errors = []
    sales_dictionary = {}
    price_dictionary = {}

    for index, product in enumerate(catalogue):
        title = product.get("title")
        price = product.get("price")

        if not isinstance(title, str):
            errors.append(
                f"Invalid catalogue entry at index {index}: not a String."
            )
            continue

        if not isinstance(price, int) and not isinstance(price, float):
            errors.append(
                f"Invalid catalogue entry at index {index}: not a number."
            )
            continue

        price_dictionary[title] = price

    for index, sale in enumerate(sales):
        sale_id = sale.get("SALE_ID")
        product = sale.get("Product")
        quantity = sale.get("Quantity")
        price = price_dictionary.get(product)

        if price is None:
            errors.append(
                f"Invalid sales entry at index {index}: non-existing product."
            )
            continue

        if not isinstance(sale_id, int):
            errors.append(
                f"Invalid sales entry at index {index}: not an Int."
            )
            continue

        if not isinstance(product, str):
            errors.append(
                f"Invalid sales entry at index {index}: not a String."
            )
            continue

        if not isinstance(quantity, int):
            errors.append(
                f"Invalid sales entry at index {index}: not an Int."
            )
            continue

        if sale_id in sales_dictionary:
            sales_dictionary[sale_id].append({"Product": product,
                                              "Quantity": quantity,
                                              "Price": price})
        else:
            sales_dictionary[sale_id] = [{"Product": product,
                                          "Quantity": quantity,
                                          "Price": price}]

    return sales_dictionary, errors


def compute_sales_total(sales_data):
    """
    Compute total cost of all sales and total cost.

    :param sales_data: merged sales and catalogue dictionary
    """
    sales_total = {}
    total = 0

    for sale_id, sales in sales_data.items():
        for index, sale in enumerate(sales):
            if index == 0:
                sales_total[sale_id] = sale["Price"] * sale["Quantity"]
            else:
                sales_total[sale_id] += sale["Price"] * sale["Quantity"]
            total += sale["Price"] * sale["Quantity"]

    return sales_total, total


def main():
    """
    Main function which:
    1. Reads and stores the JSON files into lists.
    2. Merges the catalogue and sales into a single dictionary.
    3. Computes total cost.
    """
    if len(sys.argv) < 3:
        print(
            "Usage: python compute_sales.py "
            "priceCatalogue.json salesRecord.json"
        )
        sys.exit(1)

    catalogue_file = sys.argv[1]
    sales_file = sys.argv[2]

    start_time = time.time()

    errors = []

    catalogue_data, error = load_json(catalogue_file)

    if error:
        errors.append(error)
        catalogue_data = []

    sales_data, error = load_json(sales_file)

    if error:
        errors.append(error)
        sales_data = []

    sales_data, error = build_price_catalogue(catalogue_data, sales_data)

    if len(error) > 0:
        errors.extend(error)

    sales_total, total_cost = compute_sales_total(sales_data)

    elapsed_time = time.time() - start_time

    results_lines = []
    results_lines.append("SALES RESULTS\n")
    results_lines.append("SALE_ID\tTOTAL\n")
    for sale_id, sale_total in sales_total.items():
        results_lines.append(
            f"{sale_id}\t{sale_total:.2f}\n"
        )

    results_lines.append("\n\n")
    results_lines.append(f"TOTAL SALES COST: ${total_cost:.2f}\n")
    results_lines.append(
        f"Execution Time (seconds): {elapsed_time}\n"
    )

    if errors:
        results_lines.append("\nERRORS FOUND:\n")
        for error in errors:
            results_lines.append(f"- {error}\n")

    output_text = "".join(results_lines)
    print(output_text)

    with open("SalesResults.txt", "w", encoding="utf-8") as out_file:
        out_file.write(output_text)


if __name__ == "__main__":
    main()
