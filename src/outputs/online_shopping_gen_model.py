class Customer:
    def __init__(self):
        self.customerId = None
        self.name = None
        self.email = None
        self.address = None

    def login(self):
        pass

    def addToCart(self):
        pass

    def checkOut(self):
        pass

    def viewOrderHistory(self):
        pass

class Cart:
    def __init__(self):
        self.cartId = None
        self.totalAmount = None

    def addItem(self):
        pass

    def removeItem(self):
        pass

    def caltucateTotal(self):
        pass

    def clearCart(self):
        pass

class CartItem:
    def __init__(self):
        self.quantity = None
        self.subtotal = None

    def calculateSubtotal(self):
        pass

class Product:
    def __init__(self):
        self.productId = None
        self.name = None
        self.price = None
        self.stockQuantity = None

    def checkAvailability(self):
        pass

    def updateStock(self):
        pass

class Order:
    def __init__(self):
        self.orderId = None
        self.orderDate = None
        self.status = None
        self.totalAmount = None

    def createOrder(self):
        pass

    def confirmOrder(self):
        pass

    def cancelOrder(self):
        pass

class Payment:
    def __init__(self):
        self.paymentId = None
        self.amount = None
        self.status = None

    def processPayment(self):
        pass

    def refundPayment(self):
        pass

class Inventory:
    def __init__(self):
        self.inventoryId = None

    def checkStock(self):
        pass

    def reserveProduct(self):
        pass

    def updateInventory(self):
        pass

class Shipping:
    def __init__(self):
        self.shippingId = None
        self.address = None
        self.status = None

    def createShipment(self):
        pass

    def updateShippingStatus(self):
        pass

class Notification:
    def __init__(self):
        self.notificationId = None
        self.message = None

    def sendConfirmation(self):
        pass

    def sendPaymentFailure(self):
        pass

    def sendOutOfStock(self):
        pass


def run_sequence():
    customer = Customer()
    cart = Cart()
    product = Product()
    inventory = Inventory()
    order = Order()
    payment = Payment()
    shipping = Shipping()
    notification = Notification()

    condition = False
    eachCartItem = False
    paymentSuccessful = False

    customer.checkOut()
    cart.calculateTotal()
    while condition:
        product.checkAvailability()
        inventory.checkStock()
    if paymentSuccessful:
        payment.processPayment()
        if eachCartItem:
            order.createOrder()
            while condition:
                product.updateStock()
            shipping.createShipment()
            notification.sendConfirmation()
            cart.clearCart()
            notification.sendPaymentFailure()
    else:
        notification.sendOutOfStock()

if __name__ == '__main__':
    run_sequence()
