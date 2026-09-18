import cadquery as cq

# Primary dimensions
body_radius = 45.0
body_height = 70.0
wall_thickness = 3.0
boss_radius = 15.0
boss_height = 12.0
boss_overlap = 1.0
keyway_width = 6.0
keyway_depth = 8.0
mount_hole_diameter = 4.0
mount_hole_spacing = 20.0
chamfer_distance = 1.0
vent_hole_diameter = 2.0
vent_rows = 3
vent_cols = 5
vent_pitch = 12.0
pocket_width = 8.0
pocket_height = 30.0
pocket_depth = wall_thickness + 0.5
counterbore_diameter = 10.0
counterbore_depth = 3.0

# Base thin-walled cylinder
base = cq.Workplane('XY').cylinder(body_height, body_radius)
thin_shell = base.shell(wall_thickness)

# Integrated boss extruded from top face with slight penetration for merging
assembly = (thin_shell
            .faces('>Z')
            .workplane()
            .circle(boss_radius)
            .extrude(boss_height + boss_overlap))

# Keyway slot in boss top surface
assembly = (assembly
            .faces('>Z')
            .workplane()
            .center(boss_radius - keyway_width/2, 0)
            .rect(keyway_width, keyway_depth)
            .cutBlind(-keyway_depth))

# Counterbore at keyway center
assembly = (assembly
            .faces('>Z')
            .workplane()
            .center(boss_radius - keyway_width/2, 0)
            .circle(counterbore_diameter/2)
            .cutBlind(-counterbore_depth))

# Mounting hole matrix on top surface
assembly = (assembly
            .faces('>Z')
            .workplane()
            .rarray(mount_hole_spacing, mount_hole_spacing, 2, 2)
            .hole(mount_hole_diameter))

# Vent holes on bottom face (grid pattern)
assembly = (assembly
            .faces('<Z')
            .workplane()
            .rarray(vent_pitch, vent_pitch, vent_cols, vent_rows)
            .hole(vent_hole_diameter))

# Chamfer on all outer vertical edges
assembly = assembly.edges('|Z').chamfer(chamfer_distance)

# Rectangular pocket cut into top region for internal stiffening
assembly = (assembly
            .faces('>Z')
            .workplane()
            .center(0, 0)
            .rect(pocket_width, pocket_height)
            .cutBlind(-pocket_depth))

result = assembly