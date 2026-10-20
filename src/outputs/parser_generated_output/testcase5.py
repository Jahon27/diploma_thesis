class Customer:
    def __init__(self):
        self.customerId = None

    def startPayment(self):
        pass

    def showSuccess(self):
        pass

    def showFailure(self):
        pass

class Payment:
    def __init__(self):
        self.paymentId = None
        self.amount = None
        self.status = None

    def processPayment(self):
        pass

class PaymentGateway:
    def authorizePayment(self):
        pass

class FraudService:
    def checkTransaction(self):
        pass

class Order:
    def __init__(self):
        self.orderId = None
        self.status = None

    def confirmOrder(self):
        pass

class Notification:
    def __init__(self):
        self.message = None

    def sendConfirmation(self):
        pass

    def sendPaymentFailure(self):
        pass


def run_sequence(transactionValid, paymentAuthorized):
    payment = Payment()
    fraudservice = FraudService()
    paymentgateway = PaymentGateway()
    order = Order()
    notification = Notification()
    customer = Customer()

    customer.startPayment()
    payment.processPayment()
    fraudservice.checkTransaction()
    if transactionValid:
        paymentgateway.authorizePayment()
        if paymentAuthorized:
            order.confirmOrder()
            notification.sendConfirmation()
            customer.showSuccess()
        else:
            notification.sendPaymentFailure()
            customer.showFailure()
    else:
        notification.sendPaymentFailure()
        customer.showFailure()
