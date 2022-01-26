from enum import Enum
from pathlib import Path
from typing import Any, Dict, Literal, Optional, Union

from pydantic import AnyUrl, BaseModel, Field, conint, stricturl

# enums


class LogLevel(str, Enum):
    trace = "trace"
    debug = "debug"
    info = "info"
    warning = "warning"
    error = "error"
    critical = "critical"


class MechanismType(str, Enum):
    ansible = "ansible"


class PlaybookType(str, Enum):
    provision = "provision"
    deprovision = "deprovision"


# Pydantic models


class CeleryConfigModel(BaseModel):
    broker_url: AnyUrl
    result_backend: AnyUrl


class SQLAlchemyModel(BaseModel):
    sync_url: stricturl(tld_required=False, host_required=False)
    async_url: stricturl(tld_required=False, host_required=False)


class DatabaseConfigModel(BaseModel):
    sqlalchemy: SQLAlchemyModel


class AnsibleMechanismModel(BaseModel):
    topdir: Optional[Path]
    extra_vars: Optional[Dict[str, Any]] = Field(alias="extra-vars")
    playbooks: Optional[Dict[PlaybookType, Path]]


class MechanismModel(BaseModel):
    type_: Optional[MechanismType] = Field(alias="type")
    ansible: Optional[AnsibleMechanismModel]


class NodePoolsModel(BaseModel):
    extends: Optional[str]
    mechanism: Optional[MechanismModel]
    fill_level: Optional[conint(gt=0)] = Field(alias="fill-level")
    reuse_nodes: Optional[Union[Dict[str, Union[int, str]], Literal[False]]] = Field(
        alias="reuse-nodes"
    )

    class Config:
        extra = "allow"


class NodePoolsRootModel(BaseModel):
    abstract: Optional[Dict[str, NodePoolsModel]]
    concrete: Dict[str, NodePoolsModel]


class LoggingModel(BaseModel):
    version: Literal[1]

    class Config:
        extra = "allow"


class AppModel(BaseModel):
    loglevel: Optional[LogLevel]
    host: Optional[str]
    port: Optional[conint(gt=0, lt=65536)]
    logging: Optional[LoggingModel]


class LegacyModel(BaseModel):
    host: Optional[str]
    port: Optional[conint(gt=0, lt=65536)]
    dest: Optional[str]
    loglevel: Optional[LogLevel]
    logging: Optional[LoggingModel]
    usermap: Dict[str, str]


class ConfigModel(BaseModel):
    app: Optional[AppModel]
    celery: Optional[CeleryConfigModel]
    database: Optional[DatabaseConfigModel]
    metaclient: Optional[LegacyModel]
    nodepools: Optional[NodePoolsRootModel]