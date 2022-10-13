from sqlalchemy.orm.session import Session
from sqlalchemy.sql import func, expression
from sqlalchemy import literal
from sqlalchemy.orm import aliased
from consts import (
    POSTFIX_FIELD_ABSOLUTE_DIFFERENCE,
    POSTFIX_FIELD_CONSISTENCY,
    POSTFIX_FIELD_INFELICITY,
    POSTFIX_FIELD_VALUE,
    UIN_PARENT_PROPERTIES,
)
from models import *


def get_queryset_fields_s_properties(session: Session, uin_method_ver: str):
    return (
        session.query(
            KcrValuePropertiesField.uin_field,
            KcrValuePropertiesField.value,
            KtProperties.uin_name,
            KtFieldType.uin_name.label("type_uin_name"),
        )
        .select_from(KtMethodVer)
        .join(KtSField)
        .join(KtField)
        .join(KcrValuePropertiesField)
        .join(KcrFieldTypeProperties)
        .join(KtProperties)
        .join(KtFieldType)
        .filter(KtMethodVer.uin_method_ver == uin_method_ver)
    ).all()


def get_queryset_fields_result_properties(session: Session, uin_method_ver: str):
    return (
        session.query(
            KcrValuePropertiesField.uin_field,
            KcrValuePropertiesField.value,
            KtProperties.uin_name,
            KtFieldType.uin_name.label("type_uin_name"),
        )
        .select_from(KtMethodVer)
        .join(KtResultField)
        .join(KtField)
        .join(KcrValuePropertiesField)
        .join(KcrFieldTypeProperties)
        .join(KtProperties)
        .join(KtFieldType)
        .filter(KtMethodVer.uin_method_ver == uin_method_ver)
    ).all()


def get_method_values(session: Session, probe, uin_method_ver: str):
    return s_fields_values(session, probe.uin, uin_method_ver) + result_fields_values(
        session, probe.uin, uin_method_ver, probe.uin_pokazatel
    )


def s_fields_values(session: Session, probe_uin: str, uin_method_ver: str):
    num_values_query = (
        session.query(
            KtSField.uin_s_field.label("uin"),
            KtSNumOpred.num.label("definition"),
            func.coalesce(KtSFieldValueNum.value).label("value"),
            KtField.order_by.label("order_by"),
            KtSField.common.label("common"),
        )
        .select_from(KtSNumOpred)
        .join(Probe)
        .join(KtSFieldValueNum)
        .join(KtSField)
        .join(KtField)
        .filter(
            expression.and_(
                KtSNumOpred.uin_method_ver == uin_method_ver,
                Probe.uin == probe_uin,
            )
        )
    )
    text_values_query = (
        session.query(
            KtSField.uin_s_field.label("uin"),
            KtSNumOpred.num.label("definition"),
            func.coalesce(KtSFieldValueText.value).label("value"),
            KtField.order_by.label("order_by"),
            KtSField.common.label("common"),
        )
        .select_from(KtSNumOpred)
        .join(Probe)
        .join(KtSFieldValueText)
        .join(KtSField)
        .join(KtField)
        .filter(
            expression.and_(
                KtSNumOpred.uin_method_ver == uin_method_ver,
                Probe.uin == probe_uin,
            )
        )
    )
    query = session.query(
        expression.union(text_values_query, num_values_query).subquery()
    ).order_by("common", "order_by")
    return query.all()


