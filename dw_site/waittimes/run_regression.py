import waittimes.regression as regression
import pickle

MEDIAN_AVGWAIT = 42
ARG = ["less than 10 mins", "11-24 mins", "25-53 mins", "beyond 54 mins"]

def find_model():
    '''
    Load our dataset into pandas dataframe and load the ols model we saved
    '''
    df = regression.clean_data("waittimes/nhamcs_all_data.csv")
    x = regression.user_time(df)
    
    # load the model from disk
    model = pickle.load(open("waittimes/finalized_model.sav", 'rb'))
    return model, x


def run_regression(user_pain, hosp_qs, model, x):
    '''
    Getting the real time, painscale and average wait time of the nearest
    five hospitals into our pandas dataframe to run the regression
    '''
    x["PAINSCALE"] = user_pain
    for i in range(len(hosp_qs)):
        # if the hospital doesnt have a average waittime using natioanl median instead
        if hosp_qs[i].score == -1:
            x.loc[i, "AVGWAIT"] = MEDIAN_AVGWAIT
        x.loc[i, "AVGWAIT"] = hosp_qs[i].score
        if hosp_qs[i].msa == "Metropolitan Statistical Area":
            x.loc[i, "MSA"] = 1
    
    x = x[:len(hosp_qs)]
    if len(hosp_qs) == 1:
        x = x.reshape(1, -1)             
    predictions = model.predict(x)
    for i, pred in enumerate(predictions):
        hosp_qs[i].predicted_wait = ARG[pred-1]
    
    return hosp_qs
