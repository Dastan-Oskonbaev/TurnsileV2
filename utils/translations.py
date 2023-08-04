def get_field_verbose_name(model, field_name):
    return model._meta.get_field(field_name).verbose_name


def get_field_by_verbose_name(model, verbose_name):
    for field in model._meta.fields:
        if field.verbose_name == verbose_name:
            return field.name
    return None
