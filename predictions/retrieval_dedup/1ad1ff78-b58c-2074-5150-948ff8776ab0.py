import cadquery as cq

# parameters
block_length = 80.0
block_width = 50.0
block_height = 20.0
wall_thickness = 2.0
rib_thickness = 4.0
rib_offset = 10.0
blind_hole_diameter = 6.0
blind_hole_depth = 12.0
chamfer_distance = 0.5

# base solid block
base = cq.Workplane("XY").box(block_length, block_width, block_height)

# shell to create thin walls
hollow = base.shell(wall_thickness)

# internal rib along length (X direction)
rib_height = block_height - 2*wall_thickness
rib1 = (
    hollow
    .faces(">Z").workplane(offset=-wall_thickness)
    .center(0, 0)
    .rect(rib_thickness, block_length - 2*wall_thickness)
    .extrude(-rib_height)
)

# internal rib along width (Y direction)
rib2 = (
    rib1
    .faces(">Z").workplane(offset=-wall_thickness)
    .center(0, 0)
    .rect(rib_thickness, block_width - 2*wall_thickness)
    .extrude(-rib_height)
)

# add blind hole from top exterior
blind_hole = (
    rib2
    .faces(">Z")
    .workplane()
    .hole(blind_hole_diameter, blind_hole_depth)
)

# add chamfer to outer edges
result = (
    blind_hole
    .edges("|Z")
    .chamfer(chamfer_distance)
)
