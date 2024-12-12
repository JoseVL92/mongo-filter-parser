"""Logical builder module for constructing MongoDB logical expressions."""
from typing import Dict, Union, Any

from .exceptions import OperatorError
from .operators import LOGICAL_OPERATORS
from .parser import LogicalExpression
from .field_builder import FieldBuilder


class LogicalBuilder:
    """Builds MongoDB filters with logical operators."""

    def __init__(self, query_params: Dict[str, Any]):
        self.query_params = query_params
        self.field_builder = FieldBuilder(query_params)

    def build_logical_expression(self, expr: Union[LogicalExpression, str]) -> Dict[str, Any]:
        """Convert logical expression to MongoDB filter."""
        if isinstance(expr, str):
            # It's a field name
            if expr not in self.query_params:
                raise OperatorError(f"Field '{expr}' referenced in binding but not in query params")
            return self.field_builder.build_field_filter(expr)

        # It's a logical expression
        mongo_op = LOGICAL_OPERATORS[expr.operator]
        operands = []

        # Process each operand
        for op in expr.operands:
            operand_filter = self.build_logical_expression(op)

            # If nested expression has same operator, flatten it
            if isinstance(operand_filter, dict) and mongo_op in operand_filter:
                operands.extend(operand_filter[mongo_op])
            else:
                operands.append(operand_filter)

        # Return the flattened structure
        return {mongo_op: operands}
