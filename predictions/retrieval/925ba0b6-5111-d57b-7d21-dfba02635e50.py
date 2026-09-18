import cadquery as cq
import math

outer_diameter = 80.0
inner_diameter = 40.0
base_thickness = 15.0
rib_height = 5.0
rib_width = 4.0
rib_inset = 0.5
blind_hole_diameter = 12.0
blind_hole_depth = base_thickness - 2.0
chamfer_distance = 2.0
mount_hole_diameter = 5.0
mount_hole_count = 6
mount_hole_radius = outer_diameter/2 - 10.0

base = cq.Workplane("XY").circle(outer_diameter/2).extrude(base_thickness)

shaft_hole = (
    base.faces(">Z").workplane()
    .hole(inner_diameter)
)

blind_hole = (
    shaft_hole.faces(">Z").workplane()
    .center(0, 0)
    .circle(blind_hole_diameter/2)
    .cutBlind(blind_hole_depth)
)

rib = (
    blind_hole.faces(">Z").workplane()
    .center(0, 0)
    .circle(outer_diameter/2 + rib_width)
    .circle(outer_diameter/2 - rib_inset)
    .extrude(rib_height)
)

combined = blind_hole.union(rib)

angle_step = 360.0 / mount_hole_count
points = [
    (
        mount_hole_radius * math.cos(math.radians(i * angle_step)),
        mount_hole_radius * math.sin(math.radians(i * angle_step))
    )
    for i in range(mount_hole_count)
]

with_holes = (
    combined.faces("<Z").workplane()
    .pushPoints(points)
    .hole(mount_hole_diameter)
)

result = with_holes.faces("<Z").edges().chamfer(chamfer_distance)
