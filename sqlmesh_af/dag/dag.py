import typing as tp

from airflow import DAG
from sqlmesh import Context
from sqlmesh.utils.date import to_datetime

from sqlmesh_af.operator.sqlmesh_run import SQLMeshRunOperator
from sqlmesh_af.utils.sqlmesh_ import get_sqlmesh_config, update_sqlmesh_config

if tp.TYPE_CHECKING:
    from sqlmesh import Config

    from sqlmesh_af.config import SQLMeshAFConfig


class SQLMeshDAG(DAG):
    def __init__(
        self,
        config: 'SQLMeshAFConfig',
        schedule: str,
        dag_id_prefix: str = 'sqlmesh_run',
        run_env: dict[str, str] | None = None,
        sqlmesh_cli_path: str = 'sqlmesh',
        **kwargs,
    ):
        self.config = config
        self.project_config: 'Config' = update_sqlmesh_config(get_sqlmesh_config(config.project_path), self.config)

        super().__init__(
            # dag_id has pattern {dag_id_prefix}[_{project_name}]_{env}
            dag_id='_'.join([v for v in (dag_id_prefix, self.project_config.project or '', config.env) if v]),
            schedule=schedule,
            catchup=not config.dry_run,
            start_date=to_datetime(self.project_config.model_defaults.start or '1 day ago'),
            max_active_runs=self.config.max_active_runs,
            **kwargs,
        )

        self.af_run_env = run_env
        self.sqlmesh_cli_path = sqlmesh_cli_path

        self._build_sqlmesh_dag()

    def _build_sqlmesh_dag(self):
        context = Context(
            config=self.project_config,
            paths=[self.config.project_path],
        )
        sqlmesh_dag = context.dag

        model_mapping = {}
        af_tasks_mapping: dict[str, SQLMeshRunOperator] = {}

        for model_safe_name in sqlmesh_dag.sorted:
            sqlmesh_model = context.models[model_safe_name]
            if sqlmesh_model.kind.is_external:
                continue
            model_mapping[model_safe_name] = sqlmesh_model
            af_task = SQLMeshRunOperator(
                model=sqlmesh_model,
                sqlmesh_env=self.config.env,
                config=self.config,
                project_config=self.project_config,
            )
            self.add_task(af_task)
            af_tasks_mapping[model_safe_name] = af_task

        for model_safe_name, model_deps in sqlmesh_dag.graph.items():
            for dep_safe_name in model_deps:
                dep_sqlmesh_model = context.models[dep_safe_name]
                if dep_sqlmesh_model.kind.is_external:
                    continue
                af_task = af_tasks_mapping[model_safe_name]
                af_task.set_upstream(af_tasks_mapping[dep_safe_name])
