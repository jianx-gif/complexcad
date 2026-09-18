import cadquery as cq

# Parameters
total_plate_width = 80.0
total_plate_depth = 60.0
plate_thickness = 5.0
gusset_thickness = 10.0
gusset_height = 30.0
tslot_bar_width = 12.0
tslot_leg_width = 4.0
tslot_leg_height = 8.0
hole_spacing_x = 30.0
hole_spacing_y = 20.0
hole_rows = 4
hole_columns = 2
hole_clearance_diameter = 4.5
edge_chamfer = 0.8

# Base rectangular plate
base_rectangle = (
    cq.Workplane('XY')
    .rect(total_plate_width, total_plate_depth)
    .extrude(plate_thickness)
)

# Gusset triangle attached to left side
gusset_triangle = (
    cq.Workplane('XY')
    .polyline([
        (-total_plate_width/2, total_plate_depth/2),
        (-total_plate_width/2 - gusset_thickness, total_plate_depth/2 - gusset_height/2),
        (-total_plate_width/2, total_plate_depth/2 - gusset_height),
    ])
    .close()
    .wire()
    .extrude(plate_thickness)
)

# Combine base plate and gusset
plate_with_gusset = base_rectangle.union(gusset_triangle)

# T‑slot profile points (centered on origin)
half_bar = tslot_bar_width / 2.0
half_leg = tslot_leg_width / 2.0
half_leg_height = tslot_leg_height / 2.0

ts_profile = [
    (-half_bar, half_leg),
    (-half_leg, half_leg),
    (-half_leg, -half_leg_height),
    ( half_leg, -half_leg_height),
    ( half_leg, half_leg),
    ( half_bar, half_leg),
    ( half_bar, -half_leg),
    (-half_bar, -half_leg),
]

# Cut T‑slot through the top face using composite sketch
plate_with_tslot = (
    plate_with_gusset
    .faces('>Z')
    .workplane()
    .polyline(ts_profile)
    .close()
    .cutBlind(plate_thickness)
)

# Drill clearance holes in a grid pattern on the top surface
plate_with_holes = (
    plate_with_tslot
    .faces('>Z')
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_columns, hole_rows, center=True)
    .hole(hole_clearance_diameter)
)

# Apply chamfer to all vertical edges
result = (
    plate_with_holes
    .edges('|Z')
    .chamfer(edge_chamfer)
)
