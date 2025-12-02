class Product:
    def __init__(self, name, price, cost, stock, category=None):  #Added category to the class
        self.name = name
        self.price = price  #Selling price
        self.cost = cost  #Purchase cost
        self.stock = stock  # Stock available
        self.category = category  #Category

    def update_stock(self, quantity):
        """Update the product stock"""
        if self.stock + quantity >= 0:
            self.stock += quantity
            return True
        else:
            return False

    def calculate_profit(self, quantity_sold):
        """Calculate profit for the sold quantity"""
        return (self.price - self.cost) * quantity_sold

    def __str__(self): #To display product information
        return f"{self.name} - Price: ${self.price} | Stock: {self.stock} | Category: {self.category if self.category else 'N/A'}"