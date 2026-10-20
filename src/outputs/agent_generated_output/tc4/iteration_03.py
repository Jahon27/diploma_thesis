def run_sequence():
    order = Order()
    orderitem = OrderItem()
    inventory = Inventory()
    product = Product()
    notification = Notification()
    
    order.createOrder()
    
    eachOrderItem = True
    while eachOrderItem:
        orderitem.processItem()
        inventory.reserveProduct()
        product.updateStock()
        
    order.confirmOrder()
    notification.sendConfirmation()