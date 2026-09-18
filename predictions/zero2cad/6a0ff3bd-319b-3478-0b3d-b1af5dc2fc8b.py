import cadquery as cq

# Parameters
total_length = 80.0
start_width = 50.0
end_width = 30.0
start_height = 30.0
end_height = 20.0
wall_thickness = 3.0
rib_thickness = 2.0
rib_height = 4.0
rib_spacing = 10.0
chamfer_distance = 2.0

# Outer lofted housing
outer = (
    cq.Workplane("XY")
    .rect(start_width, start_height)
    .workplane(offset=total_length)
    .rect(end_width, end_height)
    .loft(combine=True)
)

# Chamfer on the start face edges before inner cut
outer = outer.faces("<Z").edges().chamfer(chamfer_distance)

# Inner cavity loft
inner_start_width = start_width - 2 * wall_thickness
inner_start_height = start_height - 2 * wall_thickness
inner_end_width = end_width - 2 * wall_thickness
inner_end_height = end_height - 2 * wall_thickness
inner = (
    cq.Workplane("XY")
    .rect(inner_start_width, inner_start_height)
    .workplane(offset=total_length)
    .rect(inner_end_width, inner_end_height)
    .loft(combine=True)
)

# Subtract inner cavity
housing = outer.cut(inner)

# Internal ribs
rib_count = int(total_length / rib_spacing)
rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_height)
    .extrude(total_length)
)
# Position ribs inside cavity, centered in Y, offset in X to sit against inner wall
rib = rib.translate((-(inner_start_width/2) + rib_thickness/2, 0, 0))
# Create array of ribs along Z
ribs = rib
for i in range(1, rib_count):
    ribs = ribs.union(rib.translate((0, 0, i * rib_spacing)))

# Combine ribs with housing
result = housing.union(ribs)
