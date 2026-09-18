import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
thickness = 10.0
wall_thickness = 2.0
fillet_radius = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 15.0
hole_offset = 10.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = int((outer_diameter - 2 * wall_thickness) // rib_spacing)
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
base = base.edges("|Z").fillet(fillet_radius)
base = (
    base.faces(">Z")
    .workplane()
    .circle(inner_diameter / 2)
    .cutBlind(-thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(inner_diameter / 2)
    .cutBlind(-thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutBlind(-thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutBlind(-thickness)
)
base = (
    base.faces(">Z")
    .workplane()
    .polarArray(radius=hole_offset, startAngle=0, count=hole_spacing, angle=360)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, thickness))
)
result = base.union(rib)
