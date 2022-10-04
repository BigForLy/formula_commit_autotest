from formula_commit import StringField

from consts import (
    POSTFIX_FIELD_ABSOLUTE_DIFFERENCE,
    POSTFIX_FIELD_INFELICITY,
    POSTFIX_FIELD_VALUE,
    POSTFIX_FIELD_CONSISTENCY,
)


class ValueField:
    @staticmethod
    def create_from(**kwargs) -> StringField:
        kwargs["primary_key"] = (
            kwargs["primary_key"].decode() + POSTFIX_FIELD_VALUE
        ).encode()
        return StringField(
            **kwargs,
            round_to=int(kwargs.get("round")),
            formula=kwargs["calculation"],
            value=""
        )


class AbsoluteDifferenceField:
    @staticmethod
    def create_from(**kwargs) -> StringField:
        kwargs["primary_key"] = (
            kwargs["primary_key"].decode() + POSTFIX_FIELD_ABSOLUTE_DIFFERENCE
        ).encode()
        return StringField(
            **kwargs,
            round_to=int(kwargs.get("round_absolute_difference")),
            formula=kwargs["calculation_absolute_difference"],
            symbol=kwargs["symbol_absolute_difference"],
            value=""
        )


class ConsistencyField:
    @staticmethod
    def create_from(**kwargs) -> StringField:
        kwargs["primary_key"] = (
            kwargs["primary_key"].decode() + POSTFIX_FIELD_CONSISTENCY
        ).encode()
        return StringField(
            **kwargs,
            round_to=int(kwargs.get("round_limit_of_consistency")),
            formula=kwargs["calculation_limit_of_consistency"],
            symbol=kwargs["symbol_of_consistency"],
            value=""
        )


class InfelicityField:
    @staticmethod
    def create_from(**kwargs) -> StringField:
        kwargs["primary_key"] = (
            kwargs["primary_key"].decode() + POSTFIX_FIELD_INFELICITY
        ).encode()
        return StringField(
            **kwargs,
            round_to=int(kwargs.get("round_infelicity")),
            formula=kwargs["calculation_infelicity"],
            symbol=kwargs["symbol_infelicity"],
            value=""
        )
