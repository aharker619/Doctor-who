import waittimes.regression as regression

MEDIAN_AVGWAIT = 42

def find_model():
    df = regression.clean_data("waittimes/nhamcs_all_data.csv")
    model = regression.rf(df)
    return model, df


def run_regression(user_pain, hosp_qs, model, df):
    x = regression.user_time(df)
    x["PAINSCALE"] = user_pain
    for i in range(len(hosp_qs)):
        if hosp_qs[i].score == -1:
            x.loc[i, "AVGWAIT"] = MEDIAN_AVGWAIT
        x.loc[i, "AVGWAIT"] = hosp_qs[i].score
        if hosp_qs[i].msa == "Metropolitan Statistical Area":
            x.loc[i, "MSA"] = 1
        x = x[:len(hosp_qs)]

    predictions = model.predict(x)
    for i, pred in enumerate(predictions):
        hosp_qs[i].predicted_wait = pred
    
    return hosp_qs