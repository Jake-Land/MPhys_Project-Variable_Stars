from astroquery.gaia import Gaia
from get_id_from_name import get_gaia_dr3_id

def get_epoch_photometry(star_name):
    star_id = get_gaia_dr3_id(star_name)
    print(star_id)
    retrieval_type = 'EPOCH_PHOTOMETRY'
    data_structure = 'INDIVIDUAL'
    data_release = 'Gaia DR3'
    datalink = Gaia.load_data(ids=star_id, data_release = data_release, retrieval_type=retrieval_type, data_structure = data_structure, verbose = False)
    dl_keys = [inp for inp in datalink.keys()] # Getting Epoch photometry keys
    dl_keys.sort()
    dl_key = dl_keys[0]
    # Creating a readable table
    epoch_photometry_data = datalink[dl_key][0].to_table()
    epoch_photometry_data.write(f"data/{star_name}_epoch_photometry.csv", format="csv", overwrite=True)
    return epoch_photometry_data

get_epoch_photometry('RU Psc')
