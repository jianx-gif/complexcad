import cadquery as cq

# Parameters
cap_height = 40.0
outer_dia = 30.0
wall_thk = 2.0
chamfer_distance = 0.5
rib_height = 8.0
rib_thk = 2.0
rib_position = 20.0
hole_dia = 5.0

# Derived dimensions
outer_radius = outer_dia / 2.0
inner_radius = outer_radius - wall_thk

# Create hollow cylindrical body by revolving a wall profile
body = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, cap_height)
    .lineTo(outer_radius, cap_height)
    .lineTo(outer_radius, 0)
    .close()
    .revolve()
)

# External cylindrical rib on outer surface
rib = (
    cq.Workplane("XY")
    .circle(outer_radius + rib_thk)
    .extrude(rib_height)
    .translate((0, 0, rib_position))
)

# Combine body and rib
result = body.union(rib)

# Central through hole
result = result.faces(">Z").workplane().hole(hole_dia)

# Chamfer top edge (outer rim)
result = result.edges(">Z").chamfer(chamfer_distance)
