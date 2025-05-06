import logging
from zenml import step

class SetupDirs:
    def __init__(self, config: DataPathConfig):
        self.config = config

    def create_dirs(self):
        """
        Create directories if they do not exist.
        """
        for dir_path in self.config.dirs:
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"Ensured directory exists: {dir_path}")

@step
def setup_dirs_step(config: DataPathConfig) -> None:
    """
    ZenML step to create required project directories.
    """
    try:
        setup = SetupDirs(config)
        setup.create_dirs()
        logging.info("✅ Directories set up successfully.")
    except Exception as e:
        logging.error(f"Error during directory setup: {e}")
        raise
