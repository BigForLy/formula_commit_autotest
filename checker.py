from query import (
    get_probe_uin_in_probe_result,
    get_queryset_fields_result_properties,
    get_queryset_fields_s_properties,
)
from services import checked_func, get_method_fields


def ckecked(session, uin_method_ver):
    method_fields = get_method_fields(
        get_queryset_fields_s_properties(session, uin_method_ver)
        + get_queryset_fields_result_properties(session, uin_method_ver)
    )

    checked_func(
        session,
        get_probe_uin_in_probe_result(session, uin_method_ver),
        method_fields,
        uin_method_ver,
    )
