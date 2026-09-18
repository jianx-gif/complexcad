import cadquery as cq

base_length = 80.0
base_width = 30.0
base_thickness = 8.0
lip_height = 12.0
lip_thickness = 4.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 50.0
hole_offset = 10.0
rib_width = 5.0
rib_height = 3.0
rib_depth = 2.0
rib_spacing = 20.0
slot_width = 6.0
slot_length = 30.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)

# Front lip on +Y side
lip = (
    base.faces(">Y")
    .workplane()
    .rect(base_length, lip_thickness)
    .extrude(lip_height)
)

combined = base.union(lip)

# Threaded holes through base, centered in Y, spaced along X
hole_positions = [(-hole_spacing / 2, 0), (hole_spacing / 2, 0)]
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

# Slot on front lip for guide clearance
combined = (
    combined
    .faces(">Y")
    .workplane()
    .center(0, 0)
    .rect(slot_length, slot_width)
    .cutBlind(-lip_thickness)
)

# Underside ribs for stiffness, arrayed along length
rib_array = (
    combined
    .faces("<Z")
    .workplane()
    .rarray(xSpacing=rib_spacing, ySpacing=0, xCount=int(base_length / rib_spacing) + 1, yCount=1)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)

combined = combined.union(rib_array)

# Chamfer on front lip edges (vertical front edges and top front edge)
combined = (
    combined
    .edges("<Y")
    .chamfer(chamfer_size)
)

result = combined