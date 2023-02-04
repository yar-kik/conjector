from conjector import properties


@properties(filename="example.yml", root="services.email_service")
class EmailService:
    key: str  # will store "some value"


@properties(filename="example.yml", root="services.auth_service")
class AuthService:
    key: str  # will store "another value"
