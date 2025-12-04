import os
from pydantic import BaseModel


class Settings(BaseModel):
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg2://ride_user:ride_password@localhost:5433/ride_db")

    IAM_PUBLIC_KEY: str = os.getenv("IAM_PUBLIC_KEY", """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnVuq6l54dUr7dOAq9MSs
+KrUNJ+wtnQInZKcMUf7GpLB0zBUNOaOnalvUXyE5vPQvPEhehXCElv0ZN/cGUuX
371dvJxI0/kyfqxNLyedcEqCir/5sSZO56u/mQRPy0HhmpyYJNyZugMoCfONsfRE
AhdUmoLwp9kQ1MvbuIYqlhzt48Ob/CXLILOV2VStYyabUBZmW604XmxXs7DmKqXO
nJ53gnKAidoWhwpMDT+9vQj6jKVJY/4AMkhXI30tDYqLinSqj4zlPfgMeN6fjnD6
jVg6HbDPnbDWUXHyVlvpTBoEXE2jgzHBEOyTLbZ3LQq8nJ/99B4MZu0bhptsykiG
pwIDAQAB
-----END PUBLIC KEY-----""")

    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "RS256")
    JWT_ISSUER: str | None = os.getenv("JWT_ISSUER", None)
    JWT_AUDIENCE: str | None = os.getenv("JWT_AUDIENCE", None)

    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"


settings = Settings()
