import cadquery as cq
outer_diameter = 50.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_offset = 10.0
rib_width = 4.0
rib_height = 3.0
rib_thickness = 2.0
rib_spacing = 12.0
base = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(outer_radius, 0)
    .lineTo(outer_radius, outer_diameter)
    .lineTo(inner_radius, outer_diameter)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)
rib = (
    cq.Workplane("XY")
    .center(outer_radius - rib_thickness / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges().chamfer(chamfer_size)
rib = rib.faces(">Z").workplane().hole(hole_diameter)
rib = rib.faces(">Z").workplane().hole(hole_diameter)
rib = rib.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_thickness)
rib = rib.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).cutBlind(-rib_thickness)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = rib.faces(">Z").workplane().center(0, 0).rect(rib_width, rib_height).extrude(rib_thickness)
result = rib
