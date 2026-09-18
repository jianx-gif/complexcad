import cadquery as cq
guide_length = 80.0
guide_width = 30.0
guide_height = 20.0
wall_thickness = 4.0
tab_width = 12.0
tab_thickness = 5.0
tab_height = 8.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_count = 6
hole_spacing = guide_length / (hole_count - 1)
hole_spacing = guide_length / (hole_count - 1)
base = (
    cq.Workplane("XY")
    .rect(guide_length, guide_width)
    .extrude(guide_height)
)
tab = (
    cq.Workplane("XY")
    .rect(tab_width, guide_width)
    .extrude(guide_height)
    .translate((0, 0, guide_height))
)
combined = base.union(tab)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = combined.edges("|Z").chamfer(chamfer_size)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (0, guide_width / 2)])
    .circle(hole_diameter / 2)
    .cutBlind(-hole_spacing)
)
combined = combined.edges("|Z").chamfer(chamfer_size)
result = combined
