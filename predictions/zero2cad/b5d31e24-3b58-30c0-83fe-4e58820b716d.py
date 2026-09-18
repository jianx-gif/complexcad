import cadquery as cq

# Parameters
arm_length = 40.0
arm_width = 15.0
arm_thickness = 10.0
central_width = 25.0
central_thickness = 12.0
rib_width = 5.0
rib_height = 4.0
rib_spacing = 12.0
hole_diameter = 5.0
hole_depth = 8.0
hole_offset = 12.0
chamfer_size = 0.8

# Central block
central = cq.Workplane('XY').box(central_width, central_width, central_thickness)

# Arms
arm_x_pos = cq.Workplane('XY').box(arm_length, arm_width, arm_thickness).translate((central_width/2 + arm_length/2, 0, 0))
arm_x_neg = cq.Workplane('XY').box(arm_length, arm_width, arm_thickness).translate((-central_width/2 - arm_length/2, 0, 0))
arm_y_pos = cq.Workplane('XY').box(arm_width, arm_length, arm_thickness).translate((0, central_width/2 + arm_length/2, 0))
arm_y_neg = cq.Workplane('XY').box(arm_width, arm_length, arm_thickness).translate((0, -central_width/2 - arm_length/2, 0))

# Combine base cross
base = central.union(arm_x_pos).union(arm_x_neg).union(arm_y_pos).union(arm_y_neg)

# Chamfer outer vertical edges
base = base.edges('|Z').chamfer(chamfer_size)

# Rib pattern on top face
rib_count = int((arm_length - rib_spacing) // rib_spacing) + 1
rib_positions = [central_width/2 + rib_spacing/2 + i * rib_spacing for i in range(rib_count)]

ribs = cq.Workplane('XY')
for x in rib_positions:
    ribs = ribs.union(
        cq.Workplane('XY')
        .box(rib_width, arm_width, rib_height)
        .translate((x, 0, arm_thickness/2 + rib_height/2))
    )
for y in rib_positions:
    ribs = ribs.union(
        cq.Workplane('XY')
        .box(arm_width, rib_width, rib_height)
        .translate((0, y, arm_thickness/2 + rib_height/2))
    )

# Combine ribs with base
result = base.union(ribs)

# Blind holes on each arm
hole_positions = [
    (central_width/2 + hole_offset, 0),
    (-central_width/2 - hole_offset, 0),
    (0, central_width/2 + hole_offset),
    (0, -central_width/2 - hole_offset)
]
result = result.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter, depth=hole_depth)
