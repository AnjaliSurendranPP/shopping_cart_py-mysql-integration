import mysql.connector
# DATABASE CONNECTION
con = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Anjali94!",
    database="shopping_cart"
)
cursor = con.cursor()
cart = {}
# 1. DISPLAY PRODUCTS
def view_products():
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    print("\n--------- AVAILABLE PRODUCTS ---------")
    for p in products:
        print(f"ID: {p[0]} | Name: {p[1]} | Price: ₹{p[2]} | Stock: {p[3]}")
# 2. ADD TO CART
def add_to_cart():
    view_products()
    product_id = int(input("\nEnter product ID: "))
    quantity = int(input("Enter quantity: "))
    cursor.execute(
        "SELECT id, name, price, stock FROM products WHERE id=%s",
        (product_id,)
    )
    product = cursor.fetchone()
    if product is None:
        print("Product not found!")
        return
    if quantity <= 0:
        print("Quantity must be greater than zero!")
        return
    current_quantity = cart.get(product_id, {}).get("quantity", 0)
    if current_quantity + quantity > product[3]:
        print("Insufficient stock!")
        return
    if product_id in cart:

        cart[product_id]["quantity"] += quantity
    else:
        cart[product_id] = {
            "name": product[1],
            "price": float(product[2]),
            "quantity": quantity
        }
    print("Product added to cart successfully!")
# 3. VIEW CART
def view_cart():
    if not cart:
        print("\nYour cart is empty!")
        return
    total = 0
    print("\n--------- YOUR SHOPPING CART ---------")
    for pid, item in cart.items():
        subtotal = item["price"] * item["quantity"]
        print(
            f"ID: {pid} | {item['name']} | "
            f"Price: ₹{item['price']} | "
            f"Quantity: {item['quantity']} | "
            f"Subtotal: ₹{subtotal}"
        )
        total += subtotal
    print("--------------------------------------")
    print("Total Amount: ₹", total)
# 4. UPDATE QUANTITY
def update_quantity():
    view_cart()
    if not cart:
        return
    product_id = int(input("\nEnter product ID: "))
    if product_id not in cart:
        print("Product not in cart!")
        return
    quantity = int(input("Enter new quantity: "))
    cursor.execute(
        "SELECT stock FROM products WHERE id=%s",
        (product_id,)
    )
    stock = cursor.fetchone()[0]
    if quantity <= 0:
        print("Quantity must be greater than zero!")
        return
    if quantity > stock:
        print("Insufficient stock!")
        return
    cart[product_id]["quantity"] = quantity
    print("Cart updated successfully!")
# 5. REMOVE FROM CART
def remove_from_cart():
    view_cart()
    if not cart:
        return
    product_id = int(input("\nEnter product ID to remove: "))
    if product_id in cart:
        del cart[product_id]
        print("Product removed from cart!")
    else:
        print("Product not found in cart!")
# 6. CHECKOUT
def checkout():
    if not cart:
        print("Your cart is empty!")
        return
    customer_name = input("Enter customer name: ")
    total = sum(
        item["price"] * item["quantity"]
        for item in cart.values()
    )
    try:
        # SAVE ORDER
        cursor.execute(
            "INSERT INTO orders (customer_name, total_amount) VALUES (%s, %s)",
            (customer_name, total)
        )
        order_id = cursor.lastrowid
        # SAVE ORDER ITEMS AND UPDATE STOCK
        for pid, item in cart.items():
            cursor.execute(
                "SELECT stock FROM products WHERE id=%s FOR UPDATE",
                (pid,)
            )
            stock = cursor.fetchone()[0]
            if item["quantity"] > stock:
                raise ValueError(
                    f"Insufficient stock for {item['name']}"
                )
            cursor.execute(
                """INSERT INTO order_items
                (order_id, product_id, quantity, price)
                VALUES (%s, %s, %s, %s)""",
                (
                    order_id,
                    pid,
                    item["quantity"],
                    item["price"]
                )
            )
            cursor.execute(
                "UPDATE products SET stock = stock - %s WHERE id = %s",
                (item["quantity"], pid)
            )
        con.commit()
        print("\n========== BILL ==========")
        print("Order ID:", order_id)
        print("Customer:", customer_name)
        for item in cart.values():
            print(
                item["name"],
                "x", item["quantity"],
                "=", item["price"] * item["quantity"]
            )
        print("--------------------------")
        print("Total Amount: ₹", total)
        print("Thank you for shopping!")
        cart.clear()
    except Exception as e:
        con.rollback()
        print("Checkout failed:", e)
# MAIN MENU
while True:
    print("\n========== SHOPPING CART ==========")
    print("1. View Products")
    print("2. Add to Cart")
    print("3. View Cart")
    print("4. Update Quantity")
    print("5. Remove from Cart")
    print("6. Checkout")
    print("7. Exit")
    choice = input("\nEnter your choice: ")
    if choice == "1":
        view_products()
    elif choice == "2":
        add_to_cart()
    elif choice == "3":
        view_cart()
    elif choice == "4":
        update_quantity()
    elif choice == "5":
        remove_from_cart()
    elif choice == "6":
        checkout()
    elif choice == "7":
        print("Thank you!")
        break
    else:
        print("Invalid choice! Try again.")
cursor.close()
con.close()
