import cadquery as cq
outer_diameter = 70.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(outer_diameter)
)
base = base.edges().chamfer(chamfer_size)
rib = (
    base.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    rib.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
rib = (
    rib.faces(">Z")
    .workplane()
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.edges("|Z").chamfer(chamfer_size)
)
result = rib
