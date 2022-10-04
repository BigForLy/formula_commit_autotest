from sqlalchemy.orm import declarative_base
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    Integer,
    DateTime,
    Boolean,
    Float,
    Date,
    SmallInteger,
)


Base = declarative_base()


class KcrValuePropertiesField(Base):
    __tablename__ = "kcr_value_properties_field"
    uin_value_properties_field = Column(
        "uin_value_properties_field", String(36), primary_key=True, nullable=False
    )
    uin_field_type_properties = Column(
        "uin_field_type_properties",
        String(36),
        ForeignKey("kcr_field_type_properties.uin_field_type_properties"),
        nullable=False,
    )
    uin_field = Column(
        "uin_field", String(36), ForeignKey("kt_field.uin_field"), nullable=False
    )
    value = Column("value", String(10000), nullable=False, default="")
    order_by = Column("order_by", Integer, nullable=False, default=0)


class KtProperties(Base):
    __tablename__ = "kt_properties"
    uin_properties = Column(
        "uin_properties", String(36), primary_key=True, nullable=False
    )
    uin_name = Column("uin_name", String(50), nullable=False, default="")
    description = Column("description", String(255), nullable=False, default="")
    repository_properties = Column(
        "repository_properties", String(50), nullable=False, default="TextEdit"
    )


class KtFieldType(Base):
    __tablename__ = "kt_field_type"
    uin_field_type = Column(
        "uin_field_type", String(36), primary_key=True, nullable=False
    )
    uin_name = Column("uin_name", String(50), nullable=False, default="")
    description = Column("description", String(255), nullable=False, default="")
    repository_properties = Column(
        "repository_properties", String(50), nullable=False, default=""
    )
    type = Column("type", Boolean, nullable=False)
    required = Column("required", Boolean, nullable=False)
    block_common = Column("block_common", Boolean, nullable=False)
    block_assay = Column("block_assay", Boolean, nullable=False)
    block_result = Column("block_result", Boolean, nullable=False)


class KtMethodVer(Base):
    __tablename__ = "kt_method_ver"
    uin_method_ver = Column(
        "uin_method_ver", String(36), primary_key=True, nullable=False
    )
    uin_method = Column(
        "uin_method",
        String(100),
        nullable=False,
        default="",
    )
    max_count_opred = Column("max_count_opred", Integer, nullable=False, default=10)
    simple_or_complete = Column(
        "simple_or_complete", Integer, nullable=False, default=1
    )
    datetimets = Column("datetimets", DateTime, nullable=False)
    build = Column("build", Boolean, nullable=False)


class KtSField(Base):
    __tablename__ = "kt_s_field"
    uin_s_field = Column(
        "uin_s_field",
        String(36),
        ForeignKey("kt_field.uin_field"),
        primary_key=True,
        nullable=False,
    )
    uin_method_ver = Column(
        "uin_method_ver",
        String(36),
        ForeignKey("kt_method_ver.uin_method_ver"),
        nullable=False,
    )
    common = Column("common", Boolean, nullable=False)
    type = Column("type", Boolean, nullable=False)


class KtField(Base):
    __tablename__ = "kt_field"
    uin_field = Column("uin_field", String(36), primary_key=True, nullable=False)
    uin_type_field = Column(
        "uin_type_field",
        String(36),
        nullable=False,
    )
    order_by = Column("order_by", Integer, nullable=False, default=0)


class KcrFieldTypeProperties(Base):
    __tablename__ = "kcr_field_type_properties"
    uin_field_type_properties = Column(
        "uin_field_type_properties", String(36), primary_key=True, nullable=False
    )
    uin_properties = Column(
        "uin_properties",
        String(36),
        ForeignKey("kt_properties.uin_properties"),
        nullable=False,
    )
    uin_field_type = Column(
        "uin_field_type",
        String(36),
        ForeignKey("kt_field_type.uin_field_type"),
        nullable=False,
    )
    values = Column("values", String(1023), nullable=True)
    default_value = Column("default_value", String(1023), nullable=False, default="")


class KtSNumOpred(Base):
    __tablename__ = "kt_s_num_opred"
    id_s_num_opred = Column(
        "id_s_num_opred", Integer, primary_key=True, autoincrement=True, nullable=False
    )
    num = Column("num", Integer, nullable=False, default=1)
    condition = Column("condition", String(255), nullable=False, default="")
    probe_id = Column(
        "probe_id", Integer, ForeignKey("t_probe.probe_id"), nullable=True
    )
    uin_method_ver = Column(
        "uin_method_ver",
        String(36),
        ForeignKey("kt_method_ver.uin_method_ver"),
        nullable=False,
        default="0x30",
    )
    numY = Column("numY", Integer, nullable=False, default=1)


