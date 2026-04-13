

import datetime
import json
from typing import List, Dict, Tuple
import os

# =====================================
# DATA STRUCTURES & GLOBAL VARIABLES
# =====================================

# Dictionary to store user profile
user_profile = {
    "name": "",
    "monthly_income": 0.0,
    "savings_goal": 0.0
}

# List to store all transactions (each transaction is a dictionary)
transactions = []

# Dictionary to store budget categories with their limits
budget_categories = {
    "Food": 0.0,
    "Transportation": 0.0,
    "Entertainment": 0.0,
    "Utilities": 0.0,
    "Healthcare": 0.0,
    "Shopping": 0.0,
    "Other": 0.0
}

# Set to store unique expense categories (demonstrates Set data structure)
expense_categories = set()


# ==============================
# HELPER FUNCTIONS
# ==============================

def clear_screen():
    """Clear the console screen"""
    print("\n" * 100)


def display_header(title: str):
    """Display a formatted header"""
    print("\n" + "="*50)
    print(f"{title:^50}")
    print("="*50)


def get_float_input(prompt: str) -> float:
    """
    Get validated float input from user
    Demonstrates: Exception handling, while loop, type conversion
    """
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print(" Please enter a positive number.")
                continue
            return value
        except ValueError:
            print(" Invalid input! Please enter a valid number.")


