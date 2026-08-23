# Class definitions as per the CLASS DIAGRAM
class Customer:
    def __init__(self, customer_id: int, name: str, email: str, address: str):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.address = address

    def login(self) -> None:
        # placeholder for login logic
        pass

    def addToCart(self, cart: "Cart", item) -> None:
        # placeholder for adding an item to the cart
        pass

    def checkOut(self) -> None:
        # placeholder for checkout logic
        pass

    def viewOrderHistory(self) -> None:
        # placeholder for viewing order history
        pass


class Cart:
    def __init__(self, cart_id: int):
        self.cart_id = cart_id
        self.items: list = []
        self.total_amount: float = 0.0

    def addItem(self, product: "Product", quantity: int) -> None:
        # placeholder for adding an item to the cart
        pass

    def removeItem(self, product: "Product") -> None:
        # placeholder for removing an item from the cart
        pass

    def calculateTotal(self) -> float:
        # placeholder for calculating total amount
        return self.total_amount

    def clearCart(self) -> None:
        self.items = []
        self.total_amount = 0.0


class CartItem:
    def __init__(self, product: "Product", quantity: int):
        self.product = product
        self.quantity = quantity
        self.subtotal: float = product.price * quantity

    def calculateSubtotal(self) -> float:
        return self.subtotal


class Product:
    def __init__(self, product_id: int, name: str, price: float, stock_quantity: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def checkAvailability(self, quantity: int) -> bool:
        return self.stock_quantity >= quantity

    def updateStock(self, delta: int) -> None:
        self.stock_quantity += delta

    def updateStock(self) -> None:
        # placeholder to satisfy diagram method name
        pass


class Order:
    def __init__(self, order_id: int, order_date: str, status: str):
        self.order_id = order_id
        self.order_date = order_date
        self.status = status
        self.total_amount: float = 0.0

    def createOrder(self) -> None:
        # placeholder for creating an order
        pass

    def confirmOrder(self) -> None:
        # placeholder for confirming an order
        pass

    def cancelOrder(self) -> None:
        # placeholder for cancelling an order
        pass


class Payment:
    def __init__(self, payment_id: int, amount: float, status: str):
        self.payment_id = payment_id
        self.amount = amount
        self.status = status

    def processPayment(self) -> None:
        # placeholder for processing payment
        pass

    def refundPayment(self) -> None:
        # placeholder for refunding payment
        pass


class Shipping:
    def __init__(self, shipping_id: int, address: str, status: str):
        self.shipping_id = shipping_id
        self.address = address
        self.status = status

    def createShipment(self) -> None:
        # placeholder for creating a shipment
        pass

    def updateShippingStatus(self) -> None:
        # placeholder for updating shipment status
        pass


class Notification:
    def __init__(self, notification_id: int, message: str):
        self.notification_id = notification_id
        self.message = message

    def sendConfirmation(self) -> None:
        # placeholder for sending confirmation
        pass

    def sendPaymentFailure(self) -> None:
        # placeholder for sending payment failure
        pass

    def sendOutOfStock(self) -> None:
        # placeholder for sending out‑of‑stock notification
        pass


class Inventory:
    def __init__(self, inventory_id: int):
        self.inventory_id = inventory_id
        self.products: dict = {}

    def checkStock(self, product_id: int) -> bool:
        return self.products.get(product_id, 0) > 0

    def reserveProduct(self, product_id: int, quantity: int) -> None:
        # placeholder for reserving a product
        pass

    def updateInventory(self) -> None:
        # placeholder for updating inventory
        pass


# Runtime behavior as per the SEQUENCE DIAGRAM
def main() -> None:
    # Participants
    customer = Customer(1, "Alice", "alice@example.com", "123 Main St")
    cart = Cart(101)
    product = Product(2001, "Widget", 19.99, 10)
    inventory = Inventory(1)
    order = Order(3001, "2023-09-01", "pending")
    payment = Payment(4001, 0.0, "pending")
    shipping = Shipping(5001, "123 Main St", "pending")
    notification = Notification(6001, "Your order is confirmed")

    # Customer logs in (initial call)
    customer.login()

    # ------------------------------------------------------------------
    # ALT fragment: stock availability check
    # ------------------------------------------------------------------
    # The sequence expects a check for availability; we use Product.checkAvailability.
    # If not available, we send an out‑of‑stock notification and exit.
    if not product.checkAvailability(2):
        # Out‑of‑stock branch
        notification.sendOutOfStock()
        return  # early exit

    # ------------------------------------------------------------------
    # LOOP fragment: process each cart item
    # ------------------------------------------------------------------
    # Simulated list of items to purchase
    items_to_buy = [
        ("Widget", 2),
        ("Gadget", 1)  # assume Gadget product exists elsewhere
    ]

    for name, qty in items_to_buy:
        # Resolve product (simplified lookup)
        if name == "Widget":
            prod = product
        else:
            # Placeholder for other products
            continue

        # Check stock before adding
        if not prod.checkAvailability(qty):
            notification.sendOutOfStock()
            return

        # Add item to cart (loop body)
        cart.addItem(prod, qty)

        # Update product stock (reserve and decrement)
        prod.updateStock(-qty)
        inventory.reserveProduct(prod.product_id, qty)

    # ------------------------------------------------------------------
    # Optional (OPT) step: calculate total (could be omitted)
    # ------------------------------------------------------------------
    # This step is optional; we call it for completeness.
    cart.calculateTotal()

    # ------------------------------------------------------------------
    # Parallel (PAR) steps: create order and process payment
    # ------------------------------------------------------------------
    # In the diagram these could run in parallel; here we execute sequentially.
    order.createOrder()
    payment.processPayment()

    # ------------------------------------------------------------------
    # Further steps following the sequence
    # ------------------------------------------------------------------
    # Reserve the product (already done in the loop)
    # Update inventory (placeholder)
    inventory.updateInventory()

    # Create shipment and update its status
    shipping.createShipment()
    shipping.updateShippingStatus()

    # Send confirmation to the customer
    notification.sendConfirmation()

    # ------------------------------------------------------------------
    # End of scenario
    # ------------------------------------------------------------------

if __name__ == "__main__":
    main()

# Note: The sequence diagram references a "stockAvailable" message that is not
# explicitly defined as a method in the class diagram; we used Product.checkAvailability
# instead, preserving the class diagram structure while indicating the semantic
# mismatch with this comment.