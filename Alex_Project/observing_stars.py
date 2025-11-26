#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from astropy.modeling import models, fitting
from astropy.modeling.models import custom_model
from astropy.modeling import Fittable1DModel, Parameter
from astropy.time import Time
from astroquery.simbad import Simbad
import juliandate as jd
from datetime import datetime, timedelta
import pandas as pd
from astroquery.gaia import Gaia


# We have N stars each with period p_(n), p_(n+1), etc... We need to maximise phase coverage for our observations, i.e. no observing that star at the same phase more than once.
# 
# How to do this: For a specific star, n, calculate time difference between previous observations and the time for the current observation, del_t = t_0 - t_i. Divide these times by the period, phase_t = del_t/p. Discard all phase_t except for the one closest to a whole integer. If phase_t is an integer then we are observing at a phase already observed. For all N stars find the phase_t furthest from an integer (closest to 0.5, 1.5, ...) and observe it. Repeat untill we have measurements for the entire phase for all N stars.

# Code:
# 
# current_time = getDate
# star_greatest_offset = 0
# target_star = []
# 
# for star in starsCatalog:
#     greatest_offset = 0
#     for observation in star["observations"]:
#         phase_t = []
#         offset = (current_time - observation["date"] / star["period"]) % 1
#         if offset >= 0.5:
#             offset = 1 - offset
#         if offset > greatest_offset:
#             greatest_offset = offset
#     if greatest_offset > star_greatest_offset:
#         target_star = star
# 
# //observe target_star
# 

# In[2]:


ts = pd.Timestamp(datetime.now())
current_time = ts.to_julian_date()
#print(ts)
#print(current_time)


# In[3]:


# Create star catalogue
#target_stars = ('RV UMa', 'RZ Cep', 'RR Lyr')

#for star in target_stars:
#query = f"""
#SELECT basic.main_id, vartyp AS type, ROUND(AVG(period), 6) AS period
#FROM basic
#JOIN mesVar ON basic.oid = mesVar.oidref
#WHERE basic.otype = 'RR*'
#AND main_id IN {target_stars}
#GROUP BY basic.main_id, vartyp
#HAVING vartyp = 'RRAB' OR vartyp = 'RRC'
#"""
#result = Simbad.query_tap(query)
#print(result)
#stars_df = result.to_pandas()
#stars_df.main_id = [ star.replace('V*', '').strip() for star in stars_df.main_id]
#stars_df


# In[4]:


RV_UMa = {
    "name": "RV UMa",
    "id": "1561928427003019520"
}

RZ_Cep = {
    "name": "RZ Cep",
    "id": "2211629018927324288"
}

RR_Lyr = {
    "name": "RR Lyr",
    "id": "2125982599343482624"
}

target_stars = (RV_UMa['id'], RZ_Cep['id'], RR_Lyr['id'])
target_stars


# In[5]:


query = f"""
        SELECT  rr.source_id, rr.pf, rr.p1_o , rr.best_classification
        FROM gaiadr3.vari_rrlyrae AS rr
        WHERE source_id IN (1561928427003019520, 2211629018927324288, 2125982599343482624)
        """
job = Gaia.launch_job_async(query)
results = job.get_results()

results_df = results.to_pandas()
cols = ['pf', 'p1_o']
results_df = results_df.assign(period=results_df[cols].sum(1)).drop(cols, axis=1)
results_df.rename(columns={'source_id' : 'main_id', 'best_classification' : 'type'}, inplace=True)
stars_df = results_df
stars_df['main_id'] = stars_df['main_id'].astype(str)


# In[6]:


#Create dummy observation times

dummy_time = pd.Timestamp('2025-09-23 21:09:02.442422')
dummy_obs = []
for i in range(15):
    dummy_julian_time = dummy_time.to_julian_date()
    dummy_time = dummy_time + timedelta(minutes = 10)

    dummy_obs.append((dummy_julian_time, target_stars[i % 3]))


observations_df = pd.DataFrame(dummy_obs, columns=["obs_times", "main_id"])
#observations_df


# In[7]:


catalogue_df = pd.merge(observations_df, stars_df)
#catalogue_df


# In[8]:


def find_next_target_star(star_catalogue, time):
    star_greatest_offset = 0 # Greatest offest for each of the target stars
    target_star = ""
    for star in star_catalogue["main_id"].unique():
        star_data = star_catalogue[star_catalogue["main_id"] == star]
        obs_times = star_data["obs_times"]
        period = star_data["period"]
        phase = ((time - obs_times) / period) % 1
        smallest_offset = 0.5
        offset = [1 - x if x >= 0.5 else x for x in phase]
        star_offset = min(offset) 
        #print(star, star_offset)
        if star_offset > star_greatest_offset:
            star_greatest_offset = star_offset
            target_star = star
    return(target_star)


# In[9]:


def find_phase_offset(star_data, time):
    obs_times = star_data["obs_times"]
    period = star_data["period"]
    phase = ((time - obs_times) / period) % 1
    smallest_offset = 0.5
    offset = [1 - x if x >= 0.5 else x for x in phase]
    star_offset = min(offset) 
    print(phase)
    return(star_offset)


# In[10]:


RV_UMa_data = catalogue_df[catalogue_df["main_id"] == "1561928427003019520"]
RZ_Cep_data = catalogue_df[catalogue_df["main_id"] == "2211629018927324288"]


# In[11]:


find_phase_offset(RZ_Cep_data, current_time)


# In[12]:


find_next_target_star(catalogue_df, current_time)


# Next: For any time, t in observation period t_start to t_end, find the priority star.
# instead of current_time, use t_start then increase time by n minutes untill t = t_end.
# At each t find the star that should be observed then add that observation to a new df.
# Run the func again with new obs_times included.(?) 

# In[13]:


def observation_plan(start_time, end_time, time_step, star_catalogue):
    dummy_obs_df = star_catalogue.copy()
    time_at_obs = start_time
    t_step_days = time_step / 1440 # Convert minutes to days
    observation_plan = []
    while time_at_obs < end_time:
        target_star = find_next_target_star(dummy_obs_df, time_at_obs)

        new_row = pd.DataFrame({
            "obs_times": time_at_obs,
            "main_id": target_star,
            "type": [stars_df[stars_df['main_id'] == f'{target_star}']["type"].iloc[0]],
            "period": [stars_df[stars_df['main_id'] == f'{target_star}']["period"].iloc[0]]
        })
        dummy_obs_df = pd.concat([dummy_obs_df, new_row], ignore_index=True)
        time_at_obs += t_step_days

        observation_plan.append((target_star, Time(time_at_obs, format='jd').to_datetime()))
    return observation_plan


# In[14]:


t_start = pd.Timestamp("2025-10-09T14:00:00").to_julian_date()
t_end = pd.Timestamp("2025-10-09T18:00:00").to_julian_date()
t_step = 10 # minutes

observation_plan(t_start, t_end, t_step, catalogue_df)

