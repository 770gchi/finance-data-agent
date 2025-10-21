from importlib.resources import files

def load_text(package_path: str) -> str:
    """
    e.g. load_text("finance_data_agent.prompts/qlib_prompts.yaml")
    """
    pkg, rel = package_path.split("/", 1)
    return files(pkg).joinpath(rel).read_text(encoding="utf-8")