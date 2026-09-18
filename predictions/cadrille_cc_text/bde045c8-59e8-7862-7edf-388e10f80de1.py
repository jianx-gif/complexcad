import cadquery as cq
bracket_width = 80.0
bracket_height = 100.0
bracket_thickness = 10.0
pocket_width = 50.0
pocket_height = 60.0
pocket_depth = 6.0
clearance_hole_dia = 8.0
hole_offset_y = 30.0
chamfer_size = 1.0
rib_width = 8.0
rib_height = 20.0
rib_depth = bracket_thickness - 2.0
base = (
    cq.Workplane("XY")
    .rect(bracket_width, bracket_height)
    .extrude(bracket_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_offset_y, 0), (hole_offset_y, 0)])
    .hole(clearance_hole_dia)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_depth)
    .translate((0, 0, bracket_thickness))
)
result = base.union(rib)
