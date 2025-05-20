from zenml import pipeline
import logging
#from steps.setup_dirs import setup_dirs_step
from steps.ingest_data import ingest_data
from steps.model_train import train_model
from steps.model_evaluate import evaluate_model
from ModelConfig import ModelArch

@pipeline(enable_cache=False)
def training_pipeline(base_path: str, metadata_path: str = None, ModelConfig=ModelArch):
    """
    Training pipeline to train a model.
    
    Args:
        config (DataPathConfig): Config object for directory paths.
        model_config (str): Optional model name.
    """
    # Setup directories (WIP)
    # setup_dirs_step(config=config)

    # Ingest data from each person
   
    df = ingest_data(
        data_path=base_path,
        meta_data=metadata_path
    )    
    # Train model
    model = train_model(data=df, model_name=ModelConfig)

    # Evaluate model
    evaluate_model(model=model, data=df)
