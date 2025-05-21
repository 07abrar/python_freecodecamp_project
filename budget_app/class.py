class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = ""
        for entry in self.ledger:
            desc = entry["description"][:23]
            amt = f"{entry['amount']:.2f}"
            items += f"{desc:<23}{amt:>7}\n"
        total = f"Total: {self.get_balance():.2f}"
        return title + items + total

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()


def create_spend_chart(categories):
    spent = [
        sum(-item["amount"] for item in cat.ledger if item["amount"] < 0)
        for cat in categories
    ]
    total_spent = sum(spent)
    # Calculate percentage spent per category, rounded down to nearest 10
    percentages = [int((s / total_spent) * 100) // 10 * 10 for s in spent]
    chart = "Percentage spent by category\n"
    # Bar chart
    for i in range(100, -1, -10):
        line = f"{i:>3}|"
        for perc in percentages:
            line += " o " if perc >= i else "   "
            line += "  "  # 2 spaces after each bar
        chart += line.rstrip() + "\n"
    # Dashes: 3 per category, plus 2 extra
    chart += "    " + ("-" * (len(categories) * 3 + 2)) + "\n"
    # Category names vertically
    names = [cat.name for cat in categories]
    max_len = max(len(name) for name in names)
    for i in range(max_len):
        line = "     "
        for name in names:
            line += (name[i] if i < len(name) else " ") + "  "  # 2 spaces after each letter
        chart += line.rstrip() + ("\n" if i < max_len - 1 else "")
    return chart.rstrip("\n")


if __name__ == "__main__":
    food = Category("Food")
    food.deposit(1000, "initial deposit")
    food.withdraw(10.15, "groceries")
    food.withdraw(15.89, "restaurant and more food for dessert")
    clothing = Category("Clothing")
    auto = Category("Auto")
    food.transfer(50, clothing)
    clothing.withdraw(25.55, "clothes")
    clothing.withdraw(100, "shoes")
    auto.deposit(1000, "initial deposit")
    auto.withdraw(15, "gasoline")
    print(food)
    print(clothing)
    print(auto)
    print(create_spend_chart([food, clothing, auto]))