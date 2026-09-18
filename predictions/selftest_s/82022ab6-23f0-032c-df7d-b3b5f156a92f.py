import cadquery as cq

# Parameters
vertical_height = 80.0
horizontal_length = 60.0
leg_thickness = 12.0
flange_thickness = 8.0
flange_extension = 20.0
hole_diameter = 5.0
hole_count = 3
hole_offset_from_axis = leg_thickness - 2.5  # near outer surface
chamfer_size = 1.0

# Build 2D profile on XY plane (Y is axial direction)
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(leg_thickness, 0)
    .lineTo(leg_thickness, vertical_height)
    .lineTo(horizontal_length, vertical_height)
    .lineTo(horizontal_length, vertical_height - flange_thickness)
    .lineTo(flange_extension, vertical_height - flange_thickness)
    .lineTo(flange_extension, 0)
    .close()
)

# Revolve profile around Z axis to create L‑shaped support
solid = profile.revolve(360)

# Apply chamfer on all edges for safety
solid = solid.edges().chamfer(chamfer_size)

# Create three equally spaced holes around the cylindrical surface of the vertical leg
holes = (
    cq.Workplane("XY")
    .center(hole_offset_from_axis, vertical_height/2)
    .polarArray(radius=hole_offset_from_axis, startAngle=0, angle=360, count=hole_count)
    .circle(hole_diameter/2)
    .extrude(vertical_height)
)

solid = solid.cut(holes)

result = solid
