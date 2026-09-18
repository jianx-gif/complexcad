import cadquery as cq

# Parameters
bracket_length = 80.0
bracket_width = 60.0
bracket_thickness = 10.0
cutout_width = 30.0
cutout_height = 25.0
cutout_offset_x = 10.0
cutout_offset_y = 15.0
hole_diameter = 6.0
hole_spacing = 20.0
hole_offset_y = 10.0
chamfer_distance = 6.0
rib_width = 5.0
rib_height = 4.0
rib_spacing = 15.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(bracket_length, bracket_width)
    .extrude(bracket_thickness)
)

# Rectangular cutout through thickness
cutout = (
    base.faces(">Z")
    .workplane()
    .center(-bracket_length/2 + cutout_offset_x + cutout_width/2,
            -bracket_width/2 + cutout_offset_y + cutout_height/2)
    .rect(cutout_width, cutout_height)
    .cutBlind(-bracket_thickness)
)

# Three through holes aligned vertically
holes = (
    cutout.faces(">Z")
    .workplane()
    .center(-bracket_length/2 + cutout_offset_x + cutout_width/2,
            -bracket_width/2 + hole_offset_y + hole_diameter/2)
    .rarray(0, hole_spacing, 1, 3)
    .hole(hole_diameter)
)

# Chamfer outer vertical edges before adding ribs
chamfered = holes.edges("|Z").chamfer(chamfer_distance)

# Reinforcing ribs on top surface
rib_count = int((bracket_length - 2*cutout_offset_x) // rib_spacing)
rib_positions = [ -bracket_length/2 + cutout_offset_x + rib_spacing/2 + i*rib_spacing for i in range(rib_count) ]

ribs = (
    cq.Workplane("XY")
    .pushPoints([(x, 0) for x in rib_positions])
    .rect(rib_width, rib_height)
    .extrude(bracket_thickness)
)

result = chamfered.union(ribs)
