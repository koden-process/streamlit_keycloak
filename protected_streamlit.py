import os
import requests
import streamlit as st
from jose import jwt, JWTError

# Configuration Keycloak
KEYCLOAK_URL = os.getenv("KEYCLOAK_TEST_URL")
CLIENT_ID = os.getenv("KEYCLOAK_TEST_CLIENT_ID")
CLIENT_SECRET = os.getenv("KEYCLOAK_TEST_CLIENT_SECRET")


# Page de connexion
def login():
    st.title("Connexion via Keycloak")
    st.write(KEYCLOAK_URL)
    st.write(CLIENT_ID)
    st.write(CLIENT_SECRET)

    # Obtenir le Bearer Token depuis l'API Keycloak
    code = st.experimental_get_query_params().get("code")
    if code:
        token_url = f"{KEYCLOAK_URL}/protocol/openid-connect/token"
        data = {
            "grant_type": "authorization_code",
            "code": code[0],
            "redirect_uri": "http://localhost:8501",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }
        response = requests.post(token_url, data = data)
        if response.status_code == 200:
            token = response.json()
            return token["access_token"]
        else:
            st.error("Échec de l'obtention du token.")
    else:
        # Bouton de redirection vers Keycloak
        auth_url = f"{KEYCLOAK_URL}/protocol/openid-connect/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri=http://localhost:8501"
        st.markdown(f"[Se connecter avec Keycloak]({auth_url})", unsafe_allow_html = True)
        return None


# Vérifier le token et afficher le contenu
def verify_token(token):
    jwks_url = f"{KEYCLOAK_URL}/protocol/openid-connect/certs"
    try:
        jwks_response = requests.get(jwks_url).json()
        key = jwks_response["keys"][0]  # Récupère la clé publique pour valider le token
        claims = jwt.decode(token, key, algorithms = ["RS256"], audience = CLIENT_ID)
        return claims
    except JWTError as e:
        st.error(f"Erreur de validation du token: {str(e)}")
        return None


# Application principale
def main():
    token = login()
    if token:
        # claims = verify_token(token)
        st.write(token)
        claims = True
        if claims:
            st.success(f"Bienvenue, {claims['preferred_username']}!")
            st.write("Votre profil : ", claims)
        else:
            st.error("Token invalide.")


if __name__ == "__main__":
    main()
