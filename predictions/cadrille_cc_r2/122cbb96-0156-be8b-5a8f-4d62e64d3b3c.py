import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
rib_height = 5.0
rib_width = 6.0
rib_thickness = 2.0
rib_spacing = 12.0
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 15.0
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib1 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib
    .faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib1 = rib3.translate((0, rib_spacing, 0))
rib2 = rib1.translate((0, rib_spacing, 0))
rib3 = rib2.translate((0, rib_spacing, 0))
rib1 = rib3.translate((0, rib_spacing, 0))
rib2 = rib1.translate((0, rib_spacing, 0))
rib3 = rib2.translate((0, rib_spacing, 0))
rib1 = rib2.workplane(offset=thickness).center(0, 0).rect(rib_width, rib_height).extrude(rib_thickness)
result = base.union(rib1).union(rib2)
