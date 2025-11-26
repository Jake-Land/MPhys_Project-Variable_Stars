from astroplan import Observer, FixedTarget
from astroplan import AltitudeConstraint, AirmassConstraint
from astropy.coordinates import EarthLocation
from astropy.time import Time
import astropy.units as u
from astropy.coordinates import SkyCoord

BPO = [51.372840, -2.319224, 200, 30, 12]


location = EarthLocation(lat=BPO[0]*u.deg, lon=BPO[1]*u.deg, height=BPO[2]*u.m)  # BPO
observer = Observer(location=location, name="BPO", timezone="UTC")

def find_airmass(ra, dec, observation_time):
    target = FixedTarget(coord=SkyCoord(ra=ra*u.deg, dec=dec*u.deg))

    t = Time(observation_time, format='jd')  # UTC time

    altaz = observer.altaz(t, target)
    airmass = altaz.secz  # sec(z) = airmass

    return airmass.value