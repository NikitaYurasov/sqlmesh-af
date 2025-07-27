import logging
import typing as tp

from airflow.models.baseoperator import BaseOperator

if tp.TYPE_CHECKING:
    from sqlmesh import Config
    from sqlmesh.core.model import Model

    from sqlmesh_af.config import SQLMeshAFConfig


class SQLMeshRunOperator(BaseOperator):
    def __init__(
        self,
        model: 'Model',
        sqlmesh_env: str,
        config: 'SQLMeshAFConfig',
        project_config: 'Config',
        **kwargs,
    ):
        self.sqlmesh_model = model
        self.sqlmesh_env = sqlmesh_env
        self.project_config = project_config
        self.config = config

        super().__init__(
            task_id=model.fqn.replace('"', '').replace('.', '__'),
            retries=3,
            retry_delay=60,
            max_active_tis_per_dag=1,
            **kwargs,
        )

    def execute(self, context):
        from sqlmesh import Context



        if self.config.dry_run:
            logging.info(f'Dry run for {self.sqlmesh_model.name}')
            return

        sqlmesh_context = Context(
            config=self.project_config,
            paths=[self.config.project_path],
        )
        sqlmesh_context.run(
            environment=self.sqlmesh_env,
            skip_janitor=True,
            select_models=[self.sqlmesh_model.fqn],
            no_auto_upstream=True,
        )
