import cadquery as cq

# Parameters (all within 0-100 units)
base_radius = 20.0          # radius of the lower base cylinder
base_height = 15.0          # height of the lower base
shoulder_radius = 30.0      # radius where the turned knob begins
shoulder_height = 5.0       # vertical height of the shoulder section
knob_radius = 35.0          # maximum radius of the turned knob
knob_height = 20.0          # additional height of the knob above shoulder
pilot_hole_dia = 4.0        # diameter of the central pilot hole
chamfer_size = 2.0          # size of the chamfer on the top edge
mount_hole_dia = 5.0        # mounting hole diameter
mount_offset_radius = 15.0  # radial distance from center for mounting holes
mount_hole_count = 3        # number of mounting holes around the base

# Build 2D profile in the XZ plane for revolve
profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0)                                          # bottom outer edge
    .lineTo(base_radius, base_height)                                 # up side of base
    .lineTo(shoulder_radius, base_height)                             # outward to shoulder start
    .lineTo(shoulder_radius, base_height + shoulder_height)          # up shoulder
    .lineTo(knob_radius, base_height + shoulder_height)              # outward to knob radius
    .lineTo(knob_radius, base_height + shoulder_height + knob_height)  # up knob
    .lineTo(0, base_height + shoulder_height + knob_height)           # top radial line back to axis
    .close()
)

# Revolve to create axisymmetric gate stop
result = profile.revolve()

# Central pilot hole through the top face
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(pilot_hole_dia)
)

# Chamfer the outer edge of the top surface
result = (
    result
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

# Mounting holes pattern on the lower base side
result = (
    result
    .faces("<Z")
    .workplane()
    .polarArray(radius=mount_offset_radius, startAngle=0, angle=360, count=mount_hole_count)
    .hole(mount_hole_dia)
)
