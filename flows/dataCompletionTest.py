
import prefect
from prefect import task, Flow, Parameter
from prefect.tasks.dbt.dbt import DbtShellTask
from prefect.storage import GitHub
from prefect.triggers import all_finished
from prefect.run_configs import LocalRun
import pygit2
import shutil
from prefect.tasks.secrets import PrefectSecret

DBT_PROJECT = "testAction"
STORAGE = GitHub(
    repo="klxsxian/testAction",
    path=f"flows/dbtTest.py",
    access_token_secret="GITHUB_ACCESS_TOKEN",
)

@task
def say_hello():
    logger = prefect.context.get("logger")
    logger.info("Hello, Cloud!")

dbt = DbtShellTask(
    return_all=True,
    profile_name="profiles",
    profiles_dir="ci_profiles/",
    environment="dev",
    overwrite_profiles=True,
    log_stdout=True,
    helper_script=f"cd {DBT_PROJECT} && dbt deps",
    log_stderr=True,
    dbt_kwargs={
        "type": "postgres",
        "host": "124.221.124.73",
        "port": 15432,
        "dbname": "postgres",
        "schema": "schema_dbt",
        "threads": 4,
        "client_session_keep_alive": False,
    },
)

logger = prefect.context.get("logger")

@task
def get_dbt_credentials(user_name: str, password: str):
    return {"user": user_name, "password": password}

@task(trigger=all_finished)
def print_dbt_output(output):
    for line in output:
        logger.info(line)

@task(name="Clone DBT repo")
def pull_dbt_repo(repo_url: str, branch: str = None):
    pygit2.clone_repository(url=repo_url, path=DBT_PROJECT, checkout_branch=branch)

@task(name="Delete DBT folder if exists", trigger=all_finished)
def delete_dbt_folder_if_exists():
    shutil.rmtree(DBT_PROJECT, ignore_errors=True)


@task
def get_env():
    start_date = Parameter(name="start_date", required=False)
    end_date = Parameter(name="end_date", required=False)
    return {"start_date": start_date, "end_date": end_date}

with Flow("dataCompletionTest", run_config=LocalRun(labels=["myAgentLable"])) as flow:
    del_task = delete_dbt_folder_if_exists()
    dbt_repo = Parameter("dbt_repo_url", default="https://github.com/klxsxian/testAction")
    dbt_repo_branch = Parameter("dbt_repo_branch", default=None)

    pull_task = pull_dbt_repo(dbt_repo, dbt_repo_branch)
    del_task.set_downstream(pull_task)

    postgres_user = PrefectSecret("POSTGRES_USER")
    postgres_pass = PrefectSecret("POSTGRES_PASS")
    db_credentials = get_dbt_credentials(postgres_user, postgres_pass)

    # dbt run --models dwd.dwd_payment_detail  --profiles-dir ci_profiles/ --vars '{start_date:"20220101", end_date:"20220102"}'
    # env = {"start_date": "2022-01-02 00:00:00", "end_date": "2022-01-03 00:00:00"}
    #env = get_env("2022-01-02 00:00:00", "2022-01-03 00:00:00")

    environment_variables = get_env()
    #logger.info(environment_variables)

    dbt_run = dbt(
        command='dbt run --models dwd.dwd_payment_detail --vars '+environment_variables.__str__(),
        task_args={"name": "DBT Run"},
        dbt_kwargs=db_credentials
    )


    dbt_run_out = print_dbt_output(dbt_run)
    #say_hello()
