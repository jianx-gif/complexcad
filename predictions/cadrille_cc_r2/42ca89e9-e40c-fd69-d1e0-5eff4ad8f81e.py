import cadquery as cq
outer_diameter = 30.0
inner_diameter = 20.0
thickness = 10.0
chamfer_distance = 2.0
hole_diameter = 5.0
hole_spacing = 12.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 4.0
rib_thickness = 2.0
rib_spacing = 12.0
rib_count = int((outer_diameter - 2 * rib_spacing) // rib_spacing)
base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib1 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib2 = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(thickness)
)
rib3 = rib1.union(rib2)
rib4 = rib3.mirror(mirrorPlane="YZ")
hole_positions = [
    ( hole_offset,  hole_offset),
    (-hole_offset,  hole_offset),
    ( hole_offset, -hole_offset),
    ( hole_offset, -hole_offset),
]
result = (
    base
    .faces(">Z")
    .workplane()
    .pushPoints(hole_positions)
    .hole(hole_diameter)
)
