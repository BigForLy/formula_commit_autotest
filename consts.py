# Свойства поля "Значение" в блоке результатов
PROPERTIES_FIELD_VALUE = (
    "rounding_with_zeros",
    "round",
    "parent",
    "read_оnly",
    "RoundResultInAccordanceWithInfelicityRounding",
    "symbol",
    "calculation",
)
# Постфикс для поля "Значение" в блоке результатов
POSTFIX_FIELD_VALUE = "_v"


# Свойства поля "Предел повторяемости" в блоке результатов
PROPERTIES_FIELD_ABSOLUTE_DIFFERENCE = (
    "visible_absolute_difference",
    "round_absolute_difference",
    "validate_calculation_absolute_difference",
    "parent",
    "symbol_absolute_difference",
    "calculation_absolute_difference",
)
# Постфикс для поля "Предел повторяемости" в блоке результатов
POSTFIX_FIELD_ABSOLUTE_DIFFERENCE = "_a"

# Свойства поля "Абсолютное расхождение" в блоке результатов
PROPERTIES_FIELD_CONSISTENCY = (
    "visible_of_consistency",
    "round_limit_of_consistency",
    "validate_calculation_of_consistency",
    "parent",
    "symbol_of_consistency",
    "calculation_limit_of_consistency",
)
# Постфикс для поля "Абсолютное расхождение" в блоке результатов
POSTFIX_FIELD_CONSISTENCY = "_c"

# Свойства поля "Погрешность" в блоке результатов
PROPERTIES_FIELD_INFELICITY = (
    "visible_infelicity",
    "round_infelicity",
    "infelicity_readonly",
    "validate_calculation_infelicity",
    "parent",
    "symbol_infelicity",
    "calculation_infelicity",
    "RoundInfelicityInAccordanceWithResultRounding",
)
# Постфикс для поля "Погрешность" в блоке результатов
POSTFIX_FIELD_INFELICITY = "_i"

# UIN свойства "parent" у полей методов
UIN_PARENT_PROPERTIES = "7b42604d-34e6-11e9-8ecc-00ff1f255572"

# Исключения для проверок
# первичный ключ uin_method_ver, значение список проб для исключения
EXCEPTIONS = {
    "b2fdc65d-6c4e-11e7-8fb2-00ffb44a812c": [
        # Некорректное решение: 2.7 != 2.8 - ошибка в округлении mysql
        b"ebe23667-fa51-11eb-9f29-00155dc7502a",
        # Деление на 0, кроме того данные некорректно записаны в базу,
        # не хватает полей для второго определения
        b"eaed4828-fa51-11eb-9f29-00155dc7502a",
        # Не хватает поля для первого определения
        b"eae97ba7-fa51-11eb-9f29-00155dc7502a",
        # Не хватает полей, некорректные данные
        b"eadfa778-fa51-11eb-9f29-00155dc7502a",
        # Что-то не то с результатом, он в базе 0
        b"eadbeb4b-fa51-11eb-9f29-00155dc7502a",
    ],
    "40f0ac88-d249-11eb-920a-b42e99f35f65": [
        # Некорректное решение: 2.579 != 2.5789999999999997 - ошибка в округлении LIMS
        b"8340ce8d-43dd-11ed-b77f-00155d636aad",
        # Некорректное решение: 2.571 != 2.5709999999999997 - ошибка в округлении LIMS
        b"83408062-43dd-11ed-b77f-00155d636aad",
        # Некорректное решение: 2.571 != 2.5709999999999997 - ошибка в округлении LIMS
        b"83404b7e-43dd-11ed-b77f-00155d636aad",
    ],
    "a06c19f4-fc40-11ec-8e4c-d45d64d460d9": [
        # Некорректное решение: 2.562 != 2.5620000000000003 - ошибка в округлении LIMS
        b"83423239-43dd-11ed-b77f-00155d636aad",
        # Некорректное решение: 2.48 != 2,481. - некорректное округление LIMS
        b"83421c4b-43dd-11ed-b77f-00155d636aad",
    ],
    "0a3bbf6d-d249-11eb-920a-b42e99f35f65": [
        # Некорректное решение: 2.522 != 2.5220000000000002 - ошибка в округлении LIMS
        b"8342628d-43dd-11ed-b77f-00155d636aad",
        # Некорректное решение: 2.522 != 2.5220000000000002. - ошибка в округлении LIMS
        b"83426825-43dd-11ed-b77f-00155d636aad",
        b"83426825-43dd-11ed-b77f-00155d636aad",
        b"834260cf-43dd-11ed-b77f-00155d636aad",
    ],
}
