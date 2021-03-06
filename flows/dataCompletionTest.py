
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

@task
def get_dbt_credentials(user_name: str, password: str):
    return {"user": user_name, "password": password,
            "start_date": "2022-01-02 00:00:00", "end_date": "2022-01-03 00:00:00"}

@task(trigger=all_finished)
def print_dbt_output(output):
    logger = prefect.context.get("logger")
    for line in output:
        logger.info(line)

@task(name="Clone DBT repo")
def pull_dbt_repo(repo_url: str, branch: str = None):
    pygit2.clone_repository(url=repo_url, path=DBT_PROJECT, checkout_branch=branch)

@task(name="Delete DBT folder if exists", trigger=all_finished)
def delete_dbt_folder_if_exists():
    shutil.rmtree(DBT_PROJECT, ignore_errors=True)


with Flow("dbtTest", run_config=LocalRun(labels=["myAgentLable"])) as flow:
    del_task = delete_dbt_folder_if_exists()
    dbt_repo = Parameter(
        "dbt_repo_url", default="https://github.com/klxsxian/testAction"
    )
    dbt_repo_branch = Parameter("dbt_repo_branch", default=None)
    # start_date = Parameter("start_date", default=None)
    # end_date = Parameter("end_date", default=None)
    pull_task = pull_dbt_repo(dbt_repo, dbt_repo_branch)
    del_task.set_downstream(pull_task)

    postgres_user = PrefectSecret("POSTGRES_USER")
    postgres_pass = PrefectSecret("POSTGRES_PASS")
    db_credentials = get_dbt_credentials(postgres_user, postgres_pass)
    dbtKwargs = db_credentials

    #dbt run --models dwd.dwd_payment_detail  --profiles-dir ci_profiles/ --vars '{start_date:"20220101", end_date:"20220102"}'

    # if start_date is not None:
    #     dbtKwargs["start_date"] = start_date
    #
    # if end_date is not None:
    #     dbtKwargs["end_date"] = end_date

    dbt_run = dbt(
        #command="dbt run", task_args={"name": "DBT Run"}, dbt_kwargs=db_credentials
        command="dbt run --models dwd.dwd_payment_detail",
        task_args={"name": "DBT Run"},
        dbt_kwargs=dbtKwargs
    )

    dbt_run_out = print_dbt_output(dbt_run)

    #say_hello()
