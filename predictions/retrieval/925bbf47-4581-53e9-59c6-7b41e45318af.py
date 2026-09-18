import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 60.0
plate_thickness = 5.0
bearing_shaft_radius = 10.0
groove_width = 3.0
groove_radius = bearing_shaft_radius + groove_width
groove_depth = 2.0
slot_length = 18.0
slot_width = 4.0
slot_center_offset = bearing_shaft_radius + 10.0
mount_hole_diameter = 5.0
mount_hole_offset = plate_length / 4.0
rib_height = 2.0
rib_width = 5.0
rib_penetration = 0.5
chamfer_dist = 0.8

# Base plate with central through hole (bearing shaft)
base_sketch = cq.Sketch().rect(plate_length, plate_width).circle(bearing_shaft_radius, mode='s')
result = cq.Workplane('XY').placeSketch(base_sketch).extrude(plate_thickness)

# Circular groove (partial depth) around bearing shaft
result = (
    result.faces('>Z')
    .workplane()
    .circle(groove_radius)
    .cutBlind(-groove_depth)
)

# Eight clearance slots positioned radially around the shaft
for i in range(8):
    result = (
        result.workplane()
        .center(slot_center_offset, 0)
        .rotate((0, 0, 0), (0, 0, 1), i * 45)
        .rect(slot_length, slot_width)
        .cutBlind(-plate_thickness)
    )

# Two mounting holes on opposite sides of the plate
result = (
    result.faces('>Z')
    .workplane()
    .center(-mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)
result = (
    result.faces('>Z')
    .workplane()
    .center(mount_hole_offset, 0)
    .hole(mount_hole_diameter)
)

# Side ribs for added stiffness (penetrating slightly into the plate)
rib_plus = (
    cq.Workplane('XY')
    .rect(rib_width, plate_length)
    .extrude(rib_height)
    .translate((0, plate_width/2 - rib_width + rib_penetration, 0))
)
rib_minus = (
    cq.Workplane('XY')
    .rect(rib_width, plate_length)
    .extrude(rib_height)
    .translate((0, -plate_width/2 + rib_penetration, 0))
)
result = result.union(rib_plus).union(rib_minus)

# Beveled (chamfered) outer edges for safety
result = result.edges('|Z').chamfer(chamfer_dist)
