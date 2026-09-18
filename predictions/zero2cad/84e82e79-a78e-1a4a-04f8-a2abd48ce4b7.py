import cadquery as cq

outer_diameter = 80.0
inner_diameter = 20.0
plate_thickness = 5.0
lip_height = 8.0
lip_width = 6.0
fillet_radius = 0.5
chamfer_distance = 0.5
rib_width = 8.0
rib_length = 30.0
rib_height = 2.0

base = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .extrude(plate_thickness)
)

lip = (
    cq.Workplane("XY")
    .circle((outer_diameter / 2) + lip_width)
    .extrude(lip_height)
    .translate((0, 0, plate_thickness))
)

washer = base.union(lip)

washer = washer.faces(">Z").workplane().hole(inner_diameter)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_length)
    .extrude(rib_height)
    .translate((0, 0, -rib_height))
)

ribs = rib
for angle in [90, 180, 270]:
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

washer = washer.union(ribs)

washer = washer.faces(">Z").edges().chamfer(chamfer_distance)

washer = washer.edges().fillet(fillet_radius)

result = washer