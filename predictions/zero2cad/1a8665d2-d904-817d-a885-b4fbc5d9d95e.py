import cadquery as cq
import math
outer_diameter = 80.0
inner_diameter = 30.0
pulley_width = 20.0
groove_angle = 120.0
groove_depth = 10.0
groove_width = 15.0
set_screw_diameter = 5.0
set_screw_head_diameter = 9.0
set_screw_head_depth = 3.0
set_screw_offset = 12.0
chamfer_size = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
half_width = pulley_width / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, -half_width)
    .lineTo(inner_radius, half_width)
    .lineTo(outer_radius, half_width)
    .lineTo(outer_radius, -half_width)
    .close()
)
base = profile.revolve()
# V-groove wedge
wedge = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, -groove_width/2)
    .lineTo(outer_radius - groove_depth, 0)
    .lineTo(outer_radius, groove_width/2)
    .close()
    .extrude(pulley_width)
)
base = base.cut(wedge)
# Set screw hole with countersink
base = (
    base.faces(">Z")
    .workplane()
    .center(set_screw_offset, 0)
    .cskHole(set_screw_head_diameter, set_screw_head_depth, set_screw_diameter)
)
# Chamfer outer rim edges
base = base.edges("|Z").chamfer(chamfer_size)
result = base