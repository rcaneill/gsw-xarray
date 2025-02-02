from sphinx.util import progress_message

from inspect import signature

import gsw_xarray
from gsw_xarray._names import _names
from gsw_xarray._attributes import _func_attrs
from gsw_xarray._arguments import input_units

list_table = ""


def _add_attrs(list_table, attrs, label):
    if (label_value := attrs.get(label)) is not None:
        list_table += f"   * {label}: ``{label_value}``\n"

    return list_table


with progress_message("Generating gsw attribute table"):
    for name, result_name in _names.items():
        sig = signature(getattr(gsw_xarray, name))

        list_table += f"{name}\n{'-' * len(name)}\n"
        list_table += "Expected input units when using pint:\n\n"
        for arg in sig.parameters:
            list_table += f"* ``{arg}``: {input_units.get(arg)}\n"

        list_table += "\n"

        if isinstance(result_name, tuple):
            list_table += f"Has {len(result_name)} outputs\n\n"
            for i, result in enumerate(result_name):
                list_table += f"#. **{result}**\n\n"
                attrs = _func_attrs[name][i]
                list_table = _add_attrs(list_table, attrs, "standard_name")
                list_table = _add_attrs(list_table, attrs, "units")
                list_table = _add_attrs(list_table, attrs, "reference_scale")
                list_table += "\n"

        else:
            attrs = _func_attrs[name]
            list_table += "Has 1 output\n\n"
            list_table += f"#. **{result_name}**\n\n"
            list_table = _add_attrs(list_table, attrs, "standard_name")
            list_table = _add_attrs(list_table, attrs, "units")
            list_table = _add_attrs(list_table, attrs, "reference_scale")
        list_table += "\n"

    with open("_attr_table.rst", "w", encoding="utf8") as f:
        f.write(list_table)
