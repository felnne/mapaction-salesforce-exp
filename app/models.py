from dataclasses import dataclass


@dataclass()
class Config:
    sf_domain: str
    sf_client_id: str
    sf_client_secret: str


@dataclass()
class Contact:
    sf_id: str
    name: str
    email: str
    mobile: str | None = None

    def __repr__(self):
        return f"Contact(sf_id={self.sf_id}, email={self.email})"


@dataclass()
class AuthInfo:
    name: str
    email: str
