import pandas as pd


def remove_outliers(epoch_photometry: pd.DataFrame) -> pd.DataFrame:
    epoch_photometry = epoch_photometry.loc[~epoch_photometry.variability_flag_g_reject, :]
    epoch_photometry = epoch_photometry.loc[~epoch_photometry.variability_flag_bp_reject, :]
    epoch_photometry = epoch_photometry.loc[~epoch_photometry.variability_flag_rp_reject, :]
    epoch_photometry = epoch_photometry.loc[~epoch_photometry.rejected_by_photometry, :]
    return epoch_photometry