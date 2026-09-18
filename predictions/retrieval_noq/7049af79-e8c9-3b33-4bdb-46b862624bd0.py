import cadquery as cq

cover_length = 80.0
cover_width = 60.0
base_thickness = 5.0
lip_height = 4.0
taper_angle = 5.0
wall_thickness = 2.0
hole_diameter = 4.0
hole_spacing_x = 30.0
hole_spacing_y = 20.0
num_holes_x = 2
num_holes_y = 2
rib_width = 8.0
rib_thickness = 3.0
rib_height = 2.0
chamfer_dist = 0.5

# Base plate
base = (
    cq.Workplane("XY")
    .rect(cover_length, cover_width)
    .extrude(base_thickness)
)

# Tapered lip on top of base
lip = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_thickness))
    .rect(cover_length, cover_width)
    .extrude(lip_height, taper=taper_angle)
)

# Single rib profile
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)

# Position ribs near each long edge of the cover
rib_left = rib.translate((0, cover_width/2 - rib_thickness/2, base_thickness + lip_height/2))
rib_right = rib_left.mirror(mirrorPlane="XZ")

# Combine base, lip, and ribs
combined = base.union(lip).union(rib_left).union(rib_right)

# Chamfer bottom outer edges
chamfered = combined.faces("<Z").edges().chamfer(chamfer_dist)

# Mounting holes through the bottom face
result = (
    chamfered.faces("<Z")
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, num_holes_x, num_holes_y, center=True)
    .hole(hole_diameter)
)
