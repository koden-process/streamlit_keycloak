# streamlit_keycloak

Afin de pouvoir être utilisé, le projet nécessite d'avoir un serveur Keycloak en fonctionnement.
Il faut également créer les variables d'environnement suivantes :
KEYCLOAK_TEST_URL
KEYCLOAK_TEST_CLIENT_ID
KEYCLOAK_TEST_CLIENT_SECRET

```sh
export KEYCLOAK_TEST_URL=http://<keycloak-host>/realms/<realm-name>
export KEYCLOAK_TEST_CLIENT_ID=streamlit
export KEYCLOAK_TEST_CLIENT_SECRET=streamlit
```