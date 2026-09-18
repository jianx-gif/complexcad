import cadquery as cq
outer_diameter = 40.0
inner_diameter = 30.0
wall_thickness = 2.0
rib_height = 5.0
rib_width = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
chamfer_distance = 0.5
hole_diameter = 5.0
hole_depth = wall_thickness + 0.5
hole_spacing = 15.0
rib_count = int(360 / rib_spacing)
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(outer_diameter)
)
rib = (
    cq.Workplane("XY")
    .center(inner_diameter / 2 + rib_thickness / 2, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
rib = rib.translate((outer_diameter / 2 - rib_thickness / 2, 0, rib_height / 2))
combined = base.union(rib)
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_spacing, hole_spacing),
        (hole_spacing, hole_spacing),
        (hole_spacing, hole_spacing + hole_spacing),
        (hole_spacing, hole_spacing + hole_spacing)
    ])
    .hole(hole_diameter)
)
