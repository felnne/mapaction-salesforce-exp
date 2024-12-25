import sys

sys.path.append("src")

import streamlit as st

from sf_exp.clients import StreamlitOauthClient, SalesforceClient
from sf_exp.models import Config


def load_config() -> Config:
    return Config(
        oauth_client_id=st.secrets.oauth.client_id,
        oauth_client_secret=st.secrets.oauth.client_secret,
        oauth_authorise_endpoint=st.secrets.oauth.authorise_endpoint,
        oauth_token_endpoint=st.secrets.oauth.token_endpoint,
        oauth_redirect_uri=st.secrets.oauth.redirect_uri,
        oauth_scope=st.secrets.oauth.scopes,
        sf_domain=st.secrets.salesforce.domain,
        sf_client_id=st.secrets.salesforce.client_id,
        sf_client_secret=st.secrets.salesforce.client_secret,
    )


def main():
    config = load_config()
    sf = SalesforceClient(config)
    st_oauth = StreamlitOauthClient(config)

    st.title("MapAction Salesforce Automation Experiments")
    st.write(
        """
        Experiment to explore the effort needed to access and update information stored in Salesforce from an external
        app. Volunteers viewing and updating parts of their personal information is used as an example use-case.
        """
    )
    st.warning("This experiment uses an development Salesforce instance with a limited number of users. It cannot access real MapAction data.")
    st.info("In this experiment only a few profile fields are shown, and only your mobile number can be updated.")

    if "auth_id_token" not in st.session_state:
        st.write("To begin, sign in with your MapAction Google account to load your details.")

        result = st_oauth.authorize_button()
        if result and "token" in result:
            st_oauth.process_token(result)
            st.session_state.auth_id_token = st_oauth.token
            st.session_state.auth_claim_email = st_oauth.id_claims.email
            st.session_state.auth_claim_given_name = st_oauth.id_claims.given_name
            st.session_state.auth_claim_family_name = st_oauth.id_claims.family_name
            st.rerun()
    else:
        st.balloons()
        name = f"{st.session_state.auth_claim_given_name} {st.session_state.auth_claim_family_name}"
        st.info(f"Signed in as: {name} ({st.session_state.auth_claim_email})")

        contact = sf.contacts.find_by_email(st.session_state.auth_claim_email)
        if contact is None:
            st.error("Contact not found for signed in user.")
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
