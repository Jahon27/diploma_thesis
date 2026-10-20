class User:
    def __init__(self):
        self.userId = None
        self.username = None
        self.password = None

    def enterCredentials(self):
        pass

    def showDashboard(self):
        pass

    def showLoginError(self):
        pass

class UserRepository:
    def findUser(self):
        pass

class Session:
    def __init__(self):
        self.sessionId = None

    def createSession(self):
        pass

class AuthenticationService:
    def validateCredentials(self):
        pass


def run_sequence():
    user = User()
    authenticationservice = AuthenticationService()
    userrepository = UserRepository()
    session = Session()

    user.enterCredentials()
    authenticationservice.validateCredentials()
    userrepository.findUser()
    session.createSession()
    user.showDashboard()
