from pipeline.training_pipeline import training_pipeline

"""

Data:

https://github.com/Vortander/KinectGait/blob/master/GenderBMIData/person-data.csv

"""
url = ""
mode = "raw"
if __name__ == "__main__":
    training_pipeline(url, mode)
