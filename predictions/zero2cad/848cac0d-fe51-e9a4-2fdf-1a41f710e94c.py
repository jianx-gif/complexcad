import cadquery as cq

outer_diameter = 80.0
cap_height = 30.0
wall_thickness = 5.0
base_fillet_radius = 4.0
top_chamfer_distance = 6.0
rib_count = 6
rib_width = 4.0
rib_height = 12.0
rib_thickness = 2.0

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(cap_height)
    .shell(-wall_thickness)
    .faces("<Z")
    .edges()
    .fillet(base_fillet_radius)
    .faces(">Z")
    .edges()
    .chamfer(top_chamfer_distance)
)

rib = (
    cq.Workplane("XZ")
    .center(inner_radius + rib_thickness / 2.0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_width)
)

ribs = rib
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

result = base.union(ribs)
