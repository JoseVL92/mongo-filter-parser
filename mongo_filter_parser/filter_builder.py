from typing import Dict, List, Union
from pydantic import BaseModel
from urllib.parse import parse_qs

from .operators import COMPARISON_OPERATORS, LOGICAL_OPERATORS
from .parser import BindingParser, LogicalExpression
from .value_parser import parse_value


class MongoFilterBuilder:
    def __init__(self,
                 query_params: Union[str, Dict],
                 exclude_model: BaseModel = None,
                 exclude_fields: List[str] = None):
        self.query_params = self._normalize_query_params(query_params)
        self.excluded_fields = self._get_excluded_fields(exclude_model, exclude_fields)

    def build(self) -> Dict:
        """Build MongoDB filter with logical operators support."""
        binding = self.query_params.pop('__binding__', None)

        if not binding:
            return self._build_simple_filter()

        return self._build_filter_with_binding(binding)

    def _build_simple_filter(self) -> Dict:
        """Build MongoDB filter without logical operators."""
        mongo_filter = {}

        for key, value in self.query_params.items():
            if key in self.excluded_fields:
                continue

            if '__' in key:
                field, op = key.split('__', 1)
                if op in COMPARISON_OPERATORS:
                    if field not in mongo_filter:
                        mongo_filter[field] = {}
                    mongo_filter[field][COMPARISON_OPERATORS[op]] = parse_value(value)
                else:
                    raise ValueError(f"Unsupported operator: {op}")
            else:
                mongo_filter[key] = parse_value(value)

        return mongo_filter

    def _build_filter_with_binding(self, binding: str) -> Dict:
        """Build MongoDB filter with logical operators based on binding expression."""
        parser = BindingParser(binding)
        logical_expr = parser.parse()
        return self._build_logical_expression(logical_expr)

    def _build_logical_expression(self, expr: Union[LogicalExpression, str]) -> Dict:
        """Convert logical expression to MongoDB filter."""
        if isinstance(expr, str):
            # It's a field name
            if expr not in self.query_params:
                raise ValueError(f"Field '{expr}' referenced in binding but not in query params")
            return self._build_field_filter(expr)

        # It's a logical expression
        mongo_op = LOGICAL_OPERATORS[expr.operator]
        operands = [self._build_logical_expression(op) for op in expr.operands]
        return {mongo_op: operands}

    def _build_field_filter(self, field: str) -> Dict:
        """Build filter for a single field."""
        if '__' in field:
            base_field, op = field.split('__', 1)
            if op in COMPARISON_OPERATORS:
                # Special handling for regex operator
                if op == 'regex':
                    return {
                        base_field: {
                            '$regex': parse_value(self.query_params[field]),
                            '$options': 'i'  # Case insensitive
                        }
                    }
                return {
                    base_field: {
                        COMPARISON_OPERATORS[op]: parse_value(self.query_params[field])
                    }
                }
        return {field: parse_value(self.query_params[field])}

    @staticmethod
    def _normalize_query_params(query_params: Union[str, Dict]) -> Dict:
        """Convert query string to dictionary if needed."""
        if isinstance(query_params, str):
            return {k: v[0] for k, v in parse_qs(query_params).items()}
        return dict(query_params)

    @staticmethod
    def _get_excluded_fields(exclude_model: BaseModel = None,
                             exclude_fields: List[str] = None) -> List[str]:
        """Get list of excluded fields."""
        excluded = []
        if exclude_model:
            excluded.extend(exclude_model.model_fields.keys())
        if exclude_fields:
            excluded.extend(exclude_fields)
        return excluded
