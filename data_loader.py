import pandas as pd


def load_data():

    subjects = pd.read_csv("data/subjects.csv")
    visits = pd.read_csv("data/visits.csv")
    queries = pd.read_csv("data/queries.csv")
    deviations = pd.read_csv("data/deviations.csv")
    lab_results = pd.read_csv("data/lab_results.csv")

    return subjects, visits, queries, deviations, lab_results
