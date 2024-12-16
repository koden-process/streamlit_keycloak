import os

import requests
import streamlit as st
from verif_token import get_decoded_token

KEYCLOAK_URL = os.getenv("KEYCLOAK_TEST_URL")
CLIENT_ID = os.getenv("KEYCLOAK_TEST_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_TEST_CLIENT_SECRET")

def login():
    st.title("Connexion via Keycloak")
    st.write(KEYCLOAK_URL)
    st.write(CLIENT_ID)
    st.write(CLIENT_SECRET)

    params = st.query_params.to_dict()

    if "code" in params:
        code = params["code"]
        token_url = f"{KEYCLOAK_URL}/protocol/openid-connect/token"
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": "http://localhost:8501",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        response = requests.post(token_url, data = data)
        if response.status_code == 200:
            data = response.json()
            return data['access_token']
        else:
            st.error("Échec de l'obtention du token.")
            st.write(response.json())
    else:
        auth_url = f"{KEYCLOAK_URL}/protocol/openid-connect/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri=http://localhost:8501"

        st.write(f"{auth_url}", unsafe_allow_html = True)
        return None


def main():
    token = login()
    print(token)
    if token:
        claims = get_decoded_token(None, token)
        if claims:
            st.success(f"Bienvenue, {claims['preferred_username']}!")
            st.write("Votre profil : ", claims)
        else:
            st.error("Token invalide.")


if __name__ == "__main__":
    main()
