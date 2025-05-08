# This is my first calculator program in Python

# I defined a function to add two numbers and return their sum
def add(x, y):
    return x + y 

# I defined a function to subtract two numbers and return their difference
def subtract(x, y):
    return x - y 

# I defined a function to multiply two numbers and return their product
def multiply(x, y):
    return x * y 

# I defined a function to divide two numbers and return their quotient
# I also made it so that the function handles the case where the second number is zero to avoid errors because that would crash the program
def divide(x, y):
    try:
        return x / y 
    except ZeroDivisionError:
        # This block runs if someone tries to divide by zero
        return "Error: Cannot divide by zero!"

# Main function that drives the calculator program
# It displays a menu, takes user input, and then displays the result

def main():
    print("Simple Calculator")  # Program Title
    print("Select operation:")  # Prompt to choose an operation
    print("1. Add")         # Option 1 for addition
    print("2. Subtract")    # Option 2 for subtraction
    print("3. Multiply")    # Option 3 for multiplication
    print("4. Divide")      # Option 4 for division
    print("5. Exit")        # Option 5 to quit the program

    # I also added an infinite loop so that the program keeps asking until the user chooses to exit
    while True:
        # Ask the user which operation they want to perform
        choice = input("Enter choice (1/2/3/4/5): ")

        # Check if the user wants to exit
        if choice == '5':
            print("Exiting calculator. Goodbye!")
            break  # Exit the loop and end the program

        # Check if the choice is one of the valid operations
        if choice in ('1', '2', '3', '4'):
            try:
                # Ask the user for the two numbers to operate on
                # float() converts the input string into a decimal number
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                # This runs if the user input wasn't a number
                print("Invalid input: Please enter numeric values.")
                continue  # Go back to the start of the loop

            # Based on the user's choice, the proper function is called
            if choice == '1':
                result = add(num1, num2)
                op = '+'  # Addition
            elif choice == '2':
                result = subtract(num1, num2)
                op = '-'  # Subtraction
            elif choice == '3':
                result = multiply(num1, num2)
                op = '*'  # Multiplication
            elif choice == '4':
                result = divide(num1, num2)
                op = '/'  # Division

            # This shows the complete calculation and its result
            print(f"{num1} {op} {num2} = {result}")
        else:
            # If the user enters anything other than 1-5, this message is shown
            print("Invalid choice: Please select a valid operation.")

# This line ensures that main() is called when you run the script directly
if __name__ == '__main__':
    main()


# Follow up changes will be made later. I will add more features like:
# - History of calculations
# - Advanced operations like exponentiation, square root, etc.
# - A graphical user interface (GUI) using Tkinter or PyQt