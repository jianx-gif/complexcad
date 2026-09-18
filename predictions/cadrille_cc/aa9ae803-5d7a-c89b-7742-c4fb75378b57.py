import cadquery as cq
outer_radius = 20.0
inner_radius = 15.0
wall_thickness = 2.0
inner_radius = inner_radius + wall_thickness
base_thickness = 5.0
base_height = 10.0
chamfer_size = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_count = 6
hole_offset = 10.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(base_thickness)
)
base = (
    base.faces(">Z").workplane()
    .circle(inner_radius)
    .workplane(offset=base_height)
    .circle(inner_radius)
    .cutBlind(-base_thickness)
)
base = (
    base.faces(">Z").workplane()
    .circle(inner_radius)
    .cutBlind(-base_thickness)
)
base = (
    base.faces(">Z").workplane()
    .circle(inner_radius)
    .cutBlind(-base_thickness)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .circle(hole_diameter / 2)
    .cutBlind(-hole_spacing)
)
base = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .circle(hole_diameter / 2)
    .extrude(hole_depth)
)
base = base.edges("|Z").chamfer(chamfer_size)
result = base
