from enum import Enum
from typing import Dict, Any


class CognitoGroup(str, Enum):
    GENERAL_USER = "GENERAL_USER"
    ADMIN = "ADMIN"


COGNITO_GROUP_INFO: Dict[str, Dict[str, Any]] = {
    CognitoGroup.GENERAL_USER: {
        "description": "Usuarios generales con acceso básico",
        "precedence": 10,
        "permissions": [
            "read:activities",
            "read:trips",
            "create:saved_lists",
            "update:own_profile"
        ]
    },
    CognitoGroup.ADMIN: {
        "description": "Administradores con acceso completo al sistema",
        "precedence": 1,
        "permissions": [
            "all:activities",
            "all:trips",
            "all:users",
            "all:system"
        ]
    }
}


def get_default_group() -> str:
    return CognitoGroup.GENERAL_USER


def is_valid_group(group_name: str) -> bool:
    return group_name in [group.value for group in CognitoGroup]


def get_group_info(group_name: str) -> Dict[str, Any]:
    if not is_valid_group(group_name):
        raise ValueError(f"Grupo inválido: {group_name}")
    return COGNITO_GROUP_INFO.get(group_name, {}) 