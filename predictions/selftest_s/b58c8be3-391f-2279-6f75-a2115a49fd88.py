import cadquery as cq
from cadquery import Plane
import math

housing_height = 70.0
outer_radius = 30.0
inner_radius = 12.0
bearing_seat_radius = 14.0
bearing_seat_depth = 5.0
rib_thickness = 3.0
rib_height = 20.0
mount_hole_diameter = 4.0
mount_hole_count = 6
mount_hole_radius = 22.0
fillet_radius = 1.0

class ClutchHousing:
    def __init__(self):
        pass
    def _profile(self):
        wp = cq.Workplane('XZ')
        wp = wp.moveTo(0, 0)
        wp = wp.lineTo(outer_radius, 0)
        wp = wp.lineTo(outer_radius, housing_height - bearing_seat_depth)
        wp = wp.threePointArc((bearing_seat_radius, housing_height - bearing_seat_depth), (bearing_seat_radius, housing_height))
        wp = wp.lineTo(inner_radius, housing_height)
        wp = wp.lineTo(0, housing_height)
        wp = wp.close()
        return wp
    def _rib(self, solid):
        rib = (
            cq.Workplane('XY')
            .rect(rib_thickness, rib_height)
            .extrude(rib_thickness)
        )
        rib = rib.translate((outer_radius - rib_thickness/2, 0, housing_height/2))
        return solid.union(rib)
    def _mounting_holes(self, solid):
        points = [
            (mount_hole_radius * math.cos(math.radians(i * 360 / mount_hole_count)),
             mount_hole_radius * math.sin(math.radians(i * 360 / mount_hole_count)))
            for i in range(mount_hole_count)
        ]
        return (
            solid.faces('>Z')
            .workplane()
            .pushPoints(points)
            .hole(mount_hole_diameter)
        )
    def build(self):
        profile = self._profile()
        solid = profile.revolve()
        solid = solid.fillet(fillet_radius)
        solid = self._rib(solid)
        solid = self._mounting_holes(solid)
        split_plane = Plane.YZ
        halves = solid.split(split_plane)
        return halves

result = ClutchHousing().build()
