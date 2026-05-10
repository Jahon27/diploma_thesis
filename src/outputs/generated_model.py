class Person:
    def __init__(self):
        self.name = None
        self.phoneNumber = None
        self.emailAddress = None

    def purchaseParkingPass(self):
        pass

class Student(Person):
    def __init__(self):
        self.studentNumber = None
        self.averageMark = None

    def isEligibleToEnroll(self):
        pass

    def getSeminarsTaken(self):
        pass

class Professor(Person):
    def __init__(self):
        self.salary = None
        self.staffNumber = None
        self.yearsOfService = None
        self.numberOfClasses = None

class Address:
    def __init__(self):
        self.street = None
        self.city = None
        self.state = None
        self.postalCode = None
        self.country = None

    def validate(self):
        pass

    def outputAsLabel(self):
        pass


def run_sequence():
    student = Student()
    address = Address()
    professor = Professor()

    addressValid = False
    repeatEnrollmentCheck = False

    address.validate()
    if addressValid:
        address.outputAsLabel()
    else:
        student.getSeminarsTaken()
    while repeatEnrollmentCheck:
        student.isEligibleToEnroll()
    student.getSeminarsTaken()
    student.purchaseParkingPass()

if __name__ == '__main__':
    run_sequence()
