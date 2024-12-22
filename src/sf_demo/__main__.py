from dataclasses import dataclass

import streamlit as st
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
    mobile: str | None = None

    def __repr__(self):
        return f"Contact(sf_id={self.sf_id}, email={self.email})"


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

    identity = st.text_input("Identity:", "ffennell@mapaction.org")
    st.write(f"Identity: {identity}")

    contact = sf.contacts.find_by_email(identity)
    if contact is None:
        st.write("Contact not found.")
    else:
        with st.form("contact"):
            st.write("Update your contact details")
            st.text_input("Name:", contact.name, disabled=True)
            st.text_input("Email:", contact.email, disabled=True)
            mobile = st.text_input("Mobile:", contact.mobile)
            contact_submit = st.form_submit_button("Update details")

        if contact_submit and mobile is not None and mobile != contact.mobile:
            sf.contacts.update(contact, mobile)
            st.success("Details updated successfully.")


if __name__ == "__main__":
    main()
