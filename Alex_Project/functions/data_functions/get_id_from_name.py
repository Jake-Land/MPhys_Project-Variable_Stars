from astroquery.simbad import Simbad

def get_gaia_dr3_id(object_name):
    Simbad.add_votable_fields('ids')

    result = Simbad.query_object(object_name)

    ids = result['ids'][0].split('|')
    gaia_dr3_id = next((i.replace('Gaia DR3 ', '').strip() for i in ids if 'Gaia DR3' in i), None)

    return gaia_dr3_id