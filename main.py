import streamlit as st

from app.clients import SalesforceClient
from app.models import Config, AuthInfo


def load_config() -> Config:
    return Config(
        sf_domain=st.secrets.salesforce.domain,
        sf_client_id=st.secrets.salesforce.client_id,
        sf_client_secret=st.secrets.salesforce.client_secret,
    )


def intro_section() -> None:
def supports_oauth() -> bool:
    if st.secrets.env.platform == "streamlit":
        return False
    return True


    st.markdown(
        """
        # MapAction Salesforce Automation Experiments
        Experiment to explore the effort needed to access and update information stored in Salesforce from an external
        app. Volunteers viewing and updating parts of their personal information is used as an example use-case.

        In this experiment:
        - accounts for a limited subset of volunteers (plus some fake volunteers for some staff to test with) are registered
        - a limited subset fields from the Salesforce contact object are shown for each (fake) volunteer
        - only the mobile number field can be updated (other details are set to read-only)

        **Note:** This experiment uses a standalone Salesforce instance. It cannot access real MapAction data.
        """
    )


def show_auth_sign_in() -> AuthInfo | None:
    if not st.experimental_user.is_authenticated and supports_oauth():
        st.info("To begin, sign in with your MapAction Google account to load your (fake) details.")
        google_button = st.button("Continue with Google")
        if google_button:
            st.experimental_user.login(provider="google")
    elif st.experimental_user.is_authenticated and supports_oauth():
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
            st.experimental_user.logout()


def show_contact_form(salesforce_client: SalesforceClient, auth_info: AuthInfo) -> None:
    contact = salesforce_client.contacts.find_by_email(auth_info.email)

    if contact is None:
        st.error("Your account is not registered to use this experiment.")
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


def debug_section() -> None:
    st.markdown("---")
    expand = st.expander("Debug info")
    with expand:


def main():
    config = load_config()
    sf = SalesforceClient(config)

    intro_section()

    auth_info = show_auth_sign_in()
    if auth_info:
        st.info(f"Signed in as: {auth_info.name} ({auth_info.email})")
        show_auth_sign_out()

        show_contact_form(salesforce_client=sf, auth_info=auth_info)


    debug_section()
    if error := st.experimental_user.get("error"):
        st.error(f"OAuth error: {error}")


if __name__ == "__main__":
    main()
