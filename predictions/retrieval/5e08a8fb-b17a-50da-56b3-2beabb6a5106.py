import cadquery as cq

block_length = 80.0
block_width = 50.0
block_height = 20.0
margin = 5.0
rib_thickness = 4.0
rib_height = 8.0
rib_spacing = 12.0
counterbore_dia = 12.0
fastener_dia = 5.0
counterbore_depth = 8.0
chamfer_size = 0.8

rib_start_x = -block_length/2 + margin + rib_spacing/2
rib_count = int((block_length - 2*margin) // rib_spacing)
points = [(rib_start_x + i * rib_spacing, 0) for i in range(rib_count)]

base = (
    cq.Workplane("XY")
    .box(block_length, block_width, block_height)
    .edges("|Z")
    .chamfer(chamfer_size)
)

rib_solid = (
    cq.Workplane("XY")
    .workplane(offset=block_height/2)
    .pushPoints(points)
    .rect(rib_thickness, block_width - 2 * margin)
    .extrude(-rib_height)
)

combined = base.union(rib_solid)

result = (
    combined
    .faces(">Z")
    .workplane()
    .hole(counterbore_dia, depth=counterbore_depth)
    .hole(fastener_dia, depth=block_height)
)
