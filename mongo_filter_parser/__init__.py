from pydantic import BaseModel
from typing import Union, List
from .filter_builder import MongoFilterBuilder


def build_mongo_filter(query_params: Union[str, dict],
                       exclude_model: BaseModel = None,
                       exclude_fields: List[str] = None) -> dict:
    """
    Converts URL query string (or FastAPI QueryParams dict) into a MongoDB filter query.
    Supports logical operators through the __binding__ parameter.

    Example:
        query = "price__lte=7.8&created_at__lt=2024-05-08&is_verified=false&has_evolved=true&__binding__=((created_at__lt|is_verified)+has_evolved)"
        filter = build_mongo_filter(query)

    The binding expression supports:
        - Parentheses for grouping
        - + for AND operations
        - | for OR operations
    """
    builder = MongoFilterBuilder(query_params, exclude_model, exclude_fields)
    return builder.build()
