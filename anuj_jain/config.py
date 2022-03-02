import os
from pathlib import Path


base_dir = Path(__file__).resolve().parent
project_name = base_dir.name
config_name = os.environ.get("CONFIG_TYPE", "staging")


class Config():
    def __init__(self, env):
        valid_envs = ["staging", "prod"]
        if env not in valid_envs:
            raise ValueError(f"Please choose a workspace from {valid_envs}")

        super().__init__()

        self.BASE_DIR = base_dir
        self.MIGRATION_DIR=f'migrations-{env}'
        self.RESTX_ERROR_404_HELP = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SQLALCHEMY_DATABASE_URI = f'mysql://root:root@127.0.0.1:3306/insurance_{env}'




config = Config(config_name)