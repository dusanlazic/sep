import uuid
from collections import OrderedDict

import yaml
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from ..database import Base


class CustomDumper(yaml.Dumper):
    def represent_dict(self, data):
        return super().represent_dict(dict(data))


CustomDumper.add_representer(OrderedDict, CustomDumper.represent_dict)


class Merchant(Base):
    __tablename__ = "merchants"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    username: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    api_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    configuration_json: Mapped[dict] = mapped_column(JSONB, nullable=False)

    # configuration_json is a JSONB field that stores the merchant's payment methods configuration in JSON format.
    # It includes enabled payment methods.

    def get_configuration_yaml(self) -> str:
        """
        Converts the JSON configuration to YAML with fields in a specific order.
        """
        jsonb_data = self.configuration_json

        ordered_data = OrderedDict(
            [
                (
                    "urls",
                    OrderedDict(
                        [
                            ("success", jsonb_data["urls"]["success"]),
                            ("failure", jsonb_data["urls"]["failure"]),
                            ("error", jsonb_data["urls"]["error"]),
                            ("callback", jsonb_data["urls"]["callback"]),
                        ]
                    ),
                ),
                (
                    "payment_methods",
                    [
                        OrderedDict(
                            [("name", method["name"]), ("config", method["config"])]
                        )
                        for method in jsonb_data["payment_methods"]
                    ],
                ),
            ]
        )

        return yaml.dump(
            ordered_data,
            Dumper=CustomDumper,
            default_flow_style=False,
            sort_keys=False,
        )

    def get_supported_payment_method_names(self) -> list[str]:
        """
        Retrieves the names of the payment methods supported by the merchant.
        """
        return [method["name"] for method in self.configuration_json["payment_methods"]]

    def get_payment_configuration(self, name: str) -> dict:
        """
        Retrieves the payment methods configuration.
        """
        for method in self.configuration_json["payment_methods"]:
            if method["name"] == name:
                return method["config"]

        raise ValueError(f"Payment method {name} not found in the configuration.")

    def get_urls(self) -> dict:
        """
        Retrieves the URLs from the configuration.
        """
        return self.configuration_json["urls"]
