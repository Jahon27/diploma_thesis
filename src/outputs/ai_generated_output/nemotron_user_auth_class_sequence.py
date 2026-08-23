class User:
    def __init__(self, user_id: int, username: str, password: str):
        self.user_id = user_id
        self.username = username
        self.password = password

    def enter_credentials(self):
        # Inconsistency: sequence diagram shows this method being called on AuthenticationService,
        # but class diagram defines enter_credentials() on User.
        # This method could collect credentials; here it returns a dummy tuple.
        return self.username, self.password

    def show_dashboard(self):
        print(f"Welcome {self.username}, here's your dashboard.")


class UserRepository:
    def find_user(self, username: str):
        # Defined in class diagram.
        # Inconsistency: sequence diagram shows AuthenticationService calling validateCredentials()
        # on UserRepository, but class diagram defines find_user().
        # This placeholder returns a user if the username matches.
        if username == "alice":
            return User(1, username, "secret")
        return None


class Session:
    def create_session(self):
        # Defined in class diagram.
        # No inconsistency; this method is called on Session as shown.
        return 12345


class AuthenticationService:
    def __init__(self, repo: UserRepository, session: Session):
        self.repo = repo
        self.session = session

    def validate_credentials(self):
        # Defined in class diagram.
        # Inconsistency: sequence diagram shows this method being called on UserRepository,
        # but class diagram defines validate_credentials() on AuthenticationService.
        # This stub always returns True for demonstration.
        return True

    def show_dashboard(self, user: User):
        # This method is defined on User, but called by AuthenticationService.
        # No inconsistency; method ownership remains on User.
        user.show_dashboard()

    def run(self, user: User):
        # Main flow following the sequence diagram.
        # Step 1: User calls enter_credentials (inconsistency noted above).
        username, password = user.enter_credentials()

        # Step 2: AuthenticationService validates credentials via UserRepository.
        # Inconsistency: sequence expects validateCredentials() on UserRepository,
        # but class diagram defines find_user().
        found_user = self.repo.find_user(username)
        if not found_user:
            print("Login failed")
            return

        # Step 3: Create a session.
        session_id = self.session.create_session()
        print("Login successful")

        # Step 4: Show dashboard to the user.
        self.show_dashboard(found_user)


if __name__ == "__main__":
    # Create participants as defined in the diagrams.
    user = User(user_id=1, username="alice", password="secret")
    repo = UserRepository()
    session = Session()
    auth_service = AuthenticationService(repo, session)

    # Execute the authentication flow.
    auth_service.run(user)