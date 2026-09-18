import cadquery as cq
base_length = 80.0
base_width = 40.0
base_thickness = 6.0
rib_height = 12.0
rib_width = 10.0
rib_spacing = 12.0
rib_count = 6
hole_diameter = 5.0
hole_spacing = 20.0
chamfer_size = 1.0
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, base_thickness))
)
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .hole(hole_diameter)
)
result = (
    combined
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_height)
)
