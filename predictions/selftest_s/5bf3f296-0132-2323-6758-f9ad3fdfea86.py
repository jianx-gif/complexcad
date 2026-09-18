import cadquery as cq

# Primary dimensions
circle_diameter = 40.0
rect_width = 60.0
rect_height = 30.0
block_height = 40.0
hole_diameter = 20.0
fillet_radius = 3.0
rib_thickness = 5.0
rib_height = block_height * 0.6
rib_length = 15.0
side_hole_diameter = 8.0
side_hole_offset = 20.0
pocket_width = 30.0
pocket_depth = 10.0
pocket_margin = 5.0
boss_diameter = 12.0
boss_height = 6.0
countersink_angle = 90.0
peripheral_hole_dia = 4.0
peripheral_rows = 2
peripheral_spacing = 15.0

# Lofted base between a circle and a rectangle
base = (
    cq.Workplane("XY")
    .circle(circle_diameter / 2)
    .workplane(offset=block_height)
    .rect(rect_width, rect_height)
    .loft(combine="s")
)

# Fillet only the top edges to avoid geometry failures
base_fillet = base.edges(">Z").fillet(fillet_radius)

# Central through‑hole
central = base_fillet.faces(">Z").workplane().hole(hole_diameter)

# Countersunk mounting holes on the top face
mount_holes = (
    central
    .faces(">Z")
    .workplane()
    .pushPoints([(-side_hole_offset, 0), (side_hole_offset, 0)])
    .cskHole(side_hole_diameter, boss_height, countersink_angle)
)

# Top central boss
top_boss = (
    mount_holes
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Cable routing pocket cutout centered on top
pocket = (
    top_boss
    .faces(">Z")
    .workplane()
    .rect(pocket_width, pocket_width)
    .cutBlind(-pocket_depth)
)

# Clearance slot on the -Y face for assembly alignment
slot = (
    pocket
    .faces("<Y")
    .workplane()
    .center(pocket_margin, 0)
    .rect(pocket_margin * 2, pocket_width * 0.5)
    .cutBlind(-block_height * 0.8)
)

# Peripheral array of small through‑holes on the top face
peripheral = (
    slot
    .faces(">Z")
    .workplane()
    .rarray(peripheral_spacing, peripheral_spacing, peripheral_rows, peripheral_rows, center=True)
    .hole(peripheral_hole_dia)
)

result = peripheral