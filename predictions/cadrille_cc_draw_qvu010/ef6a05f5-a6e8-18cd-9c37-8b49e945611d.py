import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
thickness = 30.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 15.0
hole_count = 4
hole_offset = 10.0
profile = (
    cq.Workplane("XY")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, 0)
    .close()
)
solid = profile.extrude(thickness)
solid = solid.edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - wall_thickness / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
hole_positions = [
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
    (hole_offset, hole_offset),
    (-hole_offset, hole_offset),
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
solid = solid.edges("|Z").chamfer(chamfer_distance)
result = solid
