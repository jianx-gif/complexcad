import cadquery as cq
outer_diameter = 80.0
inner_diameter = 40.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_spacing = 15.0
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
rib1 = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib1.union(rib1).union(rib2)
rib1 = rib3.faces(">Z").workplane().hole(hole_diameter)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
    .translate((0, 0, thickness))
)
rib3 = rib1.union(rib2)
rib1 = rib1.translate((0, 0, thickness))
rib2 = rib2.translate((0, 0, thickness))
rib3 = rib2.translate((0, 0, thickness))
result = base.union(rib1).union(rib2)
