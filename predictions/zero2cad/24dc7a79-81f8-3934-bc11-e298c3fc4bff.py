import cadquery as cq

bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 4.0
mount_hole_diameter = 5.0
mount_hole_clearance = 6.0
mount_hole_cbore_diameter = 8.0
mount_hole_cbore_depth = 2.0
mount_hole_spacing = 60.0
mount_hole_offset_y = 10.0
rib_width = 6.0
rib_height = 2.0
rib_spacing = 20.0
rib_count = 2
gusset_height = 20.0
gusset_thickness = 3.0
chamfer_distance = 0.5

# Base plate
result = cq.Workplane("XY").box(bracket_length, bracket_width, bracket_thickness)

# Mounting holes on top face
result = (
    result.faces(">Z").workplane()
    .pushPoints([(-mount_hole_spacing/2, mount_hole_offset_y), (mount_hole_spacing/2, mount_hole_offset_y)])
    .cboreHole(mount_hole_clearance, mount_hole_cbore_diameter, mount_hole_cbore_depth)
)

# Ribs on top face
rib_start = -bracket_length/2 + rib_spacing
rib_positions = [rib_start + i * rib_spacing for i in range(rib_count)]
result = (
    result.faces(">Z").workplane()
    .pushPoints([(x, 0) for x in rib_positions])
    .rect(rib_width, bracket_width - 10)
    .extrude(rib_height)
)

# Gusset on +X side
result = (
    result.faces(">X").workplane(centerOption='CenterOfBoundBox')
    .move(0, -bracket_thickness/2)
    .line(gusset_thickness/2, 0)
    .line(0, gusset_height)
    .close()
    .extrude(gusset_thickness)
)

# Gusset on -X side
result = (
    result.faces("<X").workplane(centerOption='CenterOfBoundBox')
    .move(0, -bracket_thickness/2)
    .line(-gusset_thickness/2, 0)
    .line(0, gusset_height)
    .close()
    .extrude(gusset_thickness)
)

# Chamfer outer edges of gussets
result = result.edges("(>X or <X) and >Z").chamfer(chamfer_distance)
