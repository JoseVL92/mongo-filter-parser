from mongo_filter_parser.filter_builder import MongoFilterBuilder


def print_filter(query_params: dict, binding: str) -> None:
    """Helper function to demonstrate filter building with different bindings."""
    params = query_params.copy()
    params['__binding__'] = binding
    builder = MongoFilterBuilder(params)
    result = builder.build()
    print(f"\nBinding: {binding}")
    print("MongoDB Filter:", result)

def run_examples():
    # Sample query parameters
    base_params = {
        'created_at__lt': '2024-05-08',
        'is_verified': 'false',
        'has_evolved': 'true',
        'evolution_rate__lt': '12',
        'email__regex': 'user@',
        'name__regex': 'john'
    }

    # Example 1: Simple OR with AND
    print_filter(
        base_params,
        'created_at__lt|is_verified+has_evolved'
    )

    # Example 2: Grouped OR with AND
    print_filter(
        base_params,
        '(created_at__lt|is_verified)+has_evolved'
    )

    # Example 3: Complex nested expression with regex
    print_filter(
        base_params,
        'email__regex|name__regex+(has_evolved|evolution_rate__lt)'
    )

    # Example 4: Complex grouped expression
    print_filter(
        base_params,
        '(created_at__lt|is_verified)+(has_evolved|evolution_rate__lt)'
    )

if __name__ == '__main__':
    run_examples()