class Customer:
    def checkout(self, cart):
        pass

class Cart:
    def calculateTotal(self):
        pass

    def clearCart(self):
        pass

class Product:
    def checkAvailability(self):
        pass

    def checkStock(self):
        pass

class Inventory:
    def stockAvailable(self):
        pass

    def updateStock(self):
        pass

class Order:
    def createOrder(self):
        pass

    def createShipment(self):
        pass

    def sendConfirmation(self):
        pass

class Payment:
    def processPayment(self):
        pass

    def paymentStatus(self):
        pass

class Shipping:
    def shipmentCreated(self):
        pass

class Notification:
    def sendPaymentFailure(self):
        pass

    def sendOutOfStock(self):
        pass

def execute_checkout_process(customer, cart, product, inventory, order, payment, shipping, notification):
    customer.checkout(cart)
    cart.calculateTotal()
    
    # loop [each cart item]
    for item in cart:
        cart.checkAvailability(product)
        product.checkStock(inventory)
        if inventory.stockAvailable():
            # alt [all items available]
            payment.processPayment()
            if payment.paymentStatus() == "successful":
                # alt [payment successful]
                order.createOrder()
                order.createOrder()
                for item in cart:
                    inventory.updateStock()
                order.createShipment()
                if shipping.shipmentCreated():
                    order.sendConfirmation()
                    cart.clearCart()
            else:
                # alt [payment failed]
                cart.sendPaymentFailure(notification)
        else:
            # alt [out of stock]
            cart.sendOutOfStock(notification)