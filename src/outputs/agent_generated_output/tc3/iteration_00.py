class User:
    def __init__(self, userId, username, password):
        self.userId = userId
        self.username = username
        self.password = password

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
    def __init__(self, sessionId):
        self.sessionId = sessionId

    def createSession(self):
        pass

class AuthenticationService:
    def validateCredentials(self):
        pass

# Simulated sequence execution
def execute_sequence():
    user = User(1, "john_doe", "secret")
    authenticationservice = AuthenticationService()
    userrepository = UserRepository()
    session = Session(101)

    user.enterCredentials()
    credentialsValid = authenticationservice.validateCredentials()
    userFound = userrepository.findUser()
    
    if userFound:
        sessionCreated = authenticationservice.createSession()
        user.showDashboard()
    else:
        user.showLoginError()