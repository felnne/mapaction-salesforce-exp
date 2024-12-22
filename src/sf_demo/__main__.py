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

    def __repr__(self):
        return f"Contact(sf_id={self.sf_id}, email={self.email})"


class SalesforceContacts:
    def __init__(self, client: Salesforce):
        self._client = client

    def list(self) -> list[Contact]:
        contacts = []

        results = self._client.query_all("SELECT Id, Name, Email FROM Contact")
        for record in results["records"]:
            contacts.append(
                Contact(
                    sf_id=record["Id"],
                    name=record["Name"],
                    email=record["Email"],
                )
            )

        return contacts

    def add(self, given_name: str, family_name: str, email: str) -> None:
        self._client.Contact.create(
            {
                "FirstName": given_name,
                "LastName": family_name,
                "Email": email,
            }
        )


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

    if st.button("List contacts", type="primary"):
        st.write("Salesforce Contacts")
        st.table(sf.contacts.list())

    with st.form("add_contact"):
        st.write("Add new contact")
        given_name = st.text_input("First name:", "Constance")
        family_name = st.text_input("First name:", "Watson")
        email = st.text_input("Email:", "connie.watson@fastmail.fm")
        add_contact_submit = st.form_submit_button("Submit")

    if add_contact_submit:
        sf.contacts.add(given_name, family_name, email)
        st.success("Contact added successfully")


if __name__ == "__main__":
    main()
