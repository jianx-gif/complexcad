import cadquery as cq

# Parameters
rail_length = 80.0
rail_width = 30.0
rail_height = 20.0
wall_thickness = 4.0
bearing_diameter = 12.0
bearing_depth = 6.0
bearing_spacing = 20.0
num_bearings = 3
chamfer_size = 1.0
mount_hole_dia = 5.0
mount_hole_spacing = 40.0
rib_width = 6.0
rib_height = 4.0
rib_spacing = 15.0

# Base solid: outer block
outer = cq.Workplane('XY').rect(rail_width, rail_height).extrude(rail_length)
# Inner cavity to create wall thickness
inner = cq.Workplane('XY').rect(rail_width - 2*wall_thickness, rail_height - 2*wall_thickness).extrude(rail_length)
base = outer.cut(inner)

# Bearing seats on +X side
bearing_face = base.faces('>X')
bearing_wp = bearing_face.workplane(centerOption='CenterOfMass')
# Create array of bearing seats along length
bearing_pattern = bearing_wp.rarray(bearing_spacing, 0, num_bearings, 1)
# Cut bearing seats (cylindrical pockets)
base = bearing_pattern.circle(bearing_diameter/2).cutBlind(-bearing_depth)

# Mounting holes on top (+Z) face
mount_face = base.faces('>Z')
mount_wp = mount_face.workplane(centerOption='CenterOfMass')
mount_pattern = mount_wp.rarray(mount_hole_spacing, 0, 2, 1)
base = mount_pattern.hole(mount_hole_dia)

# Ribs on top surface for stiffness
rib_face = base.faces('>Z')
rib_wp = rib_face.workplane(centerOption='CenterOfMass')
rib_pattern = rib_wp.rarray(rib_spacing, 0, int(rail_length/rib_spacing), 1)
# Create ribs as rectangular protrusions
ribs = rib_pattern.rect(rib_width, rib_height).extrude(wall_thickness)
base = base.union(ribs)

# Chamfer on the far end (+Z face) edges
result = base.faces('>Z').edges().chamfer(chamfer_size)
