import cadquery as cq

jaw_length = 80.0
jaw_width = 30.0
jaw_thickness = 8.0
lip_height = 12.0
lip_thickness = 4.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_offset = 15.0
rib_width = 5.0
rib_height = 3.0
rib_spacing = 20.0
rib_depth = 2.0

base = (
    cq.Workplane("XY")
    .rect(jaw_length, jaw_width)
    .extrude(jaw_thickness)
)

lip = (
    base.faces(">Y")
    .workplane()
    .rect(jaw_length, lip_thickness)
    .extrude(lip_height)
)

combined = base.union(lip)

combined = combined.faces("<Y").edges().chamfer(chamfer_size)

hole_positions = [(-jaw_length/2 + hole_offset, 0), (jaw_length/2 - hole_offset, 0)]
combined = (
    combined.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)

rib_count = int(jaw_length / rib_spacing) + 1
combined = (
    combined.faces("<Z")
    .workplane()
    .rarray(rib_spacing, 0, rib_count, 1)
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
)

result = combined