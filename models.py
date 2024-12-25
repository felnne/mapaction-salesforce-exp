from dataclasses import dataclass


@dataclass()
class Config:
    oauth_client_id: str
    oauth_client_secret: str
    oauth_authorise_endpoint: str
    oauth_token_endpoint: str
    oauth_redirect_uri: str
    oauth_scope: str
    sf_domain: str
    sf_client_id: str
    sf_client_secret: str


@dataclass()
class AuthClaims:
    email: str
    given_name: str
    family_name: str


@dataclass()
class Contact:
    sf_id: str
    name: str
    email: str
    mobile: str | None = None

    def __repr__(self):
        return f"Contact(sf_id={self.sf_id}, email={self.email})"
