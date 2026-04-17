import unittest

from geotools.geo import distance_wgs84_geodesic


class TestGeoTools(unittest.TestCase):
    def test_distance_wgs84_geodesic(self):
        lat1 = 52.52042741543588
        lon1 = 13.405782162596813
        lat2 = 52.52074696727995
        lon2 = 13.406442521399553

        distance = distance_wgs84_geodesic(lat1, lon1, lat2, lon2)

        self.assertAlmostEqual(distance, 57.22, places=2)


if __name__ == "__main__":
    unittest.main()
