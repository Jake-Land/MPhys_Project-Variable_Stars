from astroplan import Observer, FixedTarget
from astropy.coordinates import EarthLocation, SkyCoord, get_body
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import SkyCoord
import numpy as np

BPO = [51.372840, -2.319224, 200, 30, 12]


location = EarthLocation(lat=BPO[0]*u.deg, lon=BPO[1]*u.deg, height=BPO[2]*u.m)  # BPO
observer = Observer(location=location, name="BPO", timezone="UTC")

def elevation(ra, dec, observation_time, min_elevation=30):
    target = FixedTarget(coord=SkyCoord(ra=ra*u.deg, dec=dec*u.deg))

    t = Time(observation_time, format='jd')  # UTC time

    altaz = observer.altaz(t, target)
    altitude = altaz.alt

    if altitude < min_elevation * u.deg:
        return 0  # Target is below minimum elevation
    else:
        return 1  # Target is above minimum elevation

def gradient(gradient):
    score = ((1 + np.exp(-0.5 * abs(gradient)))**-1) - 1
    return score

def hour_angle(HA_t, HA_max, HA_min):
    if HA_t < HA_min and HA_t > HA_max:
        return 0
    HA_H = 0
    if HA_min <= 0 and HA_max >= 0:
        HA_H = 0
    elif HA_min < 0 and HA_max < 0:
        HA_H = HA_max
    elif HA_min > 0 and HA_max > 0:
        HA_H = HA_min
    HA_range = np.absolute(HA_max - HA_min)
    HA_dist = np.absolute(HA_t - HA_H)
    hour_angle_score = 1 / ((HA_range + 1) * (HA_dist + 1))
    return hour_angle_score

def moon_distance(ra, dec, observation_time, min_separation=30):
    target = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')

    t = Time(observation_time, format='jd')  # UTC time

    moon = get_body('moon', t, location).transform_to('icrs')

    separation = target.separation(moon)

    if separation < min_separation * u.deg:
        return 0  # Target is too close to the Moon
    else:
        return 1  # Target is sufficiently far from the Moon

def overheads(overheads):
    overheads_score = 1 - (0.9 * overheads)
    return overheads_score

def phase_offset(phase_offset):
    phase_offset_score = np.round(np.square(np.sin(np.pi * phase_offset)), 10)
    return phase_offset_score

def priority(science_priority, override_priority):
    priority_score = science_priority * override_priority
    return priority_score

def seeing(airmass, seeing_zenith, maximum_seeing, seeing_max=3, seeing_min=0.3):
    seeing = airmass**0.6 * seeing_zenith
    if seeing > maximum_seeing:
        return 0
    if seeing <= maximum_seeing:
        seeing_score  = (seeing_max - maximum_seeing + seeing_min) / ((maximum_seeing - seeing_min + 1) * (seeing_max - maximum_seeing + seeing))
        return seeing_score
    return 0

def sky_brightness(sky_brightness, brightest_sky, sb_min=22):
    if sky_brightness >= brightest_sky:
        sky_brightness_score = (brightest_sky + 1) / ((sb_min - brightest_sky + 1) * (sb_min - sky_brightness + brightest_sky + 1))
        return sky_brightness_score
    return 0

def sky_trans(sky_trans, min_sky_trans, sky_trans_max=0.88):
    if sky_trans >= min_sky_trans:
        sky_trans_score = (min_sky_trans + 1) / ((sky_trans_max - min_sky_trans + 1) * (sky_trans_max - sky_trans + min_sky_trans + 1))
        return sky_trans_score
    if sky_trans < min_sky_trans:
        return 0
    return 0

def total(scoring_functions):
    total_score = 0
    for function, weight in scoring_functions:
        if function == 0:
            total_score = 0
            return total_score
        total_score += weight * function
    return total_score