from typing import Any
import re

from sqlalchemy.ext.declarative import as_declarative, declared_attr


def convert_camel_case(name: str) -> str:
    name = re.sub(r'(?<!^)(?=[A-Z])', '_', name).lower()
    return name


@as_declarative()
class Base:
    id: Any
    __name__: str
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return convert_camel_case(cls.__name__)