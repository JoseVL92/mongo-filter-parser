"""MongoDB filter builder implementation."""
from typing import Dict, List, Union, Any
from urllib.parse import parse_qs

from .parser import BindingParser
from .types import BaseModelProtocol
from .field_builder import FieldBuilder
from .logical_builder import LogicalBuilder


class MongoFilterBuilder:
    def __init__(self,
                 query_params: Union[str, Dict[str, Any]],
                 exclude_model: Union[BaseModelProtocol, None] = None,
                 exclude_fields: List[str] = None):
        """Initialize the filter builder."""
        self.query_params = self._normalize_query_params(query_params)
        self.excluded_fields = self._get_excluded_fields(exclude_model, exclude_fields)
        self.field_builder = FieldBuilder(self.query_params)
        self.logical_builder = LogicalBuilder(self.query_params)

    def build(self) -> Dict[str, Any]:
        """Build MongoDB filter with logical operators support."""
        binding = self.query_params.pop('__binding__', None)

        if not binding:
            return self._build_simple_filter()

        return self._build_filter_with_binding(binding)

    def _build_simple_filter(self) -> Dict[str, Any]:
        """Build MongoDB filter without logical operators."""
        mongo_filter = {}

        for key in self.query_params:
            if key in self.excluded_fields:
                continue

            field_filter = self.field_builder.build_field_filter(key)
            base_field = key.split('__')[0]

            if base_field in mongo_filter:
                mongo_filter = self.field_builder.merge_field_filters(
                    mongo_filter,
                    field_filter
                )
            else:
                mongo_filter.update(field_filter)

        return mongo_filter

    def _build_filter_with_binding(self, binding: str) -> Dict[str, Any]:
        """Build MongoDB filter with logical operators based on binding expression."""
        parser = BindingParser(binding)
        logical_expr = parser.parse()
        return self.logical_builder.build_logical_expression(logical_expr)

    @staticmethod
    def _normalize_query_params(query_params: Union[str, Dict]) -> Dict:
        """Convert query string to dictionary if needed."""
        if isinstance(query_params, str):
            return {k: v[0] for k, v in parse_qs(query_params).items()}
        return query_params

    @staticmethod
    def _get_excluded_fields(exclude_model: Union[BaseModelProtocol, None] = None,
                             exclude_fields: List[str] = None) -> List[str]:
        """Get list of excluded fields."""
        excluded = []
        if exclude_model is not None and hasattr(exclude_model, 'model_fields'):
            excluded.extend(exclude_model.model_fields.keys())
        if exclude_fields:
            excluded.extend(exclude_fields)
        return excluded
