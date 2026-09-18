import cadquery as cq
outer_radius = 20.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
rib_height = 4.0
rib_width = 6.0
rib_length = 30.0
rib_thickness = 2.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 15.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, rib_height)
    .lineTo(outer_radius, rib_height)
    .lineTo(inner_radius, rib_height)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .box(rib_length, rib_width, rib_thickness)
    .translate((inner_radius + rib_thickness/2, 0, rib_height/2))
)
solid = solid.union(rib)
solid = solid.edges().chamfer(chamfer_size)
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
solid = solid.edges("|Z").chamfer(chamfer_size)
result = solid
