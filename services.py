import copy
from typing import Any, Dict
from decimal import Decimal
from formula_commit import (
    FormulaCalculation,
    StringField,
    NumericField,
    BoolField,
    BaseField,
)
from factory import (
    AbsoluteDifferenceField,
    InfelicityField,
    ValueField,
    ConsistencyField,
)
from consts import (
    EXCEPTIONS,
    PROPERTIES_FIELD_ABSOLUTE_DIFFERENCE,
    PROPERTIES_FIELD_CONSISTENCY,
    PROPERTIES_FIELD_INFELICITY,
    PROPERTIES_FIELD_VALUE,
)
from decorator_ import counter

from query import get_method_values


def get_field(arg: Dict[str, Any]):  # static factory method
    type_ = arg.get("type_uin_name", None)
    if type_ == "user":
        return {arg["primary_key"]: StringField(**arg, formula="", value="", symbol="")}
    elif type_ == "date_time":  # create new type
        return {arg["primary_key"]: StringField(**arg, formula="", value="", symbol="")}
    elif type_ == "field_with_number":
        return {
            arg["primary_key"]: NumericField(
                **arg,
                formula=arg.get("calculation"),
                value="",
                round_to=int(arg.get("round")),
                is_required=True if arg["not_is_null"] == "True" else False,
                is_round_with_zeros=True
                if arg["rounding_with_zeros"] == "True"
                else False,
            )
        }
    elif type_ == "field_with_string":
        return {
            arg["primary_key"]: StringField(
                **arg,
                formula=arg.get("calculation"),
                value="",
                is_required=True if arg["not_is_null"] == "True" else False,
            )
        }
    elif type_ == "result_field":
        value_field_properties = {
            "primary_key": arg["primary_key"],
            "is_required": False,
            "is_round_with_zeros": True
            if arg["rounding_with_zeros"] == "True"
            else False,
        }
        absolute_difference_properties = {
            "primary_key": arg["primary_key"],
            "is_required": False,
            "is_round_with_zeros": True
            if arg["rounding_with_zeros"] == "True"
            else False,
        }
        consistency_field_properties = {
            "primary_key": arg["primary_key"],
            "is_required": False,
            "is_round_with_zeros": True
            if arg["rounding_with_zeros"] == "True"
            else False,
        }
        infelicity_field_properties = {
            "primary_key": arg["primary_key"],
            "is_required": False,
            "is_round_with_zeros": True
            if arg["rounding_with_zeros"] == "True"
            else False,
        }

        for name, value in arg.items():
            if name in PROPERTIES_FIELD_VALUE:
                value_field_properties[name] = value
            if name in PROPERTIES_FIELD_ABSOLUTE_DIFFERENCE:
                absolute_difference_properties[name] = value
            if name in PROPERTIES_FIELD_CONSISTENCY:
                consistency_field_properties[name] = value
            if name in PROPERTIES_FIELD_INFELICITY:
                infelicity_field_properties[name] = value

        return [
            (element.primary_key, element)
            for element in (
                ValueField.create_from(**value_field_properties),
                AbsoluteDifferenceField.create_from(**absolute_difference_properties),
                ConsistencyField.create_from(**consistency_field_properties),
                InfelicityField.create_from(**infelicity_field_properties),
            )
        ]
    elif type_ == "input_manual":
        return {arg["primary_key"]: BoolField(**arg, symbol=type_, value=0, formula="")}
    elif type_ == "logic":
        return {arg["primary_key"]: BoolField(**arg, value=0, formula="")}
    else:
        raise ValueError(f"Не найден тип {type_}")


def get_method_fields(queryset) -> Dict[str, Any]:
    uin = ""
    data = {}
    xs = {}
    for elem in queryset:
        if uin != elem.uin_field:
            if uin:
                xs.update(get_field(data))
                data = {}
            uin = elem.uin_field
            data.update({"type_uin_name": elem.type_uin_name})
            data.update({"primary_key": elem.uin_field})
        data.update({elem.uin_name: elem.value})
    if data:
        xs.update(get_field(data))
    return xs


def checked_func(session, probes, method_fields, uin_method_ver):
    for probe in probes:
        assert probe.uin is not None, "probe_uin is None"
        if uin_method_ver in EXCEPTIONS and probe.uin in EXCEPTIONS[uin_method_ver]:
            continue
        check_values_in_probe(session, probe, method_fields, uin_method_ver)
    print(f"Безошибочных проверок: {check_values_in_probe.n_count}")


@counter
def check_values_in_probe(session, probe, method_fields, uin_method_ver):
    try:
        fields = []
        for value in (
            method_values := get_method_values(session, probe, uin_method_ver)
        ):
            field: BaseField = copy.copy(method_fields[value.uin])
            field.definition_number = value.definition
            field.value = value.value
            field.primary_key = (field.primary_key, value.definition)
            fields.append(field)
        results = FormulaCalculation(fields).calc()
        check_fields_result(method_values, results, fields)
    except Exception as exc:
        message = f"Ошибка в версии метода: {uin_method_ver}, проба: {probe.uin}"
        n_count_not_error_message = (
            f"Безошибочных проверок: {check_values_in_probe.n_count}"
        )
        print(exc, message, n_count_not_error_message, sep="\n")
        raise ValueError(message) from exc


def check_fields_result(method_values, results, fields):
    for i in range(len(method_values) - 1):
        values = method_values[i]
        value = results[(values.uin, values.definition)]
        if values.value is None and value == "None":
            continue
        # если values.value конвертируется в число
        # то ожидаем что value тоже будет конвертировано без ошибки
        if is_convert_str_to_float(values.value):
            # В базе некорректно лежат значения, без округления, приходится округлять
            db_value = round(
                Decimal(values.value.replace(",", ".")), abs(fields[i].round_to)
            )
            assert (
                Decimal(value) == db_value
            ), f"Некорректное решение: {value} != {db_value}. Поле: {values.uin} определение: {values.definition}"

            continue
        assert (
            value == values.value
        ), f"Некорректное решение: {value} != {values.value}. Поле: {values.uin} определение: {values.definition}"


def is_convert_str_to_float(value: str) -> bool:
    try:
        float(value.replace(",", "."))
        return True
    except:
        return False
