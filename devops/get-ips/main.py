import docker
from prettytable import PrettyTable, TableStyle


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


if __name__ == "__main__":
    # List of container names
    containers = [
        (
            "telecom-reverse-proxy",
            "Telecom Frontend",
            "http://telecom-%s.nip.io",
        ),
        (
            "telecom-reverse-proxy",
            "Telecom API",
            "http://telecom-%s.nip.io/api/v1/docs",
        ),
    ]

    client = docker.from_env()

    table = PrettyTable()
    table.set_style(TableStyle.SINGLE_BORDER)
    table.align = "l"
    table.field_names = ["", "URL"]

    for container_name, description, template in containers:
        ip_address = get_container_ip(client, container_name)
        table.add_row([description, template % ip_address])

    print(table)
