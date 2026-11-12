class PickupKiosk:
    def __init__(self):
        self.kioskId = None
        self.location = None
        self.lastStatus = None

    def submitCode(self):
        pass

class PickupService:
    def __init__(self):
        self.serviceId = None
        self.pickupCode = None
        self.attemptCount = None

    def collectParcel(self):
        pass

class PickupLog:
    def __init__(self):
        self.logId = None
        self.lastOutcome = None
        self.eventCount = None

    def recordSuccess(self):
        pass

    def recordDenial(self):
        pass

class ParcelLocker:
    def __init__(self):
        self.lockerId = None
        self.parcelId = None
        self.doorOpen = None

    def unlock(self):
        pass


def run_sequence(codeValid):
    kiosk = PickupKiosk()
    service = PickupService()
    locker = ParcelLocker()
    log = PickupLog()

    service.collectParcel()
    if codeValid:
        locker.unlock()
        log.recordSuccess()
    else:
        log.recordDenial()
