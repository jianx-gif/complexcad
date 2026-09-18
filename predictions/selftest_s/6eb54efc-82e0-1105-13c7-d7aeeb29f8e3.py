import cadquery as cq

# Parameters
base_length = 80.0
base_width = 40.0
base_thickness = 8.0
slot_length = 40.0
slot_width = 10.0
hole_diameter = 6.0
hole_depth = 4.0
hole_spacing = 15.0
hole_center_offset_y = -base_width/2 + 12.0
mount_hole_dia = 8.0
mount_hole_offset_x = base_length/2 - 12.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 20.0
chamfer_distance = 1.0

# Base plate
result = (
    cq.Workplane('XY')
    .rect(base_length, base_width)
    .extrude(base_thickness)
)

# Side slot cut on -Y face
result = (
    result.faces('<<Y')
    .workplane(origin=(0,0,base_thickness/2))
    .rect(slot_length, slot_width)
    .cutBlind(-base_thickness)
)

# Through mounting holes on top face
result = (
    result.faces('>Z')
    .workplane()
    .center(mount_hole_offset_x, 0)
    .hole(mount_hole_dia)
    .center(-mount_hole_offset_x*2, 0)
    .hole(mount_hole_dia)
)

# Blind holes pattern on +Y face (inner side of slot)
result = (
    result.faces('>Y')
    .workplane(origin=(0,0,base_thickness/2))
    .center(-slot_length/2 + 8.0, hole_center_offset_y)
    .rarray(0, hole_spacing, 3, 1)
    .hole(hole_diameter, depth=hole_depth)
)

# Internal stiffening ribs cut into top surface
rib_positions = [-base_length/2 + rib_spacing, 0, base_length/2 - rib_spacing]
for x in rib_positions:
    result = (
        result.faces('>Z')
        .workplane()
        .center(x, 0)
        .rect(rib_width, base_width)
        .cutBlind(-rib_height)
    )

# Chamfer all outer edges
result = result.edges().chamfer(chamfer_distance)
