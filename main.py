
from autopipes import data_factory


run_id = data_factory.pipeline_create_run("test", "DataPlatfromRhone-ADF")

print(run_id)




# path = os.path.join(ROOT_DIR, "Databricks/Workflows/")

# Job.job_import_jobs(path)

# from autopipes import Workspace

# from_path = "./project_patterns"
# to_path = "/project_patterns"

# Workspace.workspace_import_dir(
#     from_path=from_path,
#     to_path=to_path,
#     # sub_dirs=["databricks","pipelines"]
# )