import pandas as pd
from astroquery.gaia import Gaia 

# Jakes Code
def Get_GAIA_RRL(site, query=False):

    """
    Function that searches the gaia DR3 database for RRL stars that are visible from the observation site,
    based on location and limiting apparent magnitude. Then saves the found results to a csv file
    OR the csv file is just read in if the search isn't required
    Returns the list of potential observations candidates with their id, ra/dec coords, their periods, 
    mags in gaia filters and best classification of the RRL star
    """

    # First checks whether the gaia DR3 needs to be used
    if query:
        # Min and max declaration visible from the observation site,
        # helps to reduce the star retrieved from the database
        dec_min = site[0] - (90 - site[3])
        dec_max = site[0] + (90 - site[3])
        dec_max = min(dec_max, 90.0)

        # The ADQL that is used to query the GDR3 database and get the stars we want
        ADQL = f"""
                SELECT  rr.source_id, gs.ra, gs.dec, gs.phot_g_mean_mag, gs.phot_bp_mean_mag, gs.phot_rp_mean_mag, rr.pf, rr.p1_o, rr.best_classification
                FROM gaiadr3.vari_rrlyrae AS rr
                JOIN gaiadr3.gaia_source AS gs
                ON rr.source_id = gs.source_id
                WHERE gs.dec BETWEEN {dec_min:} AND {dec_max:}
                AND gs.phot_bp_mean_mag <= {site[4]}
                """
    
        job = Gaia.launch_job_async(ADQL)      # Searching Gaia
        results = job.get_results()            # Getting the result

        results_df = results.to_pandas()
        cols = ['pf', 'p1_o']
        results_df = results_df.assign(period=results_df[cols].sum(1)).drop(cols, axis=1)
        results_df.rename(columns={'source_id' : 'main_id'}, inplace=True)

        results_df.to_csv("data/vari_rrlyrae.csv", index=False)      # Saveing the results so it doesn't have to redo this

    
    RRL = pd.read_csv("data/vari_rrlyrae.csv")                                # If the search is not done then just read the csv file 
            
    return RRL