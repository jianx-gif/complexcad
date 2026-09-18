import cadquery as cq

# Parameters
base_radius = 30.0
top_radius = 20.0
height = 70.0
wall_thickness = 5.0
chamfer_size = 2.0
hole_diameter = 5.0
hole_count = 5
hole_pattern_radius = 15.0
slot_width = 8.0
slot_height = 12.0
slot_depth = wall_thickness + 1.0

# Outer profile sketch on XZ plane
outer_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)
    .lineTo(base_radius, height * 0.4)
    .lineTo(base_radius - wall_thickness, height * 0.4)
    .lineTo(top_radius, height)
    .lineTo(0, height)
    .close()
)

# Revolve to create solid
solid = outer_profile.revolve()

# Chamfer top edge
solid = solid.faces(">Z").edges().chamfer(chamfer_size)

# Add mounting holes on top face
solid = (
    solid.faces(">Z")
    .workplane()
    .polarArray(radius=hole_pattern_radius, startAngle=0, angle=360, count=hole_count)
    .hole(hole_diameter)
)

# Create side slot using a rectangular cut
slot = (
    cq.Workplane("XY")
    .box(slot_depth, slot_width, slot_height)
    .translate((base_radius - wall_thickness/2, 0, height/2))
)

result = solid.cut(slot)
