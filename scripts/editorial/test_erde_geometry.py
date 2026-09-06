"""Numerical checks for native positioning and area preservation, independent of SVG styling."""
import math
import unittest
import numpy as np
from shapely.geometry import Polygon
from erde_geometry import GEO, FRAME, PROJECTION, tr

class GeographyTests(unittest.TestCase):
    def test_rotation_preserves_selected_pole_and_native_latitudes(self):
        self.assertAlmostEqual(tr(-150,0)[1],90,places=6)
        self.assertAlmostEqual(tr(30,0)[1],-90,places=6)
        # Independent spherical dot-product formula, covering both hemispheres.
        for lon,lat in [(-169,65),(-17.4,14.7),(110,0),(-73,-22),(36,0),(143,-6)]:
            expected=math.degrees(math.asin(math.cos(math.radians(lat))*math.cos(math.radians(lon+150))))
            native=tr(lon,lat)
            self.assertAlmostEqual(native[1],expected,places=6)
            restored=GEO.transform_point(*native,FRAME)
            np.testing.assert_allclose(restored,[lon,lat],atol=1e-7)

    def test_equal_area_from_equator_to_poles_and_map_edges(self):
        radius=6371008.8
        for west in [-180,-120,-60,0,60,120,170]:
            for south in [-90,-75,-45,-15,0,30,60,80]:
                east,north=west+10,south+10
                # Densified parallels represent spherical rectangles, not geodesic quadrilaterals.
                lon=np.concatenate([np.linspace(west,east,101),np.full(101,east),np.linspace(east,west,101),np.full(101,west)])
                lat=np.concatenate([np.full(101,south),np.linspace(south,north,101),np.full(101,north),np.linspace(north,south,101)])
                projected=PROJECTION.transform_points(GEO,lon,lat)[:,:2]
                expected=radius**2*math.radians(10)*(math.sin(math.radians(north))-math.sin(math.radians(south)))
                with self.subTest(west=west,south=south):
                    self.assertTrue(np.isfinite(projected).all())
                    self.assertLess(abs(Polygon(projected).area/expected-1),0.00001)

    def test_curved_boundary_retains_finite_poles_and_round_trip(self):
        for lon,lat in [(-180,0),(180,0),(-180,75),(180,-75),(0,90),(0,-90),(38,54)]:
            point=PROJECTION.transform_point(lon,lat,GEO)
            self.assertTrue(np.isfinite(point).all())
            if abs(lat)<90:
                restored=GEO.transform_point(*point,PROJECTION)
                np.testing.assert_allclose(restored,[lon,lat],atol=1e-6)
        equator=abs(PROJECTION.transform_point(180,0,GEO)[0])
        high=abs(PROJECTION.transform_point(180,75,GEO)[0])
        self.assertLess(high,equator*.7)

if __name__=='__main__':
    unittest.main()
