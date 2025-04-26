from drf_spectacular.utils import extend_schema

def auto_tag_by_urlprefix(endpoints):
    """
    Auto-tag endpoints based on URL prefix.
    Example:
        /api/products/ → "Products"
        /api/orders/  → "Orders"
    """
    tagged_endpoints = []
    for path, path_regex, method, callback in endpoints:
        # Extract tag from URL (e.g., "/api/products/" → "products")
        tag = None
        if path.startswith('/api/v1/products/'):
            tag = 'Products'
        elif path.startswith('/api/v1/sales/'):
            tag = 'Orders'
        elif path.startswith('/api/v1/categories/'):
            tag = 'Customers'
        elif path.startswith('/api/v1/token/'):
            tag = 'Auth'
        
        # Apply the tag if found
        if tag:
            if hasattr(callback, 'cls'):  # Class-Based View (ViewSet, APIView)
                callback.cls.schema = extend_schema(tags=[tag])(callback.cls.schema)
            elif hasattr(callback, '__name__'):  # Function-Based View (@api_view)
                callback.schema = extend_schema(tags=[tag])(callback)
        
        tagged_endpoints.append((path, path_regex, method, callback))
    return tagged_endpoints