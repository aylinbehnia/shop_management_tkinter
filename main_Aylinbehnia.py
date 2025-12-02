import os
os.system('cls')

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import PhotoImage
from sales_Aylinbehnia import SalesManager
from datetime import datetime

class ShopApp:
    def __init__(self, root):
        self.sales_manager = SalesManager()
        self.root = root
        root.iconbitmap('shopico.ico')
        self.root.title("Shop Management System")
        self.root.geometry("900x700")
        self.root.configure(bg="lightgreen")
        self.supermarket_img = PhotoImage(file="images.png")  #Add supermarket image
        self.img_label = tk.Label(self.root, image=self.supermarket_img, bg="white")
        self.img_label.pack(pady=10)

        self.header_label = tk.Label(root, text="Shop Management", font=("Lucida Bright", 22, "bold"), bg="darkblue", fg="white", pady=15)
        self.header_label.pack(fill=tk.X) #Header Label
        
        self.menu_frame = ttk.Frame(root, padding=20) #Main Frame
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        options = [
            ("View Products", self.view_products), # Create menu buttons
            ("Add Product", self.add_product),
            ("Sell Product", self.sell_product),
            ("View Sales History", self.view_sales),
            ("View Total Profit", self.view_profit)
        ]
        for text, command in options:
            button = ttk.Button(self.menu_frame, text=text, command=command, width=35, style="Custom.TButton")
            button.pack(pady=10)

        style = ttk.Style() #Custom style
        style.configure("Custom.TButton", font=("Lucida Bright", 12), padding=10, background="darkblue", foreground="green")

    
    def view_products(self):
        """Display product list in a Table (Treeview)"""
        product_window = tk.Toplevel(self.root)
        product_window.title("Available Products")
        product_window.iconbitmap('productsico.ico')
        product_window.geometry("600x400")

        tk.Label(product_window, text="Product List", background="darkblue",foreground="white", font=("Lucida Bright", 18, "bold")).pack(pady=10)
        columns = ("Name", "Price", "Cost", "Stock", "Category") #Create a table
        tree = ttk.Treeview(product_window, columns=columns, show="headings")
        
        for col in columns: #Setting column names
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for product in self.sales_manager.products.values(): #Add products to the table
            tree.insert("", "end", values=(product.name, product.price, product.cost, product.stock, product.category or "N/A"))

        tree.pack(pady=10, fill="both", expand=True)
        

    def view_sales(self):
        """Display sales history in a table format with Date & Time"""
        sales_window = tk.Toplevel(self.root)
        sales_window.title("Sales History")
        sales_window.iconbitmap('historyico.ico')
        sales_window.geometry("700x450")
        sales_window.config(bg="lightgreen")

        header_label = tk.Label(sales_window, text="📜 Sales History", font=("Lucida Bright", 16, "bold"), bg="darkblue", fg="white", pady=10)
        header_label.pack(fill=tk.X)

        columns = ("ID", "Product", "Quantity", "Profit", "Date", "Time") #table
        treeview = ttk.Treeview(sales_window, columns=columns, show="headings")

        for col in columns: #Set column titles
            treeview.heading(col, text=col, anchor=tk.CENTER)
            treeview.column(col, anchor=tk.CENTER, width=100)

        treeview.tag_configure("oddrow", background="white")
        treeview.tag_configure("evenrow", background="#d5f5e3")

        scrollbar = ttk.Scrollbar(sales_window, orient="vertical", command=treeview.yview)
        treeview.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        treeview.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        sales_list = self.sales_manager.get_sales_history() # Get sales information from sales_manager

        if not sales_list:
            treeview.insert("", tk.END, values=("No sales recorded", " ", " ", " ", " ", " "))
        else:
            for index, sale in enumerate(sales_list):
                if len(sale) == 4:  # در صورتی که timestamp وجود ندارد
                    sale_id, product, quantity, profit = sale
                    timestamp = datetime.now().timestamp()  # مقدار فعلی را بگذارید
                else:
                    sale_id, product, quantity, profit, timestamp = sale
                
                sale_date = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
                sale_time = datetime.fromtimestamp(timestamp).strftime("%H:%M:%S")
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                treeview.insert("", tk.END, values=(sale_id, product, quantity, profit, sale_date, sale_time), tags=(tag,))

    def view_profit(self):
        """Display total profit"""
        total_profit = self.sales_manager.total_profit()
        messagebox.showinfo("Total Profit", f"Total Profit: ${total_profit}")

    def add_product(self):
        """Add new product form with additional UI elements"""
        def submit():
            try:
                name = name_entry.get().strip()
                price = float(price_entry.get().strip())
                cost = float(cost_entry.get().strip())
                stock = int(stock_spinbox.get())  #Get value from Spinbox
                category = category_combobox.get()  #Get category from Combobox
                self.sales_manager.add_product(name, price, cost, stock, category)
                messagebox.showinfo("Success", "Product added successfully!")
                add_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Enter valid values.")

        add_window = tk.Toplevel(self.root)
        add_window.title("Add Product")
        add_window.iconbitmap('addico.ico')
        add_window.geometry("350x400")
        
        tk.Label(add_window, text="Product Name:", font=("Lucida Bright", 12)).pack(pady=5)
        name_entry = tk.Entry(add_window, font=("Lucida Bright", 12), width=30)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Category:", font=("Lucida Bright", 12)).pack(pady=5)
        category_combobox = ttk.Combobox(add_window, values=["None","Beverages","Bread","Food","Fruits","Snacks"], state="readonly")
        category_combobox.pack(pady=5)
        category_combobox.current(0)

        tk.Label(add_window, text="Price:", font=("Lucida Bright", 12)).pack(pady=5)
        price_entry = tk.Entry(add_window, font=("Lucida Bright", 12), width=30)
        price_entry.pack(pady=5)

        tk.Label(add_window, text="Cost:", font=("Lucida Bright", 12)).pack(pady=5)
        cost_entry = tk.Entry(add_window, font=("Lucida Bright", 12), width=30)
        cost_entry.pack(pady=5)

        tk.Label(add_window, text="Stock:", font=("Lucida Bright", 12)).pack(pady=5)
        stock_spinbox = tk.Spinbox(add_window, from_=0, to=1000, font=("Lucida Bright", 12), width=30)  # Spinbox for stock
        stock_spinbox.pack(pady=5)

        ttk.Button(add_window, text="Add Product", command=submit, width=20, style="Custom.TButton").pack(pady=10)

    def sell_product(self):
        """Sell a product"""
        def submit():
            product_name = name_entry.get().strip()
            try:
                quantity = int(quantity_spinbox.get())  #Get value from Spinbox
                result = self.sales_manager.sell_product(product_name, quantity)
                messagebox.showinfo("Success", "Product sold successfully!")
                # messagebox.showinfo("Sale Result", result)
                sell_window.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid quantity. Enter a number.")

        sell_window = tk.Toplevel(self.root)
        sell_window.title("Sell Product")
        sell_window.iconbitmap('sellico.ico')
        sell_window.geometry("350x250")

        tk.Label(sell_window, text="Product Name:", font=("Lucida Bright", 12)).pack(pady=5)
        name_entry = tk.Entry(sell_window, font=("Lucida Bright", 12), width=30)
        name_entry.pack(pady=5)

        tk.Label(sell_window, text="Quantity:", font=("Lucida Bright", 12)).pack(pady=5)
        quantity_spinbox = tk.Spinbox(sell_window, from_=1, to=1000, font=("Lucida Bright", 12), width=30)  # Spinbox for quantity
        quantity_spinbox.pack(pady=5)

        ttk.Button(sell_window, text="Sell", command=submit, width=20, style="Custom.TButton").pack(pady=10)

if __name__ == "__main__": #Program execution
    root = tk.Tk()
    app = ShopApp(root)
    root.mainloop()