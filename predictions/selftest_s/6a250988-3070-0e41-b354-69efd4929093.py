
import cadquery as cq
import math

chute_length = 40.0
large_diameter = 50.0
large_radius = large_diameter / 2.0
draft_angle_deg = 25.0
draft_angle_rad = math.radians(draft_angle_deg)
small_radius = max(large_radius - chute_length * math.tan(draft_angle_rad), 1.0)
base_thickness = 5.0
counterbore_diameter = 8.0
through_hole_diameter = 20.0
counterbore_offset = 2.0
chamfer_size = 1.0

profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (large_radius, 0),
        (large_radius, base_thickness),
        (large_radius, chute_length - base_thickness),
        (small_radius, chute_length),
        (0, chute_length),
    ])
    .close()
)

solid = profile.revolve()

result = (
    solid
    .faces(">Z")
    .workplane(offset=-counterbore_offset)
    .cboreHole(counterbore_diameter, through_hole_diameter, chute_length - counterbore_offset)
    .edges()
    .chamfer(chamfer_size)
)