def result_fields_values(
    session: Session, probe_uin: str, uin_method_ver: str, uin_pokazatel: str
):
    pokazatel_1: Pokazatel = aliased(Pokazatel, name="tp1")
    pokazatel_2: Pokazatel = aliased(Pokazatel, name="tp2")
    pokazatel_3: Pokazatel = aliased(Pokazatel, name="tp3")
    probe_result_1: ProbeResult = aliased(ProbeResult, name="tpr1")
    probe_result_2: ProbeResult = aliased(ProbeResult, name="tpr2")
    subquery_fields_result = (
        session.query(
            probe_result_2.value.label("value"),
            probe_result_2.lim_repeat.label("lim_repeat"),
            probe_result_2.abs_rasx.label("abs_rasx"),
            probe_result_2.infelicity.label("infelicity"),
            KtResultField.uin_result_field.label("uin"),
            KcrValuePropertiesField.value.label("block_uin"),
        )
        .select_from(probe_result_1)
        .outerjoin(Probe)
        .outerjoin(
            pokazatel_1,
            pokazatel_1.pokazatel_id == probe_result_1.pokazatel_id,
        )
        .outerjoin(Method, Method.method_id == pokazatel_1.pokazatel_method_id)
        .outerjoin(
            pokazatel_2,
            pokazatel_2.pokazatel_method_id == Method.method_id,
        )
        .join(
            probe_result_2,
            expression.and_(
                probe_result_2.probe_id == probe_result_1.probe_id,
                probe_result_2.pokazatel_id == pokazatel_2.pokazatel_id,
                probe_result_2.uin_method_ver == probe_result_1.uin_method_ver,
                probe_result_2.condition == probe_result_1.condition,
            ),
        )
        .outerjoin(
            pokazatel_3,
            pokazatel_3.pokazatel_id == probe_result_2.pokazatel_id,
        )
        .outerjoin(
            CrResultFieldPokazatel,
            CrResultFieldPokazatel.uin_pokazatel == pokazatel_3.uin_pokazatel,
        )
        .join(
            KtResultField,
            expression.and_(
                KtResultField.uin_result_field
                == CrResultFieldPokazatel.uin_field_result,
                KtResultField.uin_method_ver == probe_result_2.uin_method_ver,
            ),
        )
        .outerjoin(KtField, KtField.uin_field == KtResultField.uin_result_field)
        .outerjoin(
            KcrValuePropertiesField,
            KcrValuePropertiesField.uin_field == KtField.uin_field,
        )
        .outerjoin(KcrFieldTypeProperties)
        .filter(
            expression.and_(
                probe_result_1.uin_method_ver == uin_method_ver,
                Probe.uin == probe_uin,
                pokazatel_1.uin_pokazatel == uin_pokazatel,
                KcrFieldTypeProperties.uin_properties == UIN_PARENT_PROPERTIES,
            )
        )
        .subquery()
    )

    query_value = session.query(
        literal("1").label("definition"),
        literal(False).label("is_common"),
        literal("result").label("block_type"),
        subquery_fields_result.c.value.label("value"),
        subquery_fields_result.c.uin.label("order_uin"),
        func.concat(subquery_fields_result.c.uin, POSTFIX_FIELD_VALUE).label("uin"),
        subquery_fields_result.c.block_uin.label("block_uin"),
    )

    query_absolute_difference = session.query(
        literal("1").label("definition"),
        literal(False).label("is_common"),
        literal("result").label("block_type"),
        subquery_fields_result.c.lim_repeat.label("value"),
        subquery_fields_result.c.uin.label("order_uin"),
        func.concat(
            subquery_fields_result.c.uin, POSTFIX_FIELD_ABSOLUTE_DIFFERENCE
        ).label("uin"),
        subquery_fields_result.c.block_uin.label("block_uin"),
    )

    query_consistency = session.query(
        literal("1").label("definition"),
        literal(False).label("is_common"),
        literal("result").label("block_type"),
        subquery_fields_result.c.abs_rasx.label("value"),
        subquery_fields_result.c.uin.label("order_uin"),
        func.concat(subquery_fields_result.c.uin, POSTFIX_FIELD_CONSISTENCY).label(
            "uin"
        ),
        subquery_fields_result.c.block_uin.label("block_uin"),
    )

    query_infelicity = session.query(
        literal("1").label("definition"),
        literal(False).label("is_common"),
        literal("result").label("block_type"),
        subquery_fields_result.c.infelicity.label("value"),
        subquery_fields_result.c.uin.label("order_uin"),
        func.concat(subquery_fields_result.c.uin, POSTFIX_FIELD_INFELICITY).label(
            "uin"
        ),
        subquery_fields_result.c.block_uin.label("block_uin"),
    )

    query = (
        session.query(
            expression.union(
                query_value,
                query_absolute_difference,
                query_consistency,
                query_infelicity,
            ).subquery()
        )
        .order_by("order_uin")
        .all()
    )
    return query


def get_probe_uin_in_probe_result(
    session: Session, uin_method_ver: str, limit_: int = 500
):
    return (
        session.query(Probe.uin, Pokazatel.uin_pokazatel)
        .select_from(ProbeResult)
        .join(Probe)
        .join(Pokazatel, Pokazatel.pokazatel_id == ProbeResult.pokazatel_id)
        .filter(
            expression.and_(
                ProbeResult.uin_method_ver == uin_method_ver,
                ProbeResult.value.is_not(None),
                ProbeResult.value != "",
            )
        )
        .order_by(Probe.probe_id.desc())
        .limit(limit_)
    ).all()
