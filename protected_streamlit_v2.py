import os
import requests
import requests
import streamlit as st
from jose import jwt, JWTError
from urllib.parse import urlencode, urlparse, parse_qs

# Configuration Keycloak
KEYCLOAK_URL = os.getenv("KEYCLOAK_TEST_URL")
CLIENT_ID = os.getenv("KEYCLOAK_TEST_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_TEST_CLIENT_SECRET")

# Configuration Keycloak
KEYCLOAK_SERVER = "https://iam.karned.bzh/"
REALM = "Karned"
REDIRECT_URI = "http://localhost:8501"


def get_keycloak_authorization_url():
    """Génère l'URL d'autorisation Keycloak"""
    params = {
        'response_type': 'code',
        'client_id': CLIENT_ID,
        'redirect_uri': REDIRECT_URI,
        'scope': 'openid profile email'
    }
    return f"{KEYCLOAK_SERVER}realms/{REALM}/protocol/openid-connect/auth?{urlencode(params)}"


def exchange_code_for_token(code):
    """Échange le code d'autorisation contre un token"""
    token_url = f"{KEYCLOAK_SERVER}realms/{REALM}/protocol/openid-connect/token"

    payload = {
        'grant_type': 'authorization_code',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'code': code,
        'redirect_uri': REDIRECT_URI
    }

    response = requests.post(token_url, data = payload)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de l'échange de token : {response.text}")
        return None


def get_user_info(access_token):
    """Récupère les informations de l'utilisateur"""
    userinfo_url = f"{KEYCLOAK_SERVER}realms/{REALM}/protocol/openid-connect/userinfo"
    headers = {'Authorization': f'Bearer {access_token}'}

    response = requests.get(userinfo_url, headers = headers)

    if response.status_code == 200:
        return response.json()
    else:
        st.error(f"Erreur lors de la récupération des informations utilisateur : {response.text}")
        return None


def main():
    st.title("Authentification Keycloak")

    # Vérifier si l'utilisateur est déjà connecté
    if 'user_info' in st.session_state:
        st.write(f"Bonjour, {st.session_state['user_info'].get('name', 'Utilisateur')}")
        if st.button("Déconnexion"):
            del st.session_state['user_info']
            st.experimental_rerun()
    else:
        # Récupérer les paramètres de l'URL
        query_params = st.experimental_get_query_params()

        if 'code' in query_params:
            # Échanger le code contre un token
            code = query_params['code'][0]
            tokens = exchange_code_for_token(code)

            if tokens:
                # Récupérer les informations utilisateur
                user_info = get_user_info(tokens['access_token'])

                if user_info:
                    st.session_state['user_info'] = user_info
                    st.experimental_rerun()
        else:
            # Afficher le bouton de connexion
            auth_url = get_keycloak_authorization_url()
            st.markdown(f'<a href="{auth_url}" target="_self">Se connecter</a>', unsafe_allow_html = True)


if __name__ == "__main__":
    main()
