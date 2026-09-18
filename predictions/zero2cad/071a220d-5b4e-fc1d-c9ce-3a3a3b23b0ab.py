import cadquery as cq

outer_diameter = 80.0
inner_diameter = 40.0
length = 70.0
wall_thickness = (outer_diameter - inner_diameter) / 2.0
fillet_radius = 2.0
chamfer_distance = 0.8
mount_hole_diameter = 5.0
mount_hole_spacing = 30.0
rib_width = 12.0
rib_height = 8.0
rib_length = length - 10.0
slot_width = 10.0
slot_length = 20.0
slot_depth = wall_thickness - 2.0

base = (
    cq.Workplane("XY")
    .sketch()
    .circle(outer_diameter / 2.0)
    .rect(inner_diameter, inner_diameter, mode="s")
    .finalize()
    .extrude(length)
)

base = base.edges("|Z").fillet(fillet_radius)
base = base.edges().chamfer(chamfer_distance)

hole_positions = [
    (mount_hole_spacing / 2.0, 0),
    (-mount_hole_spacing / 2.0, 0),
    (0, mount_hole_spacing / 2.0),
    (0, -mount_hole_spacing / 2.0),
]
base = (
    base.faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)
rib1 = rib.translate((0, 0, length / 2.0 - rib_height / 2.0))
rib2 = rib.translate((0, 0, -length / 2.0 + rib_height / 2.0))
base = base.union(rib1).union(rib2)

slot = (
    cq.Workplane("XY")
    .rect(slot_width, slot_length)
    .extrude(slot_depth)
    .translate((outer_diameter / 2.0 - slot_depth / 2.0, 0, length / 2.0))
)
base = base.cut(slot)

result = base