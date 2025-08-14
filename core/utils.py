def update_fields_on_obj(obj, dict_to_update):
    for key, value in dict_to_update.items():
        setattr(obj, key, value)