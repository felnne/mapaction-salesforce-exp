from dataclasses import dataclass
from environs import Env
from simple_salesforce import Salesforce


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

    def __repr__(self):
        return f"Contact(sf_id={self.sf_id}, email={self.email})"


class SalesforceContacts:
    def __init__(self, client: Salesforce):
        self._client = client

    def list(self) -> list[Contact]:
        contacts = []

        results = self._client.query_all("SELECT Id, Name, Email FROM Contact")
        for record in results["records"]:
            contacts.append(Contact(
                sf_id=record["Id"],
                name=record["Name"],
                email=record["Email"],
            ))

        return contacts


class SalesforceClient:
    def __init__(self, config: Config):
        self._client = Salesforce(
            domain=config.sf_domain.replace("https://", "").replace(".salesforce.com", ""),
            consumer_key=config.sf_client_id,
            consumer_secret=config.sf_client_secret,
        )

    @property
    def contacts(self) -> SalesforceContacts:
        return SalesforceContacts(self._client)


def load_config() -> Config:
    env = Env()
    env.read_env()

    with env.prefixed("APP_"):
        return Config(
            sf_domain=env.str("SF_DOMAIN"),
            sf_client_id=env.str("SF_CLIENT_ID"),
            sf_client_secret=env.str("SF_CLIENT_SECRET"),
        )


def main():
    config = load_config()
    sf = SalesforceClient(config)
    print(sf.contacts.list())

if __name__ == '__main__':
    main()
