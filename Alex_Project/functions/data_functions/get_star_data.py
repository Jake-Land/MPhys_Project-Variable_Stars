import pandas as pd


BPO = [51.372840, -2.319224, 200, 30, 12]

RRL_candidates = pd.read_csv("data/vari_rrlyrae.csv")


def get_star_data(star_candidate):
    star_data = RRL_candidates[RRL_candidates["main_id"] == star_candidate]

    return star_data
