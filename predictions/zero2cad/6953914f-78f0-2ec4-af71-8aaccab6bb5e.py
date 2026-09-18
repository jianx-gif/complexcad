import cadquery as cq

outer_diameter = 80.0
wall_thickness = 2.0
height = 30.0
lip_height = 5.0
chamfer_size = 0.8
hole_diameter = 4.0
hole_count = 6
hole_radius = 20.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

profile = (
    cq.Workplane("XZ")
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, height)
    .lineTo(inner_radius, height)
    .lineTo(inner_radius, height + lip_height)
    .lineTo(outer_radius, height + lip_height)
    .close()
)

solid = profile.revolve()

solid = solid.edges().chamfer(chamfer_size)

result = (
    solid
    .faces(">Z")
    .workplane()
    .polarArray(radius=hole_radius, count=hole_count, startAngle=0, angle=360)
    .hole(hole_diameter)
)
