import cadquery as cq

block_length = 80.0
block_width = 50.0
block_height = 20.0
fillet_radius = 3.0
cavity_length = 60.0
cavity_width = 30.0
cavity_depth = 12.0
counterbore_head_dia = 15.0
counterbore_head_depth = 2.0
counterbore_dia = 8.0
counterbore_depth = 8.0
mounting_hole_dia = 5.0
mounting_hole_spacing = 40.0
rib_thickness = 4.0
rib_height = 6.0
chamfer_size = 1.0

# Base block with outer fillets
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges()
    .fillet(fillet_radius)
)

# Rectangular cavity centered on top face
base = (
    base
    .faces(">Z")
    .workplane()
    .rect(cavity_length, cavity_width)
    .cutBlind(-cavity_depth)
)

# Blind counterbore at cavity centre on outer top surface
base = (
    base
    .faces(">Z")
    .workplane()
    .hole(counterbore_head_dia, depth=counterbore_head_depth)
    .hole(counterbore_dia, depth=counterbore_depth)
)

# Mounting holes pattern on the +X side face
base = (
    base
    .faces(">X")
    .workplane(offset=block_height/2)
    .pushPoints([(-mounting_hole_spacing/2, 0), (mounting_hole_spacing/2, 0)])
    .hole(mounting_hole_dia)
)

# Internal ribs on the cavity floor (‑Z face after cut)
rib1 = (
    base
    .faces("<Z")
    .workplane()
    .rect(cavity_length - 2*fillet_radius, rib_thickness)
    .extrude(rib_height)
    .edges("|Z")
    .chamfer(chamfer_size)
)

rib2 = (
    base
    .faces("<Z")
    .workplane()
    .rect(rib_thickness, cavity_width - 2*fillet_radius)
    .extrude(rib_height)
    .edges("|Z")
    .chamfer(chamfer_size)
)

# Combine base and ribs into final part
result = base.union(rib1).union(rib2)
