import numpy as np

import functions.score_functions as score


def calculate_total_score(phase_offset, gradient, airmass, ra, dec, observation_time):
    seeing_score_star = score.seeing(airmass, 1, 3)
    sky_brightness_score_star = score.sky_brightness(20.5, 20.5)
    sky_trans_score_star = score.sky_trans(0.7, 0.7)
    hour_angle_score_star = score.hour_angle(0, 1.5, -0.5)
    priority_score_star = score.priority(1, 1)
    overheads_score_star = score.overheads(0)
    phase_offset_score_star = score.phase_offset(phase_offset)
    gradient_score_star = score.gradient(gradient)

    moon_distance_score_star = score.moon_distance(ra, dec, observation_time)
    elevation_score_star = score.elevation(ra, dec, observation_time)

    functions_star = np.array([
        [seeing_score_star, 1],
        [sky_brightness_score_star, 1],
        [sky_trans_score_star, 1],
        [hour_angle_score_star, 1],
        [priority_score_star, 1],
        [overheads_score_star, 1],
        [phase_offset_score_star, 1],
        [moon_distance_score_star, 1],
        [elevation_score_star, 1],
        [gradient_score_star, 1]
    ])

    final_score = score.total(functions_star)
    return final_score