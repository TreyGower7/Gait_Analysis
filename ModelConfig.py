from pydantic import BaseModel

class ConfigArch(BaseModel):
    """
    A class for configuring which model to implement for training.
    """
    # Default model
    model: str = "Transformer"