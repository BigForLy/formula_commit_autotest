import copy
from typing import Any, Dict
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
    PROPERTIES_FIELD_ABSOLUTE_DIFFERENCE,
    PROPERTIES_FIELD_CONSISTENCY,
    PROPERTIES_FIELD_INFELICITY,
    PROPERTIES_FIELD_VALUE,
)
from decorator import counter

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
        }
        absolute_difference_properties = {
            "primary_key": arg["primary_key"],
            "is_required": False,
        }
        consistency_field_properties = {
            "primary_key": arg["primary_key"],
            "is_required": False,
        }
        infelicity_field_properties = {
            "primary_key": arg["primary_key"],
            "is_required": False,
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
        if uin_method_ver == "b2fdc65d-6c4e-11e7-8fb2-00ffb44a812c" and probe.uin in (
            # Некорректное решение: 2.7 != 2.8 - ошибка в округлении mysql
            b"ebe23667-fa51-11eb-9f29-00155dc7502a",
            # Деление на 0, кроме того данные некорректно записаны в базу,
            # нехватает полей для второго определения
            b"eaed4828-fa51-11eb-9f29-00155dc7502a",
            # Нехватает поля для первого определения
            b"eae97ba7-fa51-11eb-9f29-00155dc7502a",
            # Нехватает полей, некорректные данные
            b"eadfa778-fa51-11eb-9f29-00155dc7502a",
            # Что-то не то с результатом, он в базе 0
            b"eadbeb4b-fa51-11eb-9f29-00155dc7502a",
        ):
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
        formula = FormulaCalculation(fields)
        results = formula.calc()
        check_fields_result(method_values, results)
    except Exception as exc:
        message = f"Ошибка в версии метода: {uin_method_ver}, проба: {probe.uin}"
        n_count_not_error_message = (
            f"Безошибочных проверок: {check_values_in_probe.n_count}"
        )
        print(exc, message, n_count_not_error_message, sep="\n")
        raise ValueError(message) from exc


def check_fields_result(method_values, results):
    for values in method_values:
        value = results[(values.uin, values.definition)]
        assert (
            value == values.value.replace(",", ".")
            if is_convert_str_to_float(values.value)
            else value == values.value
        ), f"Некорректное решение: {value} != {values.value}. Поле: {values.uin} определение: {values.definition}"


def is_convert_str_to_float(value: str) -> bool:
    try:
        float(value.replace(",", "."))
        return True
    except:
        return False


def convert_str_to_float(value: str) -> float:
    return float(value)
