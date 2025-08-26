import os
import docker
import shutil


def get_container_ip(client, container_name):
    try:
        container = client.containers.get(container_name)
        networks = container.attrs["NetworkSettings"]["Networks"]
        return (
            ", ".join(
                network["IPAddress"]
                for network in networks.values()
                if network["IPAddress"]
            )
            or "No IP Assigned"
        )
    except docker.errors.NotFound:
        return "Container Not Found"
    except Exception as e:
        return f"Error: {str(e)}"


def update_env_file(ip_address, template, variable, env_file):
    new_value = template % ip_address

    try:
        # If env_file file doesn't exist, copy .env.example into env_file
        if not os.path.exists(env_file):
            shutil.copy(
                env_file.replace(".env", ".env.example"),
                env_file,
            )

        with open(env_file, "r") as file:
            lines = file.readlines()

        updated = False
        with open(env_file, "w") as file:
            for line in lines:
                if line.startswith(variable + "="):
                    file.write(f"{variable}={new_value}\n")
                    updated = True
                else:
                    file.write(line)

            if not updated:
                file.write(f"{variable}={new_value}\n")

        print(f"Updated {variable} in {env_file} to: {new_value}")
    except FileNotFoundError:
        print(f"Error: {env_file} not found.")
    except Exception as e:
        print(f"Error updating {env_file}: {str(e)}")


if __name__ == "__main__":
    client = docker.from_env()

    files = [
        (
            "psp-crypto-handler-reverse-proxy",
            "crypto.psp.%s.nip.io",
            "../../psp/crypto-handler/backend/.env",
            "FRONTEND_HOST",
        ),
        (
            "consul",
            "http://consul.%s.nip.io:8500",
            "../../psp/crypto-handler/backend/.env",
            "CONSUL_HOST",
        ),
        (
            "psp-qr-handler-reverse-proxy",
            "qr.psp.%s.nip.io",
            "../../psp/qr-handler/backend/.env",
            "FRONTEND_HOST",
        ),
        (
            "psp-core-reverse-proxy",
            "psp.%s.nip.io",
            "../../psp/core/backend/.env",
            "FRONTEND_HOST",
        ),
        (
            "consul",
            "http://consul.%s.nip.io:8500",
            "../../psp/core/backend/.env",
            "CONSUL_HOST",
        ),
        (
            "psp-core-reverse-proxy",
            "http://psp.%s.nip.io/api/v1",
            "../../psp/paypal-handler/backend/.env",
            "PSP_API_BASE_URL",
        ),
        (
            "psp-core-reverse-proxy",
            "http://psp.%s.nip.io/api/v1",
            "../../telecom/backend/.env",
            "PSP_API_BASE_URL",
        ),
        (
            "telecom-reverse-proxy",
            "http://telecom.%s.nip.io",
            "../../telecom/backend/.env",
            "FRONTEND_ORIGIN",
        ),
        (
            "telecom-reverse-proxy",
            "http://api.telecom.%s.nip.io/api/v1/",
            "../../telecom/frontend/.env",
            "VITE_SERVER_URL",
        ),
        (
            "unicredit-bank-reverse-proxy",
            "http://unicredit.%s.nip.io/api/v1/",
            "../../psp/card-handler/backend/.env",
            "POPULATE_UNICREDIT_BANK_API_URL",
        ),
        (
            "erste-bank-reverse-proxy",
            "http://erste.%s.nip.io/api/v1/",
            "../../psp/card-handler/backend/.env",
            "POPULATE_ERSTE_BANK_API_URL",
        ),
        (
            "consul",
            "http://consul.%s.nip.io:8500",
            "../../psp/card-handler/backend/.env",
            "CONSUL_HOST",
        ),
        (
            "unicredit-bank-reverse-proxy",
            "unicredit.%s.nip.io",
            "../../bank/unicredit/backend/.env",
            "FRONTEND_HOST",
        ),
        (
            "erste-bank-reverse-proxy",
            "erste.%s.nip.io",
            "../../bank/erste/backend/.env",
            "FRONTEND_HOST",
        ),
        (
            "unicredit-bank-reverse-proxy",
            "http://api.unicredit.%s.nip.io/api/v1/",
            "../../bank/unicredit/frontend/.env",
            "VITE_SERVER_URL",
        ),
        (
            "erste-bank-reverse-proxy",
            "http://api.erste.%s.nip.io/api/v1/",
            "../../bank/erste/frontend/.env",
            "VITE_SERVER_URL",
        ),
        (
            "psp-core-reverse-proxy",
            "http://api.psp.%s.nip.io/api/v1/",
            "../../psp/core/frontend/.env",
            "VITE_SERVER_URL",
        ),
        (
            "psp-crypto-handler-reverse-proxy",
            "http://crypto.psp.%s.nip.io/api/v1/",
            "../../psp/crypto-handler/frontend/.env",
            "VITE_SERVER_URL",
        ),
    ]

    for container_name, template, env_file, variable in files:
        ip_address = get_container_ip(client, container_name)
        update_env_file(ip_address, template, variable, env_file)
