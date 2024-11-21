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
    components = [
        (
            "telecom-reverse-proxy",
            "Telecom Web App",
            "http://telecom.%s.nip.io/",
            None,
        ),
        (
            "telecom-reverse-proxy",
            "Telecom API",
            "http://api.telecom.%s.nip.io/api/v1/",
            None,
        ),
        (
            "psp-core-reverse-proxy",
            "PSP Frontend",
            "http://psp.%s.nip.io/",
            None,
        ),
        (
            "psp-core-reverse-proxy",
            "PSP Public-Facing API",
            "http://api.psp.%s.nip.io/api/v1/",
            None,
        ),
        (
            "psp-core-reverse-proxy",
            "PSP Internal API",
            "http://internal-api.psp.%s.nip.io/api/v1/",
            "http://psp-core-backend:9000/",
        ),
        (
            "psp-crypto-handler-reverse-proxy",
            "PSP Crypto Payment Page",
            "http://crypto.psp.%s.nip.io/",
            None,
        ),
        (
            "psp-crypto-handler-reverse-proxy",
            "PSP Crypto Public-Facing API",
            "http://crypto.psp.%s.nip.io/api/v1/",
            None,
        ),
        (
            "psp-crypto-handler-reverse-proxy",
            "PSP Crypto Internal API",
            "http://internal-crypto.psp.%s.nip.io/api/v1/",
            "http://psp-crypto-handler-backend:9000/",
        ),
        (
            "psp-card-handler-backend",
            "PSP Card Internal API",
            "http://internal-card.psp.%s.nip.io/api/v1/",
            "http://psp-card-handler-backend:9000/",
        ),
    ]

    client = docker.from_env()

    table = PrettyTable()
    table.set_style(TableStyle.SINGLE_BORDER)
    table.align = "l"
    table.field_names = [
        "Component",
        "Public URL (Avoid using if internal is provided)",
        "Internal URL",
    ]

    for container_name, name, public_url_template, internal_url in components:
        ip_address = get_container_ip(client, container_name)
        table.add_row(
            [
                name,
                public_url_template % ip_address,
                internal_url or "",
            ]
        )

    print(table)
