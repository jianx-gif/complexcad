import cadquery as cq
outer_radius = 40.0
inner_radius = 20.0
thickness = 10.0
rib_height = 4.0
rib_width = 6.0
rib_spacing = 12.0
rib_count = 12
rib_offset = 10.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 4
hole_offset = 15.0
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(inner_radius, thickness)
    .lineTo(inner_radius, 0)
    .close()
)
rib = profile.revolve(360)
rib = rib.faces(">Z").workplane().hole(inner_radius * 2)
rib = rib.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_height)
rib = rib.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_height)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.faces(">Z").workplane().rect(rib_width, rib_height).extrude(rib_height)
result = rib
