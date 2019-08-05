def get_object_id(obj, assign_new_key = False, force_insertion = False):
    global _runtime_id
    # Force_insertion implies assign_new_key
    assert not force_insertion or assign_new_key
    for identifier in _id2obj:
        if _id2obj[identifier] is obj:
            if force_insertion:
        return new_id
    return None

