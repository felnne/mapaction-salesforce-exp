from dataclasses import dataclass

import jwt
import streamlit as st
from environs import Env
from simple_salesforce import Salesforce
from streamlit_oauth import OAuth2Component


@dataclass()
class Config:
    oauth_client_id: str
    oauth_client_secret: str
    oauth_authorise_url: str
    oauth_token_url: str
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


class StreamlitOauthClient:
    def __init__(self, config: Config, token: str | None = None):
        self._token: str = ""
        if token:
            self._token = token

        self._id_claims = None

        self._redirect_uri = config.oauth_redirect_uri
        self._scope = config.oauth_scope

        self._client = OAuth2Component(
            client_id=config.oauth_client_id,
            client_secret=config.oauth_client_secret,
            authorize_endpoint=config.oauth_authorise_url,
            token_endpoint=config.oauth_token_url,
        )

    def authorize_button(self) -> dict:
        google_icon = (
            "data:image/svg+xml;charset=utf-8,%3Csvg xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' viewBox='0 0 48 48'%3E%3Cdefs%3E%3Cpath id='a' d='M44.5 20H24v8.5h11.8C34.7 33.9 30.1 37 24 37c-7.2 0-13-5.8-13-13s5.8-13 13-13c3.1 0 5.9 1.1 8.1 2.9l6.4-6.4C34.6 4.1 29.6 2 24 2 11.8 2 2 11.8 2 24s9.8 22 22 22c11 0 21-8 21-22 0-1.3-.2-2.7-.5-4z'/%3E%3C/defs%3E%3CclipPath id='b'%3E%3Cuse xlink:href='%23a' overflow='visible'/%3E%3C/clipPath%3E%3Cpath clip-path='url(%23b)' fill='%23FBBC05' d='M0 37V11l17 13z'/%3E%3Cpath clip-path='url(%23b)' fill='%23EA4335' d='M0 11l17 13 7-6.1L48 14V0H0z'/%3E%3Cpath clip-path='url(%23b)' fill='%2334A853' d='M0 37l30-23 7.9 1L48 0v48H0z'/%3E%3Cpath clip-path='url(%23b)' fill='%234285F4' d='M48 48L17 24l-4-3 35-10z'/%3E%3C/svg%3E",
        )

        return self._client.authorize_button(
            name="Continue with Google",
            redirect_uri=self._redirect_uri,
            scope=self._scope,
            icon=google_icon,
            pkce="S256",
        )

    def process_token(self, result: dict) -> str:
        try:
            self._token = result["token"]["id_token"]
            claims = jwt.decode(self._token, options={"verify_signature": False})
            self._id_claims = AuthClaims(claims["email"], claims["given_name"], claims["family_name"])
        except KeyError:
            msg = "Failed to retrieve token."
            raise RuntimeError(msg)

        return self._token

    @property
    def token(self) -> str:
        return self._token

    @property
    def id_claims(self) -> AuthClaims:
        return self._id_claims


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
            oauth_client_id=env.str("OAUTH_CLIENT_ID"),
            oauth_client_secret=env.str("OAUTH_CLIENT_SECRET"),
            oauth_authorise_url=env.str("OAUTH_AUTHORISE_URL"),
            oauth_token_url=env.str("OAUTH_TOKEN_URL"),
            oauth_redirect_uri=env.str("OAUTH_REDIRECT_URI"),
            oauth_scope=env.str("OAUTH_SCOPE"),
            sf_domain=env.str("SF_DOMAIN"),
            sf_client_id=env.str("SF_CLIENT_ID"),
            sf_client_secret=env.str("SF_CLIENT_SECRET"),
        )


def main():
    config = load_config()
    sf = SalesforceClient(config)
    st_oauth = StreamlitOauthClient(config)

    st.write(
        """
        # MapAction Salesforce external access experiment

        Experiment to explore the effort needed to access and update information stored in Salesforce from an external
        app. Uses volunteers viewing and updating parts of their personal information as an example use-case.

        **Note:** This experiment uses an isolated Salesforce instance and cannot access real MapAction data.

        To begin, sign in with your MapAction Google account to load a subset of your details. Only your mobile number
        can be updated.
        """
    )

    if "auth_id_token" not in st.session_state:
        result = st_oauth.authorize_button()
        if result and "token" in result:
            st_oauth.process_token(result)
            st.session_state.auth_id_token = st_oauth.token
            st.session_state.auth_claim_email = st_oauth.id_claims.email
            st.session_state.auth_claim_given_name = st_oauth.id_claims.given_name
            st.session_state.auth_claim_family_name = st_oauth.id_claims.family_name
            st.rerun()
    else:
        name = f"{st.session_state.auth_claim_given_name} {st.session_state.auth_claim_family_name}"
        st.write(f"Hello {name} ({st.session_state.auth_claim_email})")

        contact = sf.contacts.find_by_email(st.session_state.auth_claim_email)
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
