#!/usr/bin/python3
"""This is a simple example demonstrating Pycodestyle compliance"""


def calculate_average(numbers):
    """Calculate the average of a list of numbers."""
    total_sum = sum(numbers)
    num_elements = len(numbers)
    
    if num_elements == 0:
        return None
    
    average = total_sum / num_elements
    return average


def main():
    data = [15, 25, 10, 30, 5]
    result = calculate_average(data)
    
    if result is not None:
        print(f"The average is: {result:.2f}")
    else:
        print("No data provided.")

if __name__ == "__main__":
    main()

