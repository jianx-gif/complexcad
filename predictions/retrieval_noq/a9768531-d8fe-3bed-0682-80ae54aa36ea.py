import cadquery as cq
BS = cq.selectors.BoxSelector

sleeve_length = 80.0
outer_diameter = 30.0
inner_diameter = 20.0
wall_thickness = (outer_diameter - inner_diameter) / 2.0
rib_height = 5.0
rib_width = 4.0
rib_axial = sleeve_length * 0.6
rib_count = 8
chamfer_distance = 2.0
hole_diameter = 4.0

outer = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(sleeve_length)
inner = cq.Workplane("XY").circle(inner_diameter / 2.0).extrude(sleeve_length)
inner = inner.faces(">Z").edges().chamfer(chamfer_distance)

sleeve = outer.cut(inner)

single_rib = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(outer_diameter / 2.0 - 0.01, 0, 0))
    .rect(rib_height, rib_width, centered=False)
    .extrude(rib_axial)
    .translate((0, 0, -rib_axial / 2.0))
)

ribs = single_rib
for i in range(1, rib_count):
    ribs = ribs.union(single_rib.rotate((0, 0, 0), (0, 0, 1), i * 360.0 / rib_count))

sleeve = sleeve.union(ribs)

hole_cyl = (
    cq.Workplane("XY")
    .circle(hole_diameter / 2.0)
    .extrude(wall_thickness + 2.0)
)

hole = hole_cyl.translate((outer_diameter / 2.0 - wall_thickness / 2.0, 0, 0))
hole_pattern = hole
for i in range(1, 4):
    hole_pattern = hole_pattern.union(hole.rotate((0, 0, 0), (0, 0, 1), i * 90.0))

result = sleeve.cut(hole_pattern)
