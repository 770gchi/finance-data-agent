from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict

class FactorSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FACTOR_COSTEER_")

    # Data & execution
    data_folder: str = "git_ignore_folder/factor_implementation_source_data"
    data_folder_debug: str = "git_ignore_folder/factor_implementation_source_data_debug"
    python_bin: str = "python"
    file_based_execution_timeout: int = 3600
    select_method: str = "random"

    # Qlib
    qlib_provider_uri: str = "~/.qlib/qlib_data/cn_data"
    qlib_market: str = "csi300"
    qlib_benchmark: str = "SH000300"

    # Logging / session
    log_dir: str = ".fda_logs"
    enable_cache: Optional[bool] = None
    