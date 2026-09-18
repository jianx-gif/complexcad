import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
wall_thickness = 5.0
rib_height = 12.0
rib_width = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_depth = wall_thickness + 2.0
hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter/2, 0)
    .lineTo(outer_diameter/2, 0)
    .lineTo(outer_diameter/2, rib_height)
    .lineTo(outer_diameter/2, rib_height)
    .lineTo(outer_diameter/2, rib_height)
    .lineTo(outer_diameter/2, rib_height)
    .lineTo(inner_diameter/2, rib_height)
    .lineTo(inner_diameter/2, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter/2, rib_height/2)
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
solid = solid.cut(rib)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, -hole_offset),
    (-hole_offset, hole_offset),
]
solid = (
    solid.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
