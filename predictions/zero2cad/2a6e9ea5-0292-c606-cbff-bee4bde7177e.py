import cadquery as cq

# Parameters
outer_radius = 30.0
wall_thickness = 2.0
inner_radius = outer_radius - wall_thickness
channel_length = 80.0
inlet_length = 15.0
inlet_radius = 20.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_offset = 20.0
flange_thickness = 5.0
flange_extra = 2.0

# Build profile for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(inlet_radius, 0)
    .lineTo(outer_radius, inlet_length)
    .lineTo(outer_radius, channel_length)
    .lineTo(inner_radius, channel_length)
    .lineTo(inner_radius, inlet_length)
    .lineTo(inlet_radius, 0)
    .close()
)

# Revolve to create thin-walled channel
result = (
    profile
    .revolve()
    .faces("<Z")
    .edges()
    .chamfer(chamfer_size)
    .faces(">Z")
    .workplane()
    .circle(outer_radius + flange_extra)
    .circle(outer_radius)
    .extrude(flange_thickness)
    .faces(">X")
    .workplane()
    .center(0, hole_offset)
    .hole(hole_diameter)
)
