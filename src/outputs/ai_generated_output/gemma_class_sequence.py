class Customer:
    def __init__(self, customerId: int, name: str, email: str, address: str):
        self.customerId = customerId
        self.name = name
        self.email = email
        self.address = address

    def login(self):
        pass

    def addToCart(self):
        pass

    def checkOut(self):
        pass

    def viewOrderHistory(self):
        pass


class CartItem:
    def __init__(self, quantity: int, subtotal: float):
        self.quantity = quantity
        self.subtotal = subtotal

    def calculateSubtotal(self):
        pass


class Cart:
    def __init__(self, cartId: int, totalAmount: float):
        self.cartId = cartId
        self.totalAmount = totalAmount
        self.items = []  # List of CartItem

    def addItem(self, item: CartItem):
        pass

    def removeItem(self, item: CartItem):
        pass

    def caltucateTotal(self):
        pass

    def clearCart(self):
        pass


class Product:
    def __init__(self, productId: int, name: str, price: float, stockQuantity: int):
        self.productId = productId
        self.name = name
        self.price = price
        self.stockQuantity = stockQuantity

    def checkAvailability(self) -> bool:
        return True

    def updateStock(self):
        pass


class Order:
    def __init__(self, orderId: int, orderDate: str, status: str, totalAmount: float):
        self.orderId = orderId
        self.orderDate = orderDate
        self.status = status
        self.totalAmount = totalAmount

    def createOrder(self):
        pass

    def confirmOrder(self):
        pass

    def cancelOrder(self):
        pass


class Payment:
    def __init__(self, paymentId: int, amount: float, status: str):
        self.paymentId = paymentId
        self.amount = amount
        self.status = status

    def processPayment(self) -> str:
        return "success"

    def refundPayment(self):
        pass


class Inventory:
    def __init__(self, inventoryId: int):
        self.inventoryId = inventoryId

    def checkStock(self) -> bool:
        return True

    def reserveProduct(self):
        pass

    def updateInventory(self):
        pass


class Shipping:
    def __init__(self, shippingId: int, address: int, status: str):
        self.shippingId = shippingId
        self.address = address
        self.status = status

    def createShipment(self):
        pass

    def updateShippingStatus(self):
        pass


class Notification:
    def __init__(self, notificationId: int, message: str):
        self.notificationId = notificationId
        self.message = message

    def sendConfirmation(self):
        pass

    def sendPaymentFailure(self):
        pass

    def sendOutOfStock(self):
        pass


def run_checkout_process(customer: Customer, cart: Cart, products: list[Product], inventory: Inventory,
                         payment_system: Payment, shipping_system: Shipping, notification_system: Notification):
    # Sequence Diagram Logic
    customer.checkOut()

    # Loop: each cart item
    for item in cart.items:
        cart.caltucateTotal()
        # Note: The sequence diagram shows Product.checkAvailability() being called
        # in relation to cart items, though the exact sender/receiver is implied.
        # We assume the system checks availability for the product in the item.
        for product in products:
            if product.checkAvailability():
                if inventory.checkStock():
                    # [all items available]
                    payment_status = payment_system.processPayment()

                    if payment_status == "success":
                        # [payment successful]
                        order = Order(1, "2023-10-27", "confirmed", cart.totalAmount)
                        order.createOrder()
                        order.confirmOrder()

                        # Update stock for each cart item
                        for product in products:
                            product.updateStock()
                            inventory.updateInventory()

                        shipping_system.createShipment()
                        shipment_created = True  # Mock return

                        if shipment_created:
                            order.createOrder()  # Sequence diagram shows createOrder again
                            notification_system.sendConfirmation()
                            cart.clearCart()
                    else:
                        # [payment failed]
                        notification_system.sendPaymentFailure()
                else:
                    # [out of stock]
                    notification_system.sendOutOfStock()
            else:
                # Inconsistency: Sequence diagram implies a flow for availability
                # but doesn't explicitly define the 'else' for checkAvailability
                # other than the 'out of stock' notification.
                pass

        # If loop finishes without returning, it implies the items were processed.
        # The sequence diagram structure is complex; this is a simplified mapping.

# Note: The sequence diagram contains nested 'alt' and 'loop' fragments
# that are interpreted here to represent the logical flow of a checkout transaction.