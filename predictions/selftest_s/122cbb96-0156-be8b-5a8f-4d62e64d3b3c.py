import cadquery as cq

# Parameters
base_width = 80.0
base_depth = 60.0
base_thickness = 12.0
base_corner_radius = 5.0
boss_diameter = 30.0
boss_height = 20.0
insert_hole_diameter = 6.0
insert_hole_depth = 15.0
groove_diameter = 24.0
groove_depth = 4.0
mount_hole_dia = 5.0
mount_hole_spacing_x = 60.0
mount_hole_spacing_y = 40.0

# Base plate with rounded corners
result = (
    cq.Workplane('XY')
    .rect(base_width, base_depth)
    .extrude(base_thickness)
    .edges('|Z')
    .fillet(base_corner_radius)
)

# Cylindrical boss on top of base
result = (
    result
    .faces('>Z')
    .workplane()
    .center(0, 0)
    .circle(boss_diameter/2)
    .extrude(boss_height)
)

# Mounting holes on base plate corners
result = (
    result
    .faces('>Z[-2]')
    .workplane()
    .pushPoints([(-mount_hole_spacing_x/2, -mount_hole_spacing_y/2),
                ( mount_hole_spacing_x/2, -mount_hole_spacing_y/2),
                (-mount_hole_spacing_x/2,  mount_hole_spacing_y/2),
                ( mount_hole_spacing_x/2,  mount_hole_spacing_y/2)])
    .circle(mount_hole_dia/2)
    .cutThruAll()
)

# Threaded insert blind hole in boss
result = (
    result
    .faces('>Z[1]')
    .workplane()
    .center(0, 0)
    .circle(insert_hole_diameter/2)
    .cutBlind(insert_hole_depth)
)

# Groove for clamp clip on top of boss (circular recess)
result = (
    result
    .faces('>Z[1]')
    .workplane()
    .center(0, 0)
    .circle(groove_diameter/2)
    .cutBlind(groove_depth)
)
