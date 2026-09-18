import cadquery as cq
plate_major_radius = 45.0
plate_minor_radius = 30.0
plate_thickness = 8.0
rib_width = 3.0
rib_height = 2.0
rib_thickness = plate_thickness
pocket_radius = 12.0
pocket_depth = 6.0
insert_diameter = 5.0
insert_head_diameter = 9.0
insert_clearance = 1.0
insert_radius = plate_major_radius - 2.0
insert_clearance = 1.0
chamfer_size = 0.8
base = (
    cq.Workplane("XY")
    .circle(plate_major_radius)
    .extrude(plate_thickness)
)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, plate_thickness))
)
plate_with_rib = base.union(rib)
plate_with_hole = (
    plate_with_rib.faces(">Z")
    .workplane()
    .polarArray(radius=insert_radius, count=insert_head_diameter/2, startAngle=0, angle=360)
    .cskHole(insert_diameter, insert_head_diameter, insert_head_diameter, insert_head_diameter + 2)
)
plate_with_hole = (
    plate_with_hole.faces(">Z")
    .workplane()
    .pushPoints([(-plate_with_hole.offset, 0), (plate_with_hole.offset, 0)])
    .cskHole(insert_diameter, insert_head_diameter, insert_head_diameter + 2)
)
plate_with_rib = plate_with_hole.faces(">Z").edges().chamfer(chamfer_size)
result = plate_with_rib.faces(">Z").edges().chamfer(chamfer_size)
