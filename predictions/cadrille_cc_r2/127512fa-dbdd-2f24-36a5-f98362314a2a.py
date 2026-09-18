import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 8
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 30.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = rib.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
rib = rib.translate((inner_diameter / 2 + rib_width / 2, 0, 0))
combined = base.union(rib)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, hole_offset), (hole_spacing / 2, hole_offset)])
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, hole_offset), (hole_spacing / 2, hole_offset)])
    .hole(hole_diameter)
)
combined = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2, hole_offset), (hole_spacing / 2, hole_offset)])
    .hole(hole_diameter)
)
result = combined
