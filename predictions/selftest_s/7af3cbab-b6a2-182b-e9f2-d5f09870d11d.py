import cadquery as cq
import math

block_length = 80.0
block_width = 40.0
block_height = 20.0
boss_radius = 12.0
boss_height = 10.0
cone_angle = 30.0
cone_depth = 25.0
hole_diameter = 6.0
countersink_angle = 82.0
hole_through_depth = block_height + boss_height
fillet_radius = 2.0
chamfer_distance = 1.0
rib_height = 8.0
rib_thickness = 4.0
rib_spacing = 10.0

base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
)

boss = (
    cq.Workplane("XY")
    .center(0, 0)
    .circle(boss_radius)
    .extrude(boss_height)
)

solid = base.union(boss)

cone_radius_bottom = boss_radius
cone_radius_top = boss_radius - math.tan(math.radians(cone_angle / 2.0)) * cone_depth
if cone_radius_top < 1.0:
    cone_radius_top = 1.0
cavity_profile = (
    cq.Workplane("XZ")
    .moveTo(cone_radius_bottom, 0)
    .lineTo(cone_radius_bottom, cone_depth)
    .lineTo(cone_radius_top, cone_depth)
    .lineTo(cone_radius_top, 0)
    .close()
)

cavity = cavity_profile.revolve(360, (0, 0, 0), (0, 0, 1))
# Position cavity to stay below top surface
cavity = cavity.translate((0, 0, block_height - cone_depth - 2))
solid = solid.cut(cavity)

solid = solid.workplane(offset=block_height).cskHole(hole_diameter, hole_through_depth, countersink_angle)

solid = solid.edges("|Z").fillet(fillet_radius)
solid = solid.edges(">X").chamfer(chamfer_distance)

num_ribs = int((block_width - rib_spacing) // (rib_spacing + rib_thickness))
for i in range(num_ribs):
    y_offset = -block_width / 2 + rib_spacing + i * (rib_spacing + rib_thickness) + rib_thickness / 2
    rib = (
        cq.Workplane("XZ", origin=(block_length / 2 + rib_thickness / 2, 0, 0))
        .rect(rib_height, rib_thickness)
        .extrude(rib_thickness)
        .translate((0, y_offset, block_height / 2))
    )
    solid = solid.union(rib)

result = solid