from drf_spectacular.extensions import OpenApiAuthenticationExtension


class CustomBearerSchema(OpenApiAuthenticationExtension):
    target_class = "authentication.authentication.RemoteJWTAuthentication"
    name = "BearerAuth"

    def get_security_definition(self, auto_schema):
        return {"type": "http", "scheme": "bearer", "bearerFormat": "JWT"}
