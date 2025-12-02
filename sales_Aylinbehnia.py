from products_Aylinbehnia import Product
from tabulate import tabulate
from rich.console import Console
from rich.table import Table

console = Console() #Create a color console

class SalesManager:
    def __init__(self):
        self.sales = [] #A list that will store sales history.
        self.products = {
            "juice": Product("juice", 150, 100, 10),
            "chocolate": Product("chocolate", 20, 10, 50),
            "cheese": Product("cheese", 80, 50, 30)
        }

    def add_product(self, name, price, cost, stock, category=None):
        """Add a new product to the inventory"""
        self.products[name.lower()] = Product(name, price, cost, stock, category) #The new product is stored in the dictionary as a key-value pair.

    def sell_product(self, product_name, quantity):
        """Process the sale of a product"""
        product_name = product_name.lower()
        if product_name in self.products: #It is checked whether the imported product exists or not.
            product = self.products[product_name]
            if product.update_stock(-quantity): #Checks if there is enough stock
                profit = product.calculate_profit(quantity) #Profit from product sales is calculated.
                self.sales.append({"product": product.name, "quantity": quantity, "profit": profit}) #Sales information is added to the list.
                console.print(f"[green]Sale successful![/] Profit: [bold]${profit}[/]") #A success message is printed to the console.
            else:
                console.print("[red]Insufficient stock![/]") #Error message in case of shortage of stock
        else:
            console.print("[red]Product not found![/]") #Error message if product does not exist

    def total_profit(self):
        """Calculate the total profit"""
        total = sum(sale["profit"] for sale in self.sales) #Total profit from all sales
        console.print(f"\n[bold cyan]Total Profit: ${total}[/]")
        return total

    def get_product_list(self):
        """Get the list of products"""
        table = Table(title="Product List") #A new table is created.
        table.add_column("Name", style="bold yellow")
        table.add_column("Price", justify="right", style="cyan")
        table.add_column("Cost", justify="right", style="magenta")
        table.add_column("Stock", justify="right", style="green")
        
        for product in self.products.values(): #For each product in the dictionary a row is added to the table.
            table.add_row(product.name, str(product.price), str(product.cost), str(product.stock))
        
        console.print(table)

    def get_sales_history(self):
        """Get the sales history as a list of tuples for Tkinter"""
        if not self.sales:
            return [] #If no sales have been made, an empty list is returned.

        history = []
        for index, sale in enumerate(self.sales, start=1):
            history.append((index, sale["product"], sale["quantity"], sale["profit"])) 
            #These values ​​are stored in a tuple along with the index.

        return history