import cadquery as cq
outer_diameter = 60.0
inner_diameter = 30.0
thickness = 15.0
wall_thickness = 2.0
fillet_radius = 2.0
chamfer_distance = 0.5
rib_width = 4.0
rib_height = 10.0
rib_thickness = 2.0
rib_spacing = 12.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness))
rib = rib.translate((0, 0, thickness