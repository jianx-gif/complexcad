import cadquery as cq
import math

outer_flat_distance = 50.0
wall_thickness = 0.9
length = 80.0
vent_hole_diameter = 3.0
vent_hole_spacing = 10.0
vent_margin = 2.0
chamfer_size = 0.5

side_length = outer_flat_distance * 2 * math.tan(math.radians(22.5))
vent_hole_count = int((side_length - 2 * vent_margin) / vent_hole_spacing)
start_x = -side_length / 2 + vent_margin

outer_radius = (outer_flat_distance / 2) / math.cos(math.radians(22.5))
hole_center_radius = outer_radius - wall_thickness / 2 - vent_hole_diameter / 2

base = (
    cq.Workplane("XY")
    .polygon(8, outer_flat_distance)
    .extrude(length)
)

hollow = base.shell(-wall_thickness)

chamfered = hollow.edges("|Z").chamfer(chamfer_size)

# create vent holes through side walls using radial cylinders
hole_solid = (
    cq.Workplane("YZ")
    .circle(vent_hole_diameter / 2)
    .extrude(length + 2)
    .translate((hole_center_radius, 0, - (length + 2) / 2 + length / 2))
)

holes = hole_solid
for i in range(1, 8):
    rotated = hole_solid.rotate((0, 0, 0), (0, 0, 1), i * 360 / 8)
    holes = holes.union(rotated)

result = chamfered.cut(holes)
