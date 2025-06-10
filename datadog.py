import json
import os
from typing import Dict, Any


DATA_FILE = "budget_data.json"


class BudgetCategory:
    def __init__(self, name: str, limit: float) -> None:
        """
        Initializes a new budget category.

        Args:
            name: The name of the category (e.g., 'food').
            limit: The budget limit for this category.
        """
        self.name: str = name
        self.limit: float = limit
        self.spent: float = 0.0

    """def set_spending_budget(self, income: float, percentage: float) -> None:
        
        Sets the spending budget based on income and percentage.

        Args:
            income: The total income amount.
            percentage: The percentage of income to allocate to this category.
        
        income = input("What is your total income? ").strip()
        percent = input(f"What percentage of your total income would you like to allocate towards spending? (ex. 20 for 20%)").strip()
        try:
            percentage = float(percent)
            if percentage < 0 or percentage > 100 or :
                raise ValueError("The percentage must be between 0 and 100.")
        except ValueError as e:
            print(f"⚠️ Invalid percentage: {e}")
            return
        


        self.limit = income * (percentage / 100)
        print(f"💰 Set budget limit for '{self.name}' to ${self.limit:.2f} based on {percentage}% of ${income:.2f} income.")"""


    def add_expense(self, amount: float) -> None:
        """
        Adds an expense to the category.

        Args:
            amount: The amount to add to the category's spending.
        """
        if self.spent + amount > self.limit:
            print(f"⚠️ Warning: Adding ${amount} exceeds the budget limit for '{self.name}'. Would you still like to proceed?")
            proceed = input("Type 'yes' to proceed or 'no' to cancel: ").strip().lower()
            if proceed == 'yes':
                self.spent += amount
            elif proceed == 'no':
                print("🚫 Expense not added.")
                return
        else:
            self.spent += amount

    def remaining(self) -> float:
        """
        Calculates how much budget is left in this category.

        Returns:
            The remaining amount of money in the category.
        """
        if self.spent > self.limit:
            print(f"⚠️ Warning: You have exceeded the budget for '{self.name}'!")

        return self.limit - self.spent

    def to_dict(self) -> Dict[str, Any]:
        """
        Converts the category data into a dictionary for saving.

        Returns:
            Dictionary containing name, limit, and spent values.
        """
        return {
            "name": self.name,
            "limit": self.limit,
            "spent": self.spent
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "BudgetCategory":
        """
        Creates a BudgetCategory from a dictionary.

        Args:
            data: A dictionary with keys 'name', 'limit', and 'spent'.

        Returns:
            A populated BudgetCategory instance.
        """
        category = BudgetCategory(data["name"], data["limit"])
        category.spent = data["spent"]
        return category


class BudgetManager:
    def __init__(self) -> None:
        """
        Initializes the BudgetManager and loads data from disk.
        """
        self.categories: Dict[str, BudgetCategory] = {}
        self.load_data()

    def add_category(self, name: str, limit: float) -> None:
        """
        Adds a new category to the budget.

        Args:
            name: Name of the category.
            limit: Budget limit for the category.
        """
        # check if category already exists or if capitalized version exists
        name = name.strip().lower()
        if name in self.categories or name == "":
            print(f"🐶 Category '{name}' already exists!")
        else:
            help = input(f"Would you like help setting a budget limit for '{name}'? Type 'yes' to proceed or 'no' if you have a set value in mind: ").strip().lower()
            if help == 'yes':
                income = input("What is your total income? ").strip()
                percent = input(f"What percentage of your total income would you like to allocate towards '{name}'? (ex. 20 for 20%) ").strip()
                try:
                    percentage = float(percent)
                    if percentage < 0 or percentage > 100:
                        raise ValueError("The percentage must be between 0 and 100.")
                except ValueError as e:
                    print("Invalid percentage. Please enter a valid number between 0 and 100.")
                    return
                try:
                    income = float(income)
                    if income < 0:
                        raise ValueError("Income cannot be negative.")
                except ValueError as e:
                    print("Invalid income. Please enter a valid number.")
                    return
                limit = income * (percentage / 100)
                self.categories[name] = BudgetCategory(name, limit)
                print(f"📊 Added new category: {name} with limit ${limit}")
            else:
                if limit < 0:
                    print("⚠️ Budget limit cannot be negative. Please enter a valid limit.")
                    return
                else:
                    self.categories[name] = BudgetCategory(name, limit)
                    print(f"📊 Added new category: {name} with limit ${limit}")

    def add_expense(self, name: str, amount: float) -> None:
        """
        Adds an expense to an existing category.

        Args:
            name: Category name.
            amount: Expense amount to add.
        """
        if name in self.categories:
            self.categories[name].add_expense(amount)
            print(f"💸 Added expense of ${amount} to '{name}'")
        else:
            print(f"🚫 No such category: {name}")
    
    def remove_category(self, name: str) -> None:
        """
        Removes a category from the budget.

        Args:
            name: Name of the category to remove.
        """

        if name in self.categories:
            confirmation = input(f"Are you sure you want to remove the category '{name}?' Type 'yes' to confirm: ").strip().lower()
            if confirmation != 'yes':
                print("🚫 Category removal cancelled.")
                return
            else:
                del self.categories[name]
                print(f"🗑️ Removed category: {name}")
        else:
            print(f"🚫 No such category: {name}")

    def show_summary(self) -> None:
        """
        Displays a summary of all budget categories and their spending.
        """

        """
        Displays a summary of all budget categorie and their spending in table format.
        """
        print("\n🐾 Budget Summary (Table View)"
              "\n" + "-" * 70)
        print(f"{'Category':<20} {'Spent':<10} {'Limit':<10} {'Remaining':<10}")    
        print("-" * 70)
        for category in self.categories.values():
            remaining = category.remaining()
            print(f"{category.name:<20} ${category.spent:<10.2f} ${category.limit:<10.2f} ${remaining:<10.2f}")
            print("-" * 70)
            total_spent = sum(cat.spent for cat in self.categories.values())
        print(f"Total Spent: ${total_spent:.2f}")
        

    def save_data(self) -> None:
        """
        Saves all budget data to a JSON file.
        """
        with open(DATA_FILE, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.categories.items()}, f)

    def load_data(self) -> None:
        """
        Loads budget data from a JSON file if it exists.
        """
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                data = json.load(f)
                self.categories = {k: BudgetCategory.from_dict(v) for k, v in data.items()}


def main() -> None:
    """
    Main CLI loop. Handles user interaction and command selection.
    """
    print("🐶 Welcome to the Datadog Budget Tracker CLI!")
    manager = BudgetManager()

    while True:
        print("Choose an option:")
        print("1. Add a new category")
        print("2. Remove a category")
        print("3. Add an expense")
        print("4. Show summary")
        print("5. Save & Exit")

        choice: str = input("Enter choice (1-5): ").strip()

        if choice == "1":
            name = input("Enter category name (e.g., dog treats): ").strip()
            try:
                limit = float(input(f"Enter budget limit for '{name}': "))
                manager.add_category(name, limit)
            except ValueError:
                print("⚠️ Please enter a valid number.")
        elif choice == "2":
            name = input("Enter category name to remove: ").strip()
            manager.remove_category(name)
        elif choice == "3":
            name = input("Enter category name: ").strip()
            try:
                amount = float(input("Enter expense amount: "))
                manager.add_expense(name, amount)
            except ValueError:
                print("⚠️ Please enter a valid number.")
        elif choice == "4":
            manager.show_summary()
        elif choice == "5":
            manager.save_data()
            print("✅ Budget saved. Keep your tail wagging!")
            break
        else:
            print("❓ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()