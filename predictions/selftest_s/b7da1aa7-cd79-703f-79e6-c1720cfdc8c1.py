import cadquery as cq

plate_major_radius = 45.0
plate_minor_radius = 30.0
plate_thickness = 8.0
rib_width = 3.0
rib_height = 2.0
pocket_radius = 12.0
pocket_depth = 6.0
insert_count = 6
insert_circle_radius = 35.0
insert_diameter = 5.0
insert_head_diameter = 9.0
insert_countersink_angle = 90.0
chamfer_size = 0.8
rib_internal_width = 15.0
rib_internal_height = 3.0

base_plate = (
    cq.Workplane('XY')
    .ellipse(plate_major_radius, plate_minor_radius)
    .extrude(plate_thickness)
)

outer_rib = (
    cq.Workplane('XY')
    .ellipse(plate_major_radius - rib_width, plate_minor_radius - rib_width)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness - rib_height))
)

result = base_plate.union(outer_rib)

result = (
    result.faces('>Z')
    .workplane()
    .circle(pocket_radius)
    .cutBlind(-pocket_depth)
)

result = (
    result.faces('>Z')
    .workplane()
    .polarArray(insert_circle_radius, 0, 360, insert_count)
    .cskHole(insert_diameter, insert_head_diameter, insert_countersink_angle, plate_thickness + 1)
)

result = (
    result.faces('|Z')
    .chamfer(chamfer_size)
)

internal_rib1 = (
    cq.Workplane('XY')
    .rect(rib_internal_width, (plate_minor_radius - rib_width) * 2)
    .extrude(rib_internal_height)
)

internal_rib2 = internal_rib1.rotate((0, 0, 0), (0, 0, 1), 90)

result = result.union(internal_rib1).union(internal_rib2)
