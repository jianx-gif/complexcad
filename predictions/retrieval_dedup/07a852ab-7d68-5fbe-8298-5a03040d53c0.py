
import cadquery as cq
from math import cos, sin, radians

outer_radius = 40.0
wall_thickness = 5.0
cover_height = 15.0
rib_thickness = 2.0
rib_height = 4.0
rib_width = 6.0
rib_count = 12
chamfer_size = 1.0
hole_diameter = 6.0
hole_offset_radius = 20.0

inner_radius = outer_radius - wall_thickness

outer_cyl = cq.Workplane("XY").cylinder(cover_height, outer_radius)
inner_cyl = cq.Workplane("XY").cylinder(cover_height, inner_radius)
base_shell = outer_cyl.cut(inner_cyl)

chamfered_shell = (
    base_shell
    .edges(">Z")
    .chamfer(chamfer_size)
)

# peripheral ribs added directly on the top face
ribs = (
    chamfered_shell
    .faces(">Z")
    .workplane()
    .polarArray(0, 0, 360, rib_count)
    .center(outer_radius - rib_thickness/2, 0)
    .rect(rib_thickness, rib_width)
    .extrude(rib_height)
)

result = ribs
for theta in (0, 180):
    result = (
        result
        .faces(">Z")
        .workplane(centerOption="CenterOfMass")
        .center(hole_offset_radius * cos(radians(theta)), hole_offset_radius * sin(radians(theta)))
        .hole(hole_diameter)
    )

result = result.combine()
