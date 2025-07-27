from pathlib import Path

from sqlmesh_af import SQLMeshDAG
from sqlmesh_af.config import GatewayOverride, SQLMeshAFConfig

config = SQLMeshAFConfig(
    project_path=Path('/opt/airflow/dags/sqlmesh_project'),
    gateway_overrides=[
        GatewayOverride(
            name='local',
            database='/opt/airflow/dags/sqlmesh_project/db/sushi-example.db',
        )
    ],
    env='prod',
    dry_run=False,
)


sqlmesh_dag = SQLMeshDAG(
    dag_id_prefix='sqlmesh_run',
    schedule='@hourly',
    config=config,
)
