from typing import Dict, List, Union, Any

from .types import BaseModelProtocol
from .filter_builder import MongoFilterBuilder

def build_mongo_filter(query_params: Union[str, Dict[str, Any]],
                      exclude_model: Union[BaseModelProtocol, None] = None,
                      exclude_fields: List[str] = None) -> Dict[str, Any]:
    """
    Converts URL query string (or FastAPI QueryParams dict) into a MongoDB filter query.
    
    Args:
        query_params: URL query string or dictionary of parameters
        exclude_model: Optional Pydantic-like model for field exclusion
        exclude_fields: Optional list of field names to exclude
        
    Returns:
        MongoDB filter dictionary
    """
    builder = MongoFilterBuilder(query_params, exclude_model, exclude_fields)
    return builder.build()
