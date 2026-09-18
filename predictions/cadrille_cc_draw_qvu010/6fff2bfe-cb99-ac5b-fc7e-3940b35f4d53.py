import cadquery as cq
outer_diameter = 60.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_radius = inner_diameter / 2.0
hole_offset = 10.0
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, outer_diameter / 2)
    .lineTo(outer_diameter / 2, outer_diameter / 2)
    .lineTo(outer_diameter / 2, outer_diameter / 2)
    .lineTo(outer_diameter / 2, outer_diameter / 2)
    .close()
)
solid = profile.revolve()
solid = solid.edges().chamfer(chamfer_size)
solid = solid.faces(">Z").workplane().hole(hole_diameter)
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_offset, startAngle=0, count=hole_count, angle=360)
    .hole(hole_diameter)
)
solid = solid.faces(">Z").edges().chamfer(chamfer_size)
result = solid
