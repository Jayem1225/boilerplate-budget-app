class Category:
    ledger = []
    
    def __init__(self, name):
        self.name = name
        
    def __str__(self):
        summary = self.name.center(30, "*")
        for record in self.ledger:
            summary += "\n{:23}{:7.2f}".format(self.name, record["amount"])
        summary += "\nTotal: {.2f}".format(self.get_balance())
        return summary

    def deposit(self, amount, description):
        self.ledger.append({"amount":amount,"description":description})
        
    def withdraw(self, amount, description):
        if self.check_funds(amount):
            self.ledger.append({"amount":-abs(amount),"description":description})
            return True
        return False
        
    def get_balance(self):
        return sum([record["amount"] for record in self.ledger])
      
    def transfer(self, amount, to_category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {to_category.name}")
            to_category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False
     
    def check_funds(self, amount):
        return amount <= self.get_balance()
      
    def get_percent_withdrawn(self):
        withdrawn = 0.0
        for record in self.ledger:
            if record["amount"] < 0:
                withdrawn = withdrawn + abs(record["amount"])
        total_deposited = self.get_balance() + withdrawn
        return withdrawn/total_deposited * 100
                


def create_spend_chart(categories):
    chart = "Percentage spent by category"
    category_prcnts_rounded = {
        cat.name: round(cat.get_percent_withdrawn()/10)*10
        for cat in categories
    }
    for prcnt in range(100,-1,-10):
        # Y - Axis
        chart += "\n" + str(prcnt).rjust(3) + "|"
        # Chart Data
        for cat in categories:
            if round(category_prcnts_rounded[cat.name] >= prcnt):
                chart += " o "
            else:
                chart += "   "
    # Generate X - axis
    chart += "\n    "
    for cat in categories:
        chart += "---"
    chart += "-"
    # Generate X - axis labels
    max_cat_name_len = max([len(cat.name) for cat in categories])
    for i in range(0,max_cat_name_len):
        chart += "\n    "
        for cat in categories:
            if i < len(cat.name) - 1:
                chart += " {cat.name[i]} "
            else:
                chart += "   "
    return chart
      
