import cadquery as cq

outer_diameter = 80.0
wall_thickness = 2.0
height = 30.0
rib_thickness = 1.5
rib_height = 10.0
rib_count = 6
vent_hole_diameter = 4.0
vent_rows = 4
vent_cols = 5
vent_spacing = 12.0
chamfer_size = 0.5

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = cq.Workplane('XY').circle(outer_radius).extrude(height)
shell = base.shell(-wall_thickness)

rib = (
    cq.Workplane('XY')
    .center(inner_radius - rib_thickness / 2.0, 0)
    .rect(rib_thickness, rib_height)
    .extrude(height)
)

ribs = rib
for i in range(1, rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))

with_ribs = shell.union(ribs)

vent_points = []
start_x = -((vent_cols - 1) * vent_spacing) / 2.0
start_y = -((vent_rows - 1) * vent_spacing) / 2.0
for i in range(vent_cols):
    for j in range(vent_rows):
        x = start_x + i * vent_spacing
        y = start_y + j * vent_spacing
        if (x**2 + y**2) < (inner_radius - vent_hole_diameter) ** 2:
            vent_points.append((x, y))

vented = (
    with_ribs.faces('>Z')
    .workplane()
    .pushPoints(vent_points)
    .hole(vent_hole_diameter, depth=wall_thickness + 0.2)
)

result = vented.edges('>Z').chamfer(chamfer_size)
