class Customer:
    def __init__(self, customerId, name, email, address):
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


class Cart:
    def __init__(self, cartId, totalAmount):
        self.cartId = cartId
        self.totalAmount = totalAmount

    def addItem(self):
        pass

    def removeItem(self):
        pass

    def calculateTotal(self):
        pass

    def clearCart(self):
        pass


class CartItem:
    def __init__(self, quantity, subtotal):
        self.quantity = quantity
        self.subtotal = subtotal

    def calculateSubtotal(self):
        pass


class Product:
    def __init__(self, productId, name, price, stockQuantity):
        self.productId = productId
        self.name = name
        self.price = price
        self.stockQuantity = stockQuantity

    def checkAvailability(self):
        pass

    def updateStock(self):
        pass


class Order:
    def __init__(self, orderId, orderDate, status, totalAmount):
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
    def __init__(self, paymentId, amount, status):
        self.paymentId = paymentId
        self.amount = amount
        self.status = status

    def processPayment(self):
        pass

    def refundPayment(self):
        pass


class Inventory:
    def __init__(self, inventoryId):
        self.inventoryId = inventoryId

    def checkStock(self):
        pass

    def reserveProduct(self):
        pass

    def updateInventory(self):
        pass


class Shipping:
    def __init__(self, shippingId, address, status):
        self.shippingId = shippingId
        self.address = address
        self.status = status

    def createShipment(self):
        pass

    def updateShippingStatus(self):
        pass


class Notification:
    def __init__(self, notificationId, message):
        self.notificationId = notificationId
        self.message = message

    def sendConfirmation(self):
        pass

    def sendPaymentFailure(self):
        pass

    def sendOutOfStock(self):
        pass


# Sequence implementation
def sequence(customer, cart, product, inventory, order, payment, shipping, notification):
    cart_total = customer.checkOut()
    cart_total = cart.calculateTotal()
    
    # loop eachCartItem
    for eachCartItem in cart.items:
        availability_result = cart.product.checkAvailability()
        stock_available = product.inventory.checkStock()
        return stock_available
        return availability_result
    
    # alt allItemsAvailable
    payment_status = cart.payment.processPayment()
    return payment_status
    
    # alt paymentSuccessful
    order_created = cart.order.createOrder()
    order_created = order.inventory.reserveProduct()
    
    # loop eachCartItem
    for eachCartItem in cart.items:
        inventory.product.updateStock()
    
    shipment_created = order.shipping.createShipment()
    return shipment_created
    order.notification.sendConfirmation()
    cart.clearCart()
    
    # else paymentFailed
    cart.notification.sendPaymentFailure()
    
    # else outOfStock
    cart.notification.sendOutOfStock()