import cadquery as cq
outer_diameter = 80.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = 4
chamfer_distance = 0.5
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
inner_radius = inner_radius + wall_thickness
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
rib3 = rib1.union(rib1).union(rib2)
rib1 = rib3.faces("<Z").workplane().hole(inner_radius * 2)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib1.union(rib2)
rib1 = rib3.faces(">Z").workplane().center(rib_spacing, 0).rect(rib_width, rib_height).extrude(thickness)
rib2 = rib1.faces(">Z").workplane().center(rib_spacing, 0).rect(rib_width, rib_height).extrude(thickness)
rib3 = rib1.faces(">Z").workplane().center(rib_spacing, 0).rect(rib_width, rib_height).extrude(thickness)
rib1 = rib3.faces("<Z").workplane().center(rib_spacing, 0).rect(rib_width, rib_height).extrude(rib_thickness)
result = rib1.union(rib1).union(rib2)
