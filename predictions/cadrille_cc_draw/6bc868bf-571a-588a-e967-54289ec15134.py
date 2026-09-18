import cadquery as cq
outer_diameter = 60.0
wall_thickness = 5.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 4.0
hole_spacing = 12.0
hole_count = 6
hole_radius = inner_radius + wall_thickness
outer_radius = outer_diameter / 2.0
inner_radius = inner_radius + wall_thickness
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_radius)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(inner_radius)
    .cutBlind(-wall_thickness)
)
base = (
    base
    .faces(">Z")
    .workplane()
    .circle(hole_radius)
    .cutBlind(-wall_thickness)
)
result = base