class KtSFieldValueNum(Base):
    __tablename__ = "kt_s_field_value_num"
    id_s_field_value = Column(
        "id_s_field_value",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    uin_s_field = Column(
        "uin_s_field", String(36), ForeignKey("kt_s_field.uin_s_field"), nullable=False
    )
    id_s_num_opred = Column(
        "id_s_num_opred",
        Integer,
        ForeignKey("kt_s_num_opred.id_s_num_opred"),
        nullable=False,
        default=1,
    )
    value = Column("value", Float, nullable=True)


class Probe(Base):
    __tablename__ = "t_probe"
    probe_id = Column(
        "probe_id", Integer, primary_key=True, autoincrement=True, nullable=False
    )
    ocenka_numer = Column("Ocenka_numer", Integer, nullable=False, default=1)
    probe_type_id = Column(
        "probe_type_id",
        Integer,
        ForeignKey("t_probe_type.probe_type_id"),
        nullable=False,
    )
    probe_status_id = Column(
        "probe_status_id",
        Integer,
        ForeignKey("t_probe_status.id_probe_status"),
        nullable=False,
        default=0,
    )
    gost_id = Column("gost_id", Integer, nullable=False, default=0)
    type = Column("type", Integer, nullable=False, default=1)
    probe_parent_id = Column("probe_parent_id", Integer, nullable=False, default=0)
    count_probe = Column("count_probe", Integer, nullable=False, default=0)
    chield_probe_num_suffix = Column(
        "chield_probe_num_suffix", String(20), nullable=True
    )
    object_isl = Column("object_isl", String(1000), nullable=False, default="")
    top_journal_id = Column(
        "top_journal_id", Integer, ForeignKey("t_journal.journal_id"), nullable=False
    )
    id_nabor = Column(
        "id_nabor", Integer, ForeignKey("t_nabor.id_nabor"), nullable=True
    )
    FGIS_status = Column(
        "FGIS_status",
        Integer,
        ForeignKey("t_status_accreditation.status_accreditation_id"),
        nullable=False,
        default=1,
    )
    id_probe_status_group_synonym = Column(
        "id_probe_status_group_synonym",
        Integer,
        ForeignKey("t_status_group_synonym.id_probe_status_group_synonym"),
        nullable=False,
        default=0,
    )
    program_id = Column(
        "program_id", Integer, ForeignKey("t_program.program_id"), nullable=True
    )
    program_gost_id = Column(
        "program_gost_id", Integer, ForeignKey("t_gost.gost_id"), nullable=True
    )
    program_manual = Column("program_manual", Integer, nullable=True)
    uin = Column("uin", String(36), nullable=True)


class KtSFieldValueText(Base):
    __tablename__ = "kt_s_field_value_text"
    id_s_field_value = Column(
        "id_s_field_value",
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False,
    )
    uin_s_field = Column(
        "uin_s_field", String(36), ForeignKey("kt_s_field.uin_s_field"), nullable=False
    )
    id_s_num_opred = Column(
        "id_s_num_opred",
        Integer,
        ForeignKey("kt_s_num_opred.id_s_num_opred"),
        nullable=False,
        default=1,
    )
    value = Column("value", String(2048), nullable=False, default="")


class ProbeResult(Base):
    __tablename__ = "t_probe_result"
    probe_result_id = Column(
        "probe_result_id", Integer, primary_key=True, autoincrement=True, nullable=False
    )
    infelicity = Column("infelicity", String(50), nullable=True)
    probe_id = Column(
        "probe_id", Integer, ForeignKey("t_probe.probe_id"), nullable=False
    )
    pokazatel_id = Column("pokazatel_id", Integer, nullable=False)
    pokazatel_unite_id = Column("pokazatel_unite_id", Integer, nullable=False)
    value = Column("value", String(150), nullable=True)
    laborant_id = Column("laborant_id", Integer, nullable=False, default=0)
    order_id = Column("order_id", Integer, nullable=False)
    method_order_id = Column("method_order_id", Integer, nullable=False)
    pokazatel_use = Column("pokazatel_use", Boolean, nullable=False)
    input_type = Column("input_type", Boolean, nullable=True)
    exp_date = Column("exp_date", Date, nullable=True)
    abs_rasx = Column("abs_rasx", String(50), nullable=True)
    lim_repeat = Column("lim_repeat", String(50), nullable=True)
    uin_method_ver = Column(
        "uin_method_ver",
        String(36),
        ForeignKey("kt_method_ver.uin_method_ver"),
        nullable=False,
        default="0x30",
    )
    condition = Column("condition", String(255), nullable=True, default="")
    program_choice = Column("program_choice", Integer, nullable=True)
    report_enabled = Column("report_enabled", Boolean, nullable=False)


class KtResultField(Base):
    __tablename__ = "kt_result_field"
    uin_result_field = Column(
        "uin_result_field",
        String(36),
        ForeignKey("kt_field.uin_field"),
        primary_key=True,
        nullable=False,
    )
    uin_method_ver = Column(
        "uin_method_ver",
        String(36),
        ForeignKey("kt_method_ver.uin_method_ver"),
        nullable=False,
    )


class Pokazatel(Base):
    __tablename__ = "t_pokazatel"
    pokazatel_id = Column(
        "pokazatel_id", Integer, primary_key=True, autoincrement=True, nullable=False
    )
    pokazatel_method_id = Column(
        "pokazatel_method_id", Integer, nullable=False, default=0
    )
    pokazatel_name = Column("pokazatel_name", String(200), nullable=True)
    pokazatel_name_en = Column("pokazatel_name_en", String(200), nullable=True)
    pokazatel_unite_id = Column(
        "pokazatel_unite_id", Integer, ForeignKey("t_units.unite_id"), nullable=True
    )
    pokazatel_short = Column("pokazatel_short", String(50), nullable=True)
    pokazatel_group_id = Column(
        "pokazatel_group_id", Integer, nullable=False, default=0
    )
    pokazatel_report_name = Column(
        "pokazatel_report_name", String(250), nullable=False, default="-"
    )
    client_round = Column(
        "client_round", String(50), nullable=False, default="по нормативному документу "
    )
    uin_pokazatel = Column("uin_pokazatel", String(36), nullable=False, default="0x30")
    category_name = Column(
        "category_name", String(100), nullable=True, default="Категория 1"
    )
    pokazatel_reproduc = Column("pokazatel_reproduc", String(255), nullable=True)
    pokazatel_status = Column("pokazatel_status", Integer, nullable=False, default=1)
    change_date = Column("change_date", DateTime, nullable=False)
    change_user_id = Column(
        "change_user_id",
        Integer,
        ForeignKey("t_user.user_id"),
        nullable=False,
        default=1,
    )


class Method(Base):
    __tablename__ = "t_method"
    method_id = Column(
        "method_id", Integer, primary_key=True, autoincrement=True, nullable=False
    )
    method_name = Column("method_name", String(1000), nullable=True)
    method_gost_num = Column("method_gost_num", String(100), nullable=True)
    titr = Column("titr", Boolean, nullable=True)
    titr_id = Column("titr_id", Integer, nullable=True)
    method_uin = Column("method_uin", String(100), nullable=False)
    button_show = Column("button_show", Boolean, nullable=False)
    version = Column("version", SmallInteger, nullable=False)
    short_gost_num = Column("short_gost_num", String(100), nullable=False, default="")
    number_exp = Column("number_exp", Integer, nullable=True, default=2)
    uin_object_type = Column(
        "uin_object_type",
        String(100),
        ForeignKey("t_object_type.uin"),
        nullable=False,
        default="category_probe",
    )
    reproduc = Column("reproduc", String(255), nullable=True)
    method_status = Column("method_status", Boolean, nullable=False)
    change_date = Column("change_date", DateTime, nullable=False)
    change_user_id = Column(
        "change_user_id",
        Integer,
        ForeignKey("t_user.user_id"),
        nullable=False,
        default=1,
    )
    method_static = Column("method_static", Boolean, nullable=False)

class CrResultFieldPokazatel(Base):
    __tablename__ = "cr_result_field_pokazatel"
    uin_field_result = Column(
        "uin_field_result",
        String(36),
        ForeignKey("kt_result_field.uin_result_field"),
        primary_key=True,
        nullable=False,
    )
    uin_pokazatel = Column(
        "uin_pokazatel",
        String(36),
        ForeignKey("t_pokazatel.uin_pokazatel"),
        primary_key=True,
        nullable=False,
    )
    group_by_condition = Column(
        "group_by_condition", String(255), primary_key=True, nullable=False
    )
