import cadquery as cq

# Parameters
channel_length = 80.0
channel_width = 50.0
channel_height = 20.0
wall_thickness = 1.0
chamfer_size = 0.2
hole_diameter = 3.0
hole_spacing = 15.0
hole_count = 4
tab_width = 20.0
tab_height = 5.0
tab_thickness = 3.0
rib_width = 30.0
rib_height = 12.0
rib_thickness = 2.0

# Base solid
base = (
    cq.Workplane("YZ")
    .rect(channel_width, channel_height)
    .extrude(channel_length)
)

# Thin-walled channel
hollow = base.shell(-wall_thickness)

# Chamfer outer vertical edges
chamfered = hollow.edges("|Z").chamfer(chamfer_size)

# Add mounting tab on +X face
with_tab = (
    chamfered
    .faces(">X")
    .workplane()
    .rect(tab_width, tab_height)
    .extrude(tab_thickness, combine=True)
)

# Add internal rib on bottom interior face
with_rib = (
    with_tab
    .faces("<Z")
    .workplane(invert=True)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness, combine=True)
)

# Drill linear array of screw holes on +Y side
result = (
    with_rib
    .faces(">Y")
    .workplane()
    .rarray(hole_spacing, 0, hole_count, 1)
    .hole(hole_diameter)
)
