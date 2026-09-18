
import cadquery as cq

bracket_length = 80.0
bracket_width = 40.0
bracket_thickness = 8.0

tab_length = 15.0
tab_height = 20.0

slot_width = 8.0
slot_length = 30.0
slot_offset = 10.0

blind_hole_diameter = 6.0
blind_hole_depth = 4.0

mount_hole_diameter = 4.0
mount_hole_spacing = 30.0
mount_hole_offset = 12.0

chamfer_distance = 1.0
rib_thickness = 4.0
rib_height = 5.0
rib_offset = 5.0

csk_depth = 1.5
csk_angle = 82

# Base profile with tab
base = (
    cq.Workplane("XY")
    .polyline([
        (0, 0),
        (bracket_length, 0),
        (bracket_length, bracket_width),
        (bracket_length - tab_length, bracket_width),
        (bracket_length - tab_length, bracket_width - tab_height),
        (0, bracket_width - tab_height),
        (0, 0),
    ])
    .close()
    .extrude(bracket_thickness)
)

# Milled slot through the main plate (centered)
result = (
    base
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rect(slot_length, slot_width)
    .cutThruAll()
)

# Blind hole near interior corner of the tab
centroid_x = bracket_length / 2.0
centroid_y = (bracket_width - tab_height) / 2.0
hole_target_x = bracket_length - tab_length / 2.0
hole_target_y = bracket_width - tab_height / 2.0
hole_dx = hole_target_x - centroid_x
hole_dy = hole_target_y - centroid_y
result = (
    result
    .faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .center(hole_dx, hole_dy)
    .hole(blind_hole_diameter, blind_hole_depth)
)

# Chamfer all edges for safety and smooth interior corner
result = result.edges().chamfer(chamfer_distance)

# Mounting holes pattern on main plate (back face)
mh_center_y = (bracket_width - tab_height) / 2.0 - centroid_y
result = (
    result
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .center(-bracket_length / 2.0 + mount_hole_offset, mh_center_y)
    .rarray(mount_hole_spacing, 0, 2, 1)
    .hole(mount_hole_diameter)
)

# Countersink for mounting holes
result = (
    result
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .center(-bracket_length / 2.0 + mount_hole_offset, mh_center_y)
    .rarray(mount_hole_spacing, 0, 2, 1)
    .cskHole(mount_hole_diameter, csk_depth, csk_angle)
)

# Reinforcement rib on backside of main plate
rib_center_x = -bracket_length / 2.0 + rib_offset + rib_thickness / 2.0
rib_center_y = 0.0
result = (
    result
    .faces("<Z")
    .workplane(centerOption="CenterOfMass")
    .center(rib_center_x, rib_center_y)
    .rect(rib_height, rib_thickness)
    .extrude(rib_thickness)
)
