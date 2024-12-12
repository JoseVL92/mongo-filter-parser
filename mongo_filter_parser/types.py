"""Duck-typing pydantic BaseModel, used for typing purposes only"""
from typing import Any, Protocol, runtime_checkable


@runtime_checkable
class BaseModelProtocol(Protocol):
    """Protocol for Pydantic-like model compatibility."""
    model_fields: dict[str, Any]
