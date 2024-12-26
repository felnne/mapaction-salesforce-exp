from simple_salesforce import Salesforce

from app.models import Config, Contact


# noinspection SqlResolve
class SalesforceContacts:
    def __init__(self, client: Salesforce):
        self._client = client

    def list(self) -> list[Contact]:
        contacts = []

        results = self._client.query_all("SELECT Id, Name, Email, MobilePhone FROM Contact")
        for record in results["records"]:
            contacts.append(
                Contact(
                    sf_id=record["Id"],
                    name=record["Name"],
                    email=record["Email"],
                    mobile=record.get("MobilePhone"),
                )
            )

        return contacts

    def find_by_email(self, email: str) -> Contact | None:
        result = self._client.query(f"SELECT Id, Name, Email, MobilePhone FROM Contact WHERE Email = '{email}'")

        if result["totalSize"] == 0:
            return None

        if result["totalSize"] > 1:
            msg = f"Multiple contacts found with email '{email}'."
            raise ValueError(msg)

        record = result["records"][0]
        return Contact(
            sf_id=record["Id"],
            name=record["Name"],
            email=record["Email"],
            mobile=record.get("MobilePhone"),
        )

    def add(self, given_name: str, family_name: str, email: str, mobile: str | None = None) -> None:
        payload = {
            "FirstName": given_name,
            "LastName": family_name,
            "Email": email,
        }
        if mobile:
            payload["MobilePhone"] = mobile

        self._client.Contact.create(payload)

    def update(self, contact: Contact, mobile: str | None = None) -> None:
        payload = {}
        if mobile:
            payload["MobilePhone"] = mobile

        self._client.Contact.update(contact.sf_id, payload)


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
