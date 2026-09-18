import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 3.0
rib_width = 6.0
rib_height = 2.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_size = 0.5
mount_hole_dia = 5.0
mount_hole_spacing = 30.0
rib_count = int(360 / rib_spacing)
profile = (
    cq.Workplane("XZ")
    .moveTo(inner_diameter / 2, 0)
    .lineTo(inner_diameter / 2, thickness)
    .lineTo(outer_diameter / 2, thickness)
    .lineTo(outer_diameter / 2, 0)
    .close()
)
rib = (
    cq.Workplane("XY")
    .box(rib_thickness, rib_height, rib_thickness)
    .translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
)
rib = rib.edges().chamfer(chamfer_size)
rib = rib.faces(">Z").workplane().hole(inner_diameter)
rib = rib.faces(">Z").workplane().hole(inner_diameter)
rib = rib.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().rect(rib_thickness, rib_height).extrude(rib_thickness)
result = rib
