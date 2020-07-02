
import pandas as pd
import numpy as np

# set working directory to directory where 'parameters.csv' file is stored

params = pd.read_csv("parameters.csv")
params.rename(columns={"Name":"ParamNames"},inplace=True)
#print(params.columns)
paramFrame = params[params["Type"]=="Model Parameter"][["ParamNames","Value","Type"]]

latentMean = paramFrame[paramFrame["ParamNames"]=="latent period"][["Value"]]
RecoveryMean = paramFrame[paramFrame["ParamNames"]=="infectious period"][["Value"]]
HospMean = paramFrame[paramFrame["ParamNames"]=="hosp period"][["Value"]]
DeathICUMean = paramFrame[paramFrame["ParamNames"]=="death period with ICU"][["Value"]]
DeathNoICUMean = paramFrame[paramFrame["ParamNames"]=="death period"][["Value"]]

randomParams_dict = {
  "R0": np.random.normal(4, 1, 1000),
  "LatentPeriod": np.random.normal(latentMean, 1, 1000),
  "RemovalPeriod": np.random.normal(RecoveryMean, 1, 1000),
  "HospPeriod": np.random.normal(HospMean, 1, 1000),
  "DeathICUPeriod": np.random.normal(DeathICUMean, 1, 1000),
  "DeathNoICUPeriod": np.random.normal(DeathNoICUMean, 1, 1000)
}

randomParams = pd.DataFrame(randomParams_dict)

randomParams[randomParams>0].dropna()

randomParams.to_csv("GeneratedParams.csv")
