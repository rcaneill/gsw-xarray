from pint import UndefinedUnitError

generic_units = {
    "degree_north": "degree",
    "degree_east": "degree",
    "ppt": "1",
}


def safe_unit(unit, registry):
    """
    If unit in registry, return unit. Otherwise, tries to get the generic
    value.
    If no unit is found, raises a UndefinedUnitError.
    """
    if registry is None:
        return unit
    if unit in registry:
        return unit
    try:
        unit = generic_units[unit]
    except KeyError:
        # Will not be raised unless a registry where the common units are not defined is used
        raise UndefinedUnitError(
            f"The unit '{unit}' is not defined in the unit registry but is necessary for input or output of the gsw function."
        )
    return unit
