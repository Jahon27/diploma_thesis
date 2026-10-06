class Order:
    def __init__(self):
        self._orderId: int = 0
        self._totalAmount: int = 0
        self._items: list = []  # list of OrderItem

    def createOrder(self) -> None:
        # Initialize order (e.g., set IDs, reset total)
        pass

    def confirmOrder(self) -> None:
        # Finalize the order
        pass

    def sendConfirmation(self, notification: 'Notification') -> None:
        notification.sendConfirmation()


class OrderItem:
    def __init__(self):
        self._quantity: int = 0
        self._product: 'Product | None' = None

    def processItem(self) -> None:
        # Process the item (e.g., validate, calculate)
        pass

    def reserveProduct(self, inventory: 'Inventory') -> None:
        # Request inventory to reserve the product for this item
        inventory.reserveProduct(self._product, self._quantity)


class Inventory:
    def __init__(self):
        self._inventoryId: int = 0
        self._product: 'Product | None' = None

    def reserveProduct(self, product: 'Product | None', quantity: int) -> None:
        # Reserve the given quantity of the product
        pass

    def updateStock(self) -> None:
        # Update stock levels in the associated product
        if self._product:
            self._product.updateStock()


class Product:
    def __init__(self):
        self._productId: int = 0
        self._stockQuantity: int = 0

    def updateStock(self) -> None:
        # Adjust the stock quantity
        pass


class Notification:
    def __init__(self):
        self._message: str = ""

    def sendConfirmation(self) -> None:
        # Send the confirmation message (e.g., email, SMS)
        pass