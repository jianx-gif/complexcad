import cadquery as cq

outer_radius = 30.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
length = 80.0
rib_height = 2.0
rib_width = 10.0
rib_start = 30.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 3

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, length)
    .lineTo(inner_radius, length)
    .lineTo(inner_radius, rib_start + rib_width)
    .lineTo(inner_radius + rib_height, rib_start + rib_width)
    .lineTo(inner_radius + rib_height, rib_start)
    .lineTo(inner_radius, rib_start)
    .lineTo(inner_radius, 0)
    .close()
)

solid = profile.revolve()

solid = solid.faces(">Z").edges().chamfer(chamfer_size)

result = (
    solid
    .faces(">Z")
    .workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)
