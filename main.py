import streamlit as st

from app.clients import SalesforceClient
from app.models import Config


def load_config() -> Config:
    return Config(
        sf_domain=st.secrets.salesforce.domain,
        sf_client_id=st.secrets.salesforce.client_id,
        sf_client_secret=st.secrets.salesforce.client_secret,
    )


def intro_section() -> None:
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


def contact_form_section(salesforce_client: SalesforceClient) -> None:
    contact = salesforce_client.contacts.find_by_email(st.experimental_user.email)

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
        st.write("Auth info:")
        st.json(st.experimental_user)


def main():
    config = load_config()
    sf = SalesforceClient(config)

    intro_section()

    if not st.experimental_user.is_authenticated:
        st.write("To begin, sign in with your MapAction Google account to load your details.")
        google_button = st.button("Continue with Google")
        if google_button:
            st.experimental_user.login(provider="google")
    else:
        st.info(f"Signed in as: {st.experimental_user.name} ({st.experimental_user.email})")
        logout_button = st.button("Logout")
        if logout_button:
            st.experimental_user.logout()

        contact_form_section(salesforce_client=sf)

    debug_section()
    if error := st.experimental_user.get("error"):
        st.error(f"Auth error: {error}")


if __name__ == "__main__":
    main()
