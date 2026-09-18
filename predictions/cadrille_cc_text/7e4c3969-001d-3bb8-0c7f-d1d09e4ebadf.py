import cadquery as cq
outer_radius = 30.0
inner_radius = 20.0
thickness = 5.0
socket_depth = 2.0
pocket_width = 8.0
pocket_depth = 2.5
chamfer = 0.5
hole_diameter = 3.0
hole_depth = 2.5
hole_count = 6
hole_radial_offset = 25.0
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .close()
    .revolve()
)
base = base.edges().chamfer(chamfer)
pocket = (
    cq.Workplane("XY")
    .center(outer_radius - pocket_depth/2, 0)
    .rect(pocket_width, pocket_depth)
    .extrude(pocket_depth)
)
base = base.cut(pocket)
base = base.edges().chamfer(chamfer)
base = base.faces(">Z").workplane().hole(hole_diameter)
base = base.faces(">Z").workplane().polarArray(radius=hole_radial_offset, count=hole_count, startAngle=0, angle=360).hole(hole_diameter)
base = base.faces(">Z").workplane().polarArray(radius=hole_radial_offset, count=hole_count, startAngle=0, angle=360).hole(hole_diameter)
base = base.cut(base)
pocket = (
    cq.Workplane("XY")
    .center(outer_radius - pocket_depth/2, 0)
    .rect(pocket_width, pocket_depth)
    .extrude(pocket_depth)
)
result = base.cut(pocket)
