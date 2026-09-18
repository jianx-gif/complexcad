import cadquery as cq
outer_radius = 30.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
base_thickness = 10.0
base_height = 12.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_count = 6
hole_radius = hole_diameter / 2.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, base_height)
    .lineTo(outer_radius, base_height)
    .lineTo(outer_radius, base_thickness)
    .lineTo(outer_radius, base_thickness + base_thickness)
    .lineTo(outer_radius, base_thickness + base_thickness + 0.5)
    .lineTo(outer_radius, base_thickness + 0.5)
    .lineTo(outer_radius, base_thickness + 0.5)
    .close()
)
result = profile.revolve()
result = result.edges().chamfer(chamfer_size)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(hole_radius, 0, 360, hole_count)
    .hole(hole_diameter)
)
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(hole_radius, 0, 360, hole_count)
    .hole(hole_diameter)
)
