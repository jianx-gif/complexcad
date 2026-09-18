import cadquery as cq
jaw_width = 80.0
jaw_height = 30.0
jaw_thickness = 10.0
rib_width = 5.0
rib_height = 20.0
rib_thickness = jaw_thickness
hole_diameter = 5.0
hole_spacing = 20.0
hole_offset = 10.0
chamfer_distance = 1.0
base = (
    cq.Workplane("XY")
    .rect(jaw_width, jaw_height)
    .extrude(jaw_thickness)
)
base = base.edges("|Z").chamfer(chamfer_distance)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.edges("|Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces(">Z").workplane().center(0, hole_offset).rect(rib_width, rib_height).extrude(rib_thickness)
base = base.edges("|Z").chamfer(chamfer_distance)
base = base.faces(">Z").workplane().center(0, hole_offset).hole(hole_diameter)
base = base.faces(">Z").edges().chamfer(chamfer_distance)
result = base
