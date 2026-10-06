class Customer:
    def __init__(self):
        self._customerId = 0  # private attribute

    def startPayment(self):
        """Orchestrates the payment process."""
        payment = Payment()
        payment.processPayment(self)

    def showSuccess(self):
        """Indicates a successful payment."""
        print("Payment successful")

    def showFailure(self):
        """Indicates a failed payment."""
    def showFailure(self):
        """Indicates a failed payment."""
        print("Payment failed")


class Payment:
    def __init__(self):
        self._paymentId = 0   # private attribute
        self._amount = 0      # private attribute
        self._status = ""     # private attribute

    def processPayment(self, customer):
        """
        Processes the payment by interacting with FraudService,
        PaymentGateway, Order, and Notification, and finally
        informs the Customer of the outcome.
        """
        fraud_service = FraudService()
        transaction_valid = fraud_service.checkTransaction()

        if transaction_valid:
            gateway = PaymentGateway()
            payment_authorized = gateway.authorizePayment()

            if payment_authorized:
                order = Order()
                order.confirmOrder()
                notification = Notification()
                notification.sendConfirmation()
                customer.showSuccess()
            else:
                notification = Notification()
                notification.sendPaymentFailure()
                customer.showFailure()
        else:
            notification = Notification()
            notification.sendPaymentFailure()
            customer.showFailure()


class FraudService:
    def __init__(self):
        pass

    def checkTransaction(self):
        """
        Simulates transaction validation.
        In a real system this would contain fraud detection logic.
        """
        # Placeholder: assume transaction is valid
        return True


class PaymentGateway:
    def __init__(self):
        pass

    def authorizePayment(self):
        """
        Simulates payment authorization.
        In a real system this would communicate with a gateway.
        """
        # Placeholder: assume payment is authorized
        return True


class Order:
    def __init__(self):
        self._orderId = 0   # private attribute
        self._status = ""   # private attribute

    def confirmOrder(self):
        """Confirms the order."""
        self._status = "Confirmed"


class Notification:
    def __init__(self):
        self._message = ""  # private attribute

    def sendConfirmation(self):
        """Sends a confirmation notification."""
        self._message = "Order confirmed"
        print(self._message)

    def sendPaymentFailure(self):
        """Sends a payment failure notification."""
        self._message = "Payment failed"
        print(self._message)