def get_int_input(prompt: str, min_val: int = 1, max_val: int = 100) -> int:
    """
    Get validated integer input within a range
    Demonstrates: Type conversion, conditional logic
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            else:
                print(f" Please enter a number between {min_val} and {max_val}.")
        except ValueError:
            print(" Invalid input! Please enter a valid integer.")


def get_date_input(prompt: str) -> str:
    """
    Get validated date input
    Demonstrates: String manipulation, datetime module, exception handling
    """
    while True:
        date_str = input(prompt + " (YYYY-MM-DD): ")
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")


# =========================================
# CORE FUNCTIONALITY FUNCTIONS
# =========================================

def setup_user_profile():
    """
    Setup user profile
    Demonstrates: Dictionary manipulation, user input
    """
    display_header("USER PROFILE SETUP")
    
    user_profile["name"] = input("Enter your name: ").strip()
    user_profile["monthly_income"] = get_float_input("Enter your monthly income ($): ")
    user_profile["savings_goal"] = get_float_input("Enter your monthly savings goal ($): ")
    
    print(f"\n Profile created successfully! Welcome, {user_profile['name']}!")
    input("\nPress Enter to continue...")


def setup_budget_categories():
    """
    Set budget limits for different categories
    Demonstrates: Dictionary iteration, key-value pairs
    """
    display_header("BUDGET CATEGORY SETUP")
    
    print("Set monthly budget limits for each category:\n")
    
    for category in budget_categories.keys():
        budget_categories[category] = get_float_input(f"{category}: $")
    
    print("\n Budget categories configured successfully!")
    input("\nPress Enter to continue...")


def add_transaction():
    """
    Add a new income or expense transaction
    Demonstrates: List append, dictionary creation, datetime, conditional logic
    """
    display_header("ADD TRANSACTION")
    
    print("1. Income")
    print("2. Expense")
    
    trans_type = get_int_input("\nSelect transaction type (1-2): ", 1, 2)
    
    # Create transaction dictionary
    transaction = {
        "id": len(transactions) + 1,  # Integer ID
        "type": "Income" if trans_type == 1 else "Expense",  # String
        "amount": 0.0,  # Float
        "category": "",  # String
        "description": "",  # String
        "date": "",  # String
        "is_recurring": False  # Boolean
    }
    
    transaction["amount"] = get_float_input("Enter amount ($): ")
    
    if transaction["type"] == "Expense":
        # Display available categories
        print("\nAvailable Categories:")
        categories_list = list(budget_categories.keys())  # Convert dict keys to list
        for idx, cat in enumerate(categories_list, 1):
            print(f"{idx}. {cat}")
        
        cat_choice = get_int_input(f"\nSelect category (1-{len(categories_list)}): ", 
                                   1, len(categories_list))
        transaction["category"] = categories_list[cat_choice - 1]
        
        # Add to expense categories set (demonstrates Set)
        expense_categories.add(transaction["category"])
    else:
        transaction["category"] = "Income"
    
    transaction["description"] = input("Enter description: ").strip()
    transaction["date"] = get_date_input("Enter date")
    
    recurring = input("Is this a recurring transaction? (y/n): ").lower()
    transaction["is_recurring"] = recurring == 'y'
    
    # Add transaction to list
    transactions.append(transaction)
    
    print(f"\n Transaction added successfully! (ID: {transaction['id']})")
    input("\nPress Enter to continue...")


def view_all_transactions():
    """
    Display all transactions
    Demonstrates: List iteration, string formatting, conditional display
    """
    display_header("ALL TRANSACTIONS")
    
    if not transactions:
        print("\n No transactions found.")
        input("\nPress Enter to continue...")
        return
    
    print(f"\n{'ID':<5} {'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<10} {'Description':<20}")
    print("-" * 85)
    
    for trans in transactions:
        # String formatting with f-strings
        print(f"{trans['id']:<5} {trans['date']:<12} {trans['type']:<10} "
              f"{trans['category']:<15} ${trans['amount']:<9.2f} {trans['description']:<20}")
    
    input("\nPress Enter to continue...")


def view_transactions_by_category():
    """
    Filter and display transactions by category
    Demonstrates: List comprehension, filtering, nested data structures
    """
    display_header("TRANSACTIONS BY CATEGORY")
    
    if not transactions:
        print("\n No transactions found.")
        input("\n Press Enter to continue...")
        return
    
    # Get unique categories from transactions using list comprehension and set
    categories = list(set(t["category"] for t in transactions))
    
    print("Available categories:")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat}")
    
    choice = get_int_input(f"\nSelect category (1-{len(categories)}): ", 1, len(categories))
    selected_category = categories[choice - 1]
    
    # Filter transactions using list comprehension
    filtered = [t for t in transactions if t["category"] == selected_category]
    
    print(f"\n--- {selected_category} Transactions ---\n")
    print(f"{'ID':<5} {'Date':<12} {'Type':<10} {'Amount':<10} {'Description':<20}")
    print("-" * 70)
    
    for trans in filtered:
        print(f"{trans['id']:<5} {trans['date']:<12} {trans['type']:<10} "
              f"${trans['amount']:<9.2f} {trans['description']:<20}")
    
    input("\nPress Enter to continue...")


def calculate_summary() -> Tuple[float, float, float]:
    """
    Calculate financial summary
    Demonstrates: Tuple return, list comprehension, sum() function
    Returns: (total_income, total_expenses, balance) as a tuple
    """
    # Using list comprehension to filter and sum
    total_income = sum(t["amount"] for t in transactions if t["type"] == "Income")
    total_expenses = sum(t["amount"] for t in transactions if t["type"] == "Expense")
    balance = total_income - total_expenses
    
    return (total_income, total_expenses, balance)  # Tuple


def display_financial_summary():
    """
    Display comprehensive financial summary
    Demonstrates: Tuple unpacking, dictionary operations, percentage calculations
    """
    display_header("FINANCIAL SUMMARY")
    
    # Tuple unpacking
    total_income, total_expenses, balance = calculate_summary()
    
    print(f"\n{'Metric':<30} {'Amount':>15}")
    print("-" * 45)
    print(f"{'Total Income':<30} ${total_income:>14.2f}")
    print(f"{'Total Expenses':<30} ${total_expenses:>14.2f}")
    print(f"{'Current Balance':<30} ${balance:>14.2f}")
    print(f"{'Savings Goal':<30} ${user_profile['savings_goal']:>14.2f}")
    
    # Calculate savings percentage
    if user_profile['monthly_income'] > 0:
        savings_rate = (balance / user_profile['monthly_income']) * 100
        print(f"{'Savings Rate':<30} {savings_rate:>14.2f}%")
    
    print("\n" + "=" * 45)
    print("CATEGORY BREAKDOWN")
    print("=" * 45)
    
    # Dictionary to store category-wise expenses
    category_expenses = {}
    
    for trans in transactions:
        if trans["type"] == "Expense":
            cat = trans["category"]
            category_expenses[cat] = category_expenses.get(cat, 0) + trans["amount"]
    
    print(f"\n{'Category':<20} {'Spent':>12} {'Budget':>12} {'Remaining':>12}")
    print("-" * 60)
    
    for category, budget_limit in budget_categories.items():
        spent = category_expenses.get(category, 0)
        remaining = budget_limit - spent
        print(f"{category:<20} ${spent:>11.2f} ${budget_limit:>11.2f} ${remaining:>11.2f}")
        
        # Warning if over budget
        if spent > budget_limit and budget_limit > 0:
            print(f" OVER BUDGET by ${spent - budget_limit:.2f}!")
    
    input("\nPress Enter to continue...")


def search_transactions():
    """
    Search transactions by description keyword
    Demonstrates: String methods, filtering, case-insensitive search
    """
    display_header("SEARCH TRANSACTIONS")
    
    if not transactions:
        print("\n No transactions found.")
        input("\nPress Enter to continue...")
        return
    
    keyword = input("Enter search keyword: ").strip().lower()
    
    # Search using list comprehension and string methods
    results = [t for t in transactions if keyword in t["description"].lower()]
    
    if not results:
        print(f"\n No transactions found matching '{keyword}'")
    else:
        print(f"\n Found {len(results)} transaction(s):\n")
        print(f"{'ID':<5} {'Date':<12} {'Type':<10} {'Category':<15} {'Amount':<10} {'Description':<20}")
        print("-" * 85)
        
        for trans in results:
            print(f"{trans['id']:<5} {trans['date']:<12} {trans['type']:<10} "
                  f"{trans['category']:<15} ${trans['amount']:<9.2f} {trans['description']:<20}")
    
    input("\nPress Enter to continue...")


def delete_transaction():
    """
    Delete a transaction by ID
    Demonstrates: List manipulation, enumerate, conditional removal
    """
    display_header("DELETE TRANSACTION")
    
    if not transactions:
        print("\n No transactions found.")
        input("\nPress Enter to continue...")
        return
    
    trans_id = get_int_input("Enter transaction ID to delete: ", 1, len(transactions))
    
    # Find and remove transaction
    for idx, trans in enumerate(transactions):
        if trans["id"] == trans_id:
            confirm = input(f"Delete '{trans['description']}' (${trans['amount']})? (y/n): ").lower()
            if confirm == 'y':
                transactions.pop(idx)  # Remove from list
                print("\n Transaction deleted successfully!")
            else:
                print("\n Deletion cancelled.")
            input("\nPress Enter to continue...")
            return
    
    print("\n Transaction ID not found.")
    input("\nPress Enter to continue...")



def save_data():
    """
    Save data to JSON file
    Demonstrates: File I/O, JSON serialization, dictionary/list operations
    """
    data = {
        "user_profile": user_profile,
        "budget_categories": budget_categories,
        "transactions": transactions,
        "expense_categories": list(expense_categories)  # Convert set to list for JSON
    }
    
    try:
        # Use a consistent, valid path - saves in current directory
        with open("budget_data.json", "w") as file:
            json.dump(data, file, indent=4)
        print("\nData saved successfully!")
    except Exception as e:
        print(f"\nError saving data: {e}")


def load_data():
    """
    Load data from JSON file
    Demonstrates: File I/O, JSON deserialization, exception handling
    """
    global user_profile, budget_categories, transactions, expense_categories
    
    try:
        # Use the same path as save_data()
        with open("budget_data.json", "r") as file:
            data = json.load(file)
            
            user_profile = data.get("user_profile", user_profile)
            budget_categories = data.get("budget_categories", budget_categories)
            transactions = data.get("transactions", transactions)
            expense_categories = set(data.get("expense_categories", []))  # Convert list back to set
            
        print("\n Data loaded successfully!")
    except FileNotFoundError:
        print("\n Welcome to your monthly budget system.")  # Fixed typo
    except Exception as e:
        print(f"\n✗ Error loading data: {e}")

def display_statistics():
    """
    Display advanced statistics
    Demonstrates: Dictionary operations, max/min functions, sorted()
    """
    display_header("STATISTICS & INSIGHTS")
    
    if not transactions:
        print("\n No transactions to analyze.")
        input("\nPress Enter to continue...")
        return
    
    # Get expense transactions only
    expenses = [t for t in transactions if t["type"] == "Expense"]
    
    if expenses:
        # Find highest expense using max() with key function
        highest_expense = max(expenses, key=lambda x: x["amount"])
        print(f" Highest Expense: ${highest_expense['amount']:.2f} - {highest_expense['description']}")
        
        # Find lowest expense
        lowest_expense = min(expenses, key=lambda x: x["amount"])
        print(f" Lowest Expense: ${lowest_expense['amount']:.2f} - {lowest_expense['description']}")
        
        # Average expense
        avg_expense = sum(t["amount"] for t in expenses) / len(expenses)
        print(f" Average Expense: ${avg_expense:.2f}")
        
        # Most used category (using dictionary to count)
        category_count = {}
        for trans in expenses:
            cat = trans["category"]
            category_count[cat] = category_count.get(cat, 0) + 1
        
        most_used = max(category_count.items(), key=lambda x: x[1])
        print(f" Most Used Category: {most_used[0]} ({most_used[1]} transactions)")
    
    # Recurring transactions count
    recurring_count = sum(1 for t in transactions if t["is_recurring"])
    print(f" Recurring Transactions: {recurring_count}")
    
    input("\nPress Enter to continue...")


# ==================================
# MAIN MENU FUNCTION
# =================================

def main_menu():
    """
    Display and handle main menu
    Demonstrates: While loop, conditional logic, function calls
    """
    # Try to load existing data
    load_data()
    
    # If no user profile, setup first
    if not user_profile["name"]:
        setup_user_profile()
        setup_budget_categories()
    
    while True:
        clear_screen()
        display_header(f" PERSONAL BUDGET TRACKER - {user_profile['name']}")
        
        print("\n1.  Add Transaction")
        print("2.  View All Transactions")
        print("3.  View Transactions by Category")
        print("4.  Financial Summary")
        print("5.  Search Transactions")
        print("6.  Delete Transaction")
        print("7.  Statistics & Insights")
        print("8.  Update Budget Categories")
        print("9.  Save Data")
        print("10. Exit")
        
        choice = get_int_input("\nSelect option (1-10): ", 1, 10)
        
        if choice == 1:
            add_transaction()
        elif choice == 2:
            view_all_transactions()
        elif choice == 3:
            view_transactions_by_category()
        elif choice == 4:
            display_financial_summary()
        elif choice == 5:
            search_transactions()
        elif choice == 6:
            delete_transaction()
        elif choice == 7:
            display_statistics()
        elif choice == 8:
            setup_budget_categories()
        elif choice == 9:
            save_data()
            input("\nPress Enter to continue...")
        elif choice == 10:
            save_choice = input("\nSave data before exiting? (y/n): ").lower()
            if save_choice == 'y':
                save_data()
            print("\n Thank you for using Budget Tracker! Goodbye!")
            break


# ========================
# PROGRAM ENTRY POINT
# ========================

if __name__ == "__main__":
    main_menu()
