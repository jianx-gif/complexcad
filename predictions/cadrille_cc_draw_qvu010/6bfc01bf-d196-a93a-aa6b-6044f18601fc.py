import cadquery as cq
outer_diameter = 80.0
wall_thickness = 4.0
inner_diameter = outer_diameter - 2 * wall_thickness
inner_radius = outer_diameter / 2.0
chamfer_size = 1.0
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = 12
hole_offset = 10.0
rib_width = 6.0
rib_height = 12.0
rib_thickness = 2.0
rib_spacing = 12.0
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(outer_diameter)
)
base = base.edges().chamfer(chamfer_size)
rib = (
    cq.Workplane("XY")
    .center(outer_diameter / 2.0, 0)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
base = base.union(rib)
base = base.faces(">Z").edges().chamfer(chamfer_size)
hole_positions = [
    (inner_radius, 0),
    (-inner_radius, 0),
    (inner_radius, inner_radius),
    (-inner_radius, inner_radius),
]
base = (
    base.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
base = (
    base.faces(">Z").workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)
rib = rib.translate((0, 0, outer_diameter / 2.0 - rib_thickness / 2.0))
rib = rib.translate((0, 0, outer_diameter / 2.0 - rib_thickness / 2.0))
rib = rib.translate((0, 0, outer_diameter / 2.0 - rib_thickness / 2.0))
result = base.union(rib)
