class Manager:
    def __init__(self):
        self.name = None
        self.id = None
        self.phoneNo = None
        self.location = None

    def purchaseInvestory(self):
        pass

    def recordComplaints(self):
        pass

    def ManageStaff(self):
        pass

class Guest:
    def __init__(self):
        self.name = None
        self.id = None
        self.phoneNo = None
        self.roomNum = None

    def checkIn(self):
        pass

    def checkOut(self):
        pass

    def payBill(self):
        pass

    def orderFood(self):
        pass

    def submitFeedBack(self):
        pass

class Chef:
    def __init__(self):
        self.name = None
        self.averageMark = None
        self.location = None

    def takeOrders(self):
        pass

class Receptionist:
    def __init__(self):
        self.name = None
        self.id = None
        self.phoneNo = None
        self.location = None

    def checkRoomAvailability(self):
        pass

    def bookRoom(self):
        pass

    def generateBill(self):
        pass

    def acceptCustomerFeedBack(self):
        pass

class Inventory:
    def __init__(self):
        self.type = None
        self.status = None

class Rooms:
    def __init__(self):
        self.roomNo = None
        self.location = None

class FoodItems:
    def __init__(self):
        self.id = None
        self.name = None

class Bill:
    def __init__(self):
        self.billNo = None
        self.guestName = None

class Housekeeping:
    def __init__(self):
        self.name = None
        self.guestName = None

    def cleanRoom(self):
        pass


if __name__ == '__main__':
    run_sequence()
