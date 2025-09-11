from typing import Any
from uuid import UUID

import requests
import yaml
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..discovery import resolve
from ..merchants.models import Merchant
from .models import PaymentMethod


def get_merchant_payment_methods_configuration(
    db: Session,
    current_user_id: UUID,
) -> tuple[dict[str, dict[str, Any]], str]:
    merchant = db.query(Merchant).filter(Merchant.id == current_user_id).first()

    return merchant.configuration_json, merchant.get_configuration_yaml()


def apply_merchant_payment_methods_configuration(
    db: Session,
    config_yaml: str,
    current_user_id: UUID,
) -> tuple[dict, str]:
    try:
        new_config: dict = yaml.safe_load(config_yaml)
    except yaml.YAMLError as e:
        print("Failed to parse YAML configuration:", e)
        raise HTTPException(
            status_code=400, detail="Failed to parse YAML configuration"
        )

    for payment_method in new_config["payment_methods"]:
        name: str = payment_method["name"]
        config: dict = payment_method["config"]

        print(payment_method)

        payment_method = (
            db.query(PaymentMethod).filter(PaymentMethod.name == name).first()
        )
        try:
            payload = {
                "merchant_id": str(current_user_id),
                "configuration": config,
            }

            print(payload)

            host, port = resolve(payment_method.service_name)

            response = requests.post(
                f"http://{host}:{port}/merchants",
                json=payload,
            )
            print(response)
            response.raise_for_status()
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to apply configuration for merchant {current_user_id} on handler {name}: {e}",
            )
        else:
            print(
                f"Configuration for merchant {current_user_id} on handler {name} applied successfully."
            )

    merchant = db.query(Merchant).filter(Merchant.id == current_user_id).first()
    merchant.configuration_json = new_config
    db.commit()

    return merchant.configuration_json, merchant.get_configuration_yaml()


def get_payment_methods(db: Session) -> list[PaymentMethod]:
    return db.query(PaymentMethod).all()


def add_payment_method(db: Session, name: str, service_name: str) -> PaymentMethod:
    host, port = resolve(service_name)
    response = requests.get(f"http://{host}:{port}/schema")
    response.raise_for_status()

    title: str = response.json()["title"]
    config_schema: dict = response.json()["configuration_schema"]

    new_payment_method = PaymentMethod(
        name=name,
        title=title,
        configuration_schema=config_schema,
        service_name=service_name,
    )
    try:
        db.add(new_payment_method)
        db.flush()
        return new_payment_method
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Payment method already exists.")
