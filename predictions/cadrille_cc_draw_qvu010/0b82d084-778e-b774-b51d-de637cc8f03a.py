import cadquery as cq
outer_diameter = 100.0
inner_diameter = 30.0
thickness = 6.0
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0
rib_count = 6
chamfer_distance = 0.5
hole_diameter = 5.0
hole_depth = thickness / 2.0
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2 - rib_thickness / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, 0))
combined = base.union(rib)
hole_positions = [
    (inner_diameter / 2 - rib_thickness / 2 - hole_offset),
    (-inner_diameter / 2 + rib_thickness / 2, 0),
    ( inner_diameter / 2 - rib_thickness / 2 - hole_offset, 0)
]
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
