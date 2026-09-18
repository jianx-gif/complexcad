import cadquery as cq

# Parameters
outer_radius = 40.0
length = 80.0
wall_thickness = 5.0
inner_radius = outer_radius - wall_thickness
bottom_fillet_radius = 3.0
cooling_hole_dia = 3.0
num_holes_z = 6
num_holes_y = 4
tab_width = 30.0
tab_height = 15.0
tab_thickness = 8.0
tab_hole_dia = 6.0
tab_overlap = 0.5

# Base outer solid
outer = cq.Workplane("XY").circle(outer_radius).extrude(length)
inner = cq.Workplane("XY").circle(inner_radius).extrude(length)
result = outer.cut(inner)

# Cooling labyrinth: through‑wall holes on the +X side (use cylinders cut from a tangent workplane)
hole_spacing_z = length / (num_holes_z + 1)
hole_spacing_y = (inner_radius * 2 - 2 * wall_thickness) / (num_holes_y + 1)
for i in range(1, num_holes_z + 1):
    z_pos = i * hole_spacing_z - length / 2
    for j in range(1, num_holes_y + 1):
        y_pos = -inner_radius + wall_thickness + j * hole_spacing_y - (hole_spacing_y / 2)
        hole = (
            cq.Workplane("YZ", origin=(outer_radius, 0, 0))
            .center(y_pos, z_pos)
            .circle(cooling_hole_dia / 2)
            .extrude(wall_thickness + 0.5)
        )
        result = result.cut(hole)

# Tab on the +X side created via a YZ workplane slightly overlapping the housing
tab = (
    cq.Workplane("YZ", origin=(outer_radius - tab_overlap, 0, 0))
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
)
# Clearance hole through the tab (planar front face)
tab = tab.faces(">X").workplane().center(0, 0).hole(tab_hole_dia)
result = result.union(tab)

# Fillet bottom outer edge
result = result.faces("<Z").edges().fillet(bottom_fillet_radius)
