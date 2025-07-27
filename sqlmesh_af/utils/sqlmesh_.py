import typing as tp
from pathlib import Path

from sqlmesh import Config
from sqlmesh.core.config.loader import load_configs

if tp.TYPE_CHECKING:
    from sqlmesh_af.config import SQLMeshAFConfig


def get_sqlmesh_config(project_path: Path) -> Config:
    if not project_path.is_dir():
        raise ValueError(f'Project path {project_path} is not a directory')

    return list(load_configs(config=None, config_type=Config, paths=[project_path]).values())[0]


def update_sqlmesh_config(sqlmesh_config: Config, config: 'SQLMeshAFConfig'):
    if not config.gateway_overrides:
        return
    for gateway_override in config.gateway_overrides:
        gateway_name = gateway_override.name
        for field_name in gateway_override.model_fields_set:
            if field_name == 'name':
                continue
            if gateway_name not in sqlmesh_config.gateways:
                continue
            setattr(sqlmesh_config.gateways[gateway_name].connection, field_name, getattr(gateway_override, field_name))
    print(f'Gateway overrides: {sqlmesh_config.gateways}')
