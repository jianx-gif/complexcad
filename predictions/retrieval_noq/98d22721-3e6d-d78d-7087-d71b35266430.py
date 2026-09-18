import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 50.0
plate_thickness = 8.0
latch_hole_diameter = 6.0
tab_length = 12.0
tab_height = 10.0
rib_width = 6.0
rib_length = 30.0
rib_height = 4.0
rib_spacing = 20.0
ejector_depth = 6.0
ejector_draft_angle = 5.0
chamfer_distance = 0.5

base_profile = (
    cq.Workplane("XY")
    .moveTo(-plate_length/2, -plate_width/2)
    .lineTo(plate_length/2, -plate_width/2)
    .lineTo(plate_length/2, plate_width/2 - tab_height/2)
    .lineTo(plate_length/2 + tab_length, plate_width/2 - tab_height/2)
    .lineTo(plate_length/2 + tab_length, plate_width/2 + tab_height/2)
    .lineTo(plate_length/2, plate_width/2 + tab_height/2)
    .lineTo(plate_length/2, plate_width/2)
    .lineTo(-plate_length/2, plate_width/2)
    .close()
)

plate = base_profile.extrude(plate_thickness)

plate = (
    plate
    .faces(">Z")
    .workplane()
    .hole(latch_hole_diameter)
)

rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_length)
    .extrude(rib_height)
)

rib1 = rib.translate((0, -rib_spacing/2, plate_thickness/2 + rib_height/2))
rib2 = rib.translate((0, rib_spacing/2, plate_thickness/2 + rib_height/2))
plate = plate.union(rib1).union(rib2)

cavity = (
    cq.Workplane("XY", origin=(0, 0, 0))
    .rect(latch_hole_diameter*1.5, latch_hole_diameter*1.5)
    .extrude(ejector_depth, taper=ejector_draft_angle)
)
plate = plate.cut(cavity)

plate = plate.edges().chamfer(chamfer_distance)

result = plate