import cadquery as cq
block_length = 80.0
block_width = 50.0
block_height = 30.0
rib_width = 6.0
rib_height = 5.0
rib_spacing = 10.0
central_hole_diameter = 8.0
thread_pitch = 2.0
thread_depth = 2.0
corner_chamfer = 2.0
base = (
    cq.Workplane("XY")
    .rect(block_length, block_width)
    .extrude(block_height)
    .edges("|Z")
    .chamfer(corner_chamfer)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
base = base.edges("|Z").chamfer(corner_chamfer)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(central_hole_diameter)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(thread_depth, thread_depth)
    .extrude(thread_depth)
)
base = base.edges("|Z").chamfer(corner_chamfer)
result = base
