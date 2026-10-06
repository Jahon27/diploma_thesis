class User:
    def __init__(self, user_id: int, username: str, password: str):
        self._userId = user_id
        self._username = username
        self._password = password

    def enterCredentials(self):
        # This method triggers the sequence logic
        auth_service = AuthenticationService()
        
        # Sequence Diagram Logic:
        # User calls validateCredentials() on AuthenticationService
        is_valid = auth_service.validateCredentials()
        
        if is_valid:
            # [credentialsValid] branch
            # AuthenticationService calls createSession() on Session
            session = Session()
            session.createSession()
            # Session returns sessionCreated to AuthenticationService (implied)
            # User calls showDashboard()
            self.showDashboard()
        else:
            # [credentialsInvalid] branch
            # User calls showLoginError()
            self.showLoginError()

    def showDashboard(self):
        pass

    def showLoginError(self):
        pass


class UserRepository:
    def findUser(self):
        pass


class Session:
    def __init__(self, session_id: int):
        self._sessionId = session_id

    def createSession(self):
        pass


class AuthenticationService:
    def validateCredentials(self):
        # Sequence Diagram Logic:
        # AuthenticationService calls findUser() on UserRepository
        user_repo = UserRepository()
        user_found = user_repo.findUser()
        
        # Sequence Diagram shows userFound return message from UserRepository to AuthenticationService
        if user_found:
            return True
        else:
            return False