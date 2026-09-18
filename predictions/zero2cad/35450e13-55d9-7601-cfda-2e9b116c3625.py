import cadquery as cq

# Parameters
base_length = 80.0
base_width = 50.0
base_thickness = 10.0
slot_length = 60.0
slot_width = 10.0
rib_height = 6.0
rib_thickness = 4.0
rib_offset = 5.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_offset = 12.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)

# Slot cut through the plate
slot = (
    cq.Workplane("XY")
    .center(0, 0)
    .rect(slot_length, slot_width)
    .extrude(base_thickness + 2)
)
base = base.cut(slot)

# Mounting holes at four corners
hole_positions = [
    (-base_length/2 + hole_offset, -base_width/2 + hole_offset),
    ( base_length/2 - hole_offset, -base_width/2 + hole_offset),
    ( base_length/2 - hole_offset,  base_width/2 - hole_offset),
    (-base_length/2 + hole_offset,  base_width/2 - hole_offset),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Reinforcing rib on one side (positive X side)
rib = (
    cq.Workplane("XY")
    .center(base_length/2 - rib_offset - rib_thickness/2, 0)
    .rect(rib_thickness, base_width - 2*hole_offset)
    .extrude(rib_height)
)
base = base.union(rib)

# Chamfer outer edges
result = base.edges().chamfer(chamfer_size)
