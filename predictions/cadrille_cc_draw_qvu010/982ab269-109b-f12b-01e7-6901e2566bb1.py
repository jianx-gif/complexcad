import cadquery as cq
outer_diameter = 60.0
wall_thickness = 2.0
inner_diameter = outer_diameter - 2 * wall_thickness
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness
inner_radius = outer_radius - wall_thickness
chamfer_distance = 0.5
hole_diameter = 5.0
hole_spacing = 30.0
rib_width = 4.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
outer_radius = outer_radius - wall_thickness
inner_radius = inner_radius - wall_thickness
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, inner_radius)
    .lineTo(outer_radius, inner_radius)
    .lineTo(outer_radius, inner_radius)
    .lineTo(inner_radius, inner_radius)
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
rib = (
    cq.Workplane("XY")
    .center(inner_radius + rib_thickness / 2.0, inner_radius + rib_height / 2.0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
solid = solid.union(rib)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
hole_positions = [
    (inner_radius + wall_thickness + hole_spacing / 2.0, inner_radius + hole_spacing / 2.0),
    (inner_radius + wall_thickness + hole_spacing / 2.0, inner_radius + hole_spacing / 2.0),
    (-inner_radius, 0)
]
solid = (
    solid.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
solid = solid.faces(">Z").edges().chamfer(chamfer_distance)
result = solid
