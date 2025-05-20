from pipeline.training_pipeline import training_pipeline

"""

Data:

https://github.com/Vortander/KinectGait/blob/master/GenderBMIData/person-data.csv

"""
if __name__ == "__main__":
    base_url = "https://github.com/Vortander/KinectGait/tree/master/Data"
    metadata_url = "https://raw.githubusercontent.com/Vortander/KinectGait/master/GenderBMIData/person-data.csv?raw=true"


    training_pipeline(base_path=base_url, metadata_path=metadata_url)
