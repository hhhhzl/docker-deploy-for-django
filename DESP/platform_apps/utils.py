def make_filter_kwargs(query_params, filter_fields):
    """
    Construct filter kwargs from query parameters in <view>.get_queryset()
    """
    return {
        field: query_params.get(field)
        for field in filter_fields
        if query_params.get(field) is not None
    }
