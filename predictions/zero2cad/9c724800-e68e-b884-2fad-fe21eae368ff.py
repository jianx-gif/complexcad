import cadquery as cq

# Parameters
clip_length = 80.0
clip_width = 40.0
sheet_thickness = 2.0
split_gap = 2.0
split_offset = 30.0
tab_width = 10.0
tab_height = 12.0
tab_offset = 15.0
hole_diameter = 5.0
hole_offset_x = 20.0
hole_offset_y = 10.0
chamfer_size = 0.5

# Base plate
base = (
    cq.Workplane("XY")
    .rect(clip_length, clip_width)
    .extrude(sheet_thickness)
)

# Split gap cut (creates the split line)
split_cut = (
    cq.Workplane("XY")
    .center(split_offset, clip_width/2)
    .rect(split_gap, clip_width - 2*sheet_thickness)
    .extrude(sheet_thickness + 0.1)
)

# Tab cutout (creates a tab for mounting)
tab_cut = (
    cq.Workplane("XY")
    .center(-clip_length/2 + tab_offset, -clip_width/2 + tab_height/2)
    .rect(tab_width, tab_height)
    .extrude(sheet_thickness + 0.1)
)

# Assemble base with cuts
result = base.cut(split_cut).cut(tab_cut)

# Add mounting hole through the tab region
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_offset_x, hole_offset_y)
    .hole(hole_diameter)
)

# Apply chamfer to outer edges for safety
result = result.edges("|Z").chamfer(chamfer_size)
