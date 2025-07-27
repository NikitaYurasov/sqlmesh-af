from pathlib import Path

from pydantic import BaseModel, Field

from sqlmesh_af.config.gateway_conf import GatewayOverride


class SQLMeshAFConfig(BaseModel):
    project_path: Path
    gateway_overrides: list[GatewayOverride] = Field(default_factory=list)
    env: str = 'prod'
    dry_run: bool = False
    max_active_runs: int = 50

    @property
    def config_path(self) -> Path:
        if (self.project_path / 'config.yaml').exists():
            return self.project_path / 'config.yaml'
        elif (self.project_path / 'config.yml').exists():
            return self.project_path / 'config.yml'
        else:
            raise ValueError(f'Config file not found in {self.project_path}')
