from fastapi_keycloak import FastAPIKeycloak, OIDCUser, UsernamePassword, HTTPMethod, KeycloakUser, KeycloakGroup
import time
import traceback
from app.log_config import init_loggers
from .config import settings
from fastapi import Request

log = init_loggers(logger_name="keycloak_config-logger")


def get_keycloak(request: Request = None):
    if request is not None:
        request_id = request.headers.get("X-Request-ID")
    else:
        request_id = ""

    # time.sleep(20)
    log.info(f"Trying to connect to Keycloak...", extra={"request_id": request_id})
    try:
        idp = FastAPIKeycloak(
            server_url=f"http://{settings.keycloak_hostname}:{settings.keycloak_port}/auth",
            client_id=settings.client_id,
            client_secret=settings.client_secret,
            admin_client_secret=settings.admin_client_secret,
            realm=settings.realm,
            callback_uri=f"http://{settings.auth_server_url}:{settings.keycloak_port_callback}/callback"
        )
        idp.login_uri = f"http://{settings.auth_server_url}:8002/docs"
        # idp.add_swagger_config(app)
        log.info(f"The connection to Keycloak was successful", extra={"request_id": request_id})
        return idp
    except Exception as ex:
        log.error(f"An error occurred while connecting to Keycloak: {ex}", extra={"request_id": request_id})
        log.error(f"{traceback.format_exc()}", extra={"request_id": request_id})
        raise Exception("Failed to connect to Keycloak.}")
        # return False


# def check_keycloak():
#     time.sleep(20)
#     log.info(f"Trying to connect to Keycloak...")
#     try:
#         idp = FastAPIKeycloak(
#             server_url=f"http://{settings.keycloak_hostname}:{settings.keycloak_port}/auth",
#             client_id=settings.client_id,
#             client_secret=settings.client_secret,
#             admin_client_secret=settings.admin_client_secret,
#             realm=settings.realm,
#             callback_uri=f"http://{settings.auth_server_url}:{settings.keycloak_port_callback}/callback"
#         )
#         idp.login_uri = f"http://{settings.auth_server_url}:8002/docs"
#         # idp.add_swagger_config(app)
#         log.info(f"The connection to Keycloak was successful")
#         return idp
#     except Exception as ex:
#         log.error(f"An error occurred while connecting to Keycloak: {ex}")
#         log.debug(f"{traceback.format_exc()}")
#         raise Exception("Failed to connect to Keycloak after 1 attempts. Shuts down the service")
#         # return False


# def get_keycloak_test():
#     # time.sleep(20)
#     log.info(f"Trying to connect to Keycloak...")
#     try:
#         idp = FastAPIKeycloak(
#             server_url=f"http://{settings.keycloak_hostname}:{settings.keycloak_port}/auth",
#             client_id=settings.client_id,
#             client_secret=settings.client_secret,
#             admin_client_secret=settings.admin_client_secret,
#             realm=settings.realm,
#             callback_uri=f"http://{settings.auth_server_url}:{settings.keycloak_port_callback}/callback"
#         )
#         idp.login_uri = f"http://{settings.auth_server_url}:8002/docs"
#         # idp.add_swagger_config(app)
#         log.info(f"The connection to Keycloak was successful")
#         return idp
#     except Exception as ex:
#         log.error(f"An error occurred while connecting to Keycloak: {ex}")
#         log.debug(f"{traceback.format_exc()}")
#         raise Exception("Failed to connect to Keycloak after 1 attempts. Shuts down the service")
#         # return False