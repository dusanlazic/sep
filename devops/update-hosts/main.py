import docker


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


def update_env_file(ip_address, template, env_file):
    new_host_value = template % ip_address

    try:
        with open(env_file, "r") as file:
            lines = file.readlines()

        updated = False
        with open(env_file, "w") as file:
            for line in lines:
                if line.startswith("FRONTEND_HOST="):
                    file.write(f"FRONTEND_HOST={new_host_value}\n")
                    updated = True
                else:
                    file.write(line)

            if not updated:
                file.write(f"FRONTEND_HOST={new_host_value}\n")

        print(f"Updated FRONTEND_HOST in {env_file} to: {new_host_value}")
    except FileNotFoundError:
        print(f"Error: {env_file} not found.")
    except Exception as e:
        print(f"Error updating {env_file}: {str(e)}")


if __name__ == "__main__":
    client = docker.from_env()

    components = [
        (
            "psp-crypto-handler-reverse-proxy",
            "crypto.psp.%s.nip.io",
            "../../psp/crypto-handler/backend/.env.example",
        ),
    ]

    for container_name, template, env_file in components:
        ip_address = get_container_ip(client, container_name)
        update_env_file(ip_address, template, env_file)
