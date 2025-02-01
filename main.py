from pathlib import Path
from tomllib import load as toml_load

import streamlit as st

from app.clients import SalesforceClient
from app.models import Config, AuthInfo


def load_config() -> Config:
    return Config(
        sf_domain=st.secrets.salesforce.domain,
        sf_client_id=st.secrets.salesforce.client_id,
        sf_client_secret=st.secrets.salesforce.client_secret,
    )


def supports_oauth() -> bool:
    if st.secrets.env.platform == "streamlit":
        return False
    return True


def app_version() -> str:
    with Path("pyproject.toml").open(mode="rb") as f:
        # noinspection PyTypeChecker
        data = toml_load(f)
        return data["project"]["version"]


def show_intro() -> None:
    st.title("MapAction Salesforce Automation Experiments")
    st.markdown(
        """
        Experiment to explore the effort needed to access and update information stored in Salesforce.
        It uses the use-case of volunteers viewing and updating parts of their personal information as an example.

        **Note:** This experiment does not use real MapAction data.
        """
    )


def show_auth_sign_in() -> AuthInfo | None:
    if not st.experimental_user.get("is_logged_in") and supports_oauth():
        st.info("To begin, sign in with your MapAction Google account to load your (fake) details.")
        google_button = st.button("Continue with Google")
        if google_button:
            st.login(provider="google")
    elif st.experimental_user.get("is_logged_in") and supports_oauth():
        return AuthInfo(
            name=st.experimental_user.name,
            email=st.experimental_user.email,
        )
    elif not supports_oauth():
        return AuthInfo(
            name="Connie Watson (Example User)",
            email="cwatson@mapaction.org",
        )


def show_auth_sign_out() -> None:
    if supports_oauth():
        logout_button = st.button("Logout")
        if logout_button:
            st.logout()


def show_contact_form(salesforce_client: SalesforceClient, auth_info: AuthInfo) -> None:
    contact = salesforce_client.contacts.find_by_email(auth_info.email)

    if contact is None:
        st.error("This account is not registered to use this experiment.")
    else:
        st.header("Personal Details", divider=True)
        with st.form("contact"):
            st.write("Update your details")
            st.text_input("Name:", contact.name, disabled=True)
            st.text_input("Email:", contact.email, disabled=True)
            mobile = st.text_input("Mobile:", contact.mobile)
            contact_submit = st.form_submit_button("Update details")

        if contact_submit and mobile is not None and mobile != contact.mobile:
            salesforce_client.contacts.update(contact, mobile)
            st.success("Details updated successfully.")


def show_experiment_info() -> None:
    st.markdown("---")
    expand = st.expander("Experiment information")
    with expand:
        st.markdown(
            f"""
            ### App info
            - version: {app_version()}
            - repo: [github.com/felnne/mapaction-salesforce-exp](https://github.com/felnne/mapaction-salesforce-exp)
            """
        )

        st.markdown(
            """
            ### Limitations
            - this experiment uses a standalone Salesforce instance - it cannot access real data
            - limited information (name, email, mobile) are shown for each volunteer's Salesforce contact object
            - only the mobile number field can be updated (other details are set to read-only)
            """
        )


def main():
    config = load_config()
    sf = SalesforceClient(config)

    show_intro()

    auth_info = show_auth_sign_in()
    if auth_info:
        st.info(f"Signed in as: {auth_info.name} ({auth_info.email})")
        show_auth_sign_out()

        show_contact_form(salesforce_client=sf, auth_info=auth_info)

    show_experiment_info()

    if error := st.experimental_user.get("error"):
        st.error(f"OAuth error: {error}")


if __name__ == "__main__":
    main()
