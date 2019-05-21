def _serialize_object_into_file(name, p):
    """Serialize an object into a file if necessary.
    :param name: Name of the object
    :param p: Object wrapper
    :return: p (whose type and value might be modified)
    """
    if p.type == TYPE.OBJECT or p.is_future:
        # 2nd condition: real type can be primitive, but now it's acting as a future (object)
        try:
        ...
         _turn_into_file(name, p)
    ...
    elif p.type == TYPE.COLLECTION:
        # Just make contents available as serialized files (or objects)
        # We will build the value field later
        # (which will be used to reconstruct the collection in the worker)
        from pycompss.api.parameter import get_compss_type
        new_object = [
            _serialize_object_into_file(
                name,
                Parameter(
                    p_type = get_compss_type(x, p.depth),
                    p_direction = p.direction,
                    p_object = x,
                    depth = p.depth - 1
                )
            )
            for x in p.object
        ]
        p.object = new_object
        # Give this object an identifier inside the binding
        get_object_id(p.object, True, False)
    return p
