import cadquery as cq

circle_diameter = 20.0
rect_width = 40.0
rect_height = 15.0
lever_length = 80.0
slot_width = 8.0
slot_length = 60.0
chamfer_dist = 2.0
mount_hole_diameter = 6.0
base_hole_diameter = 4.0
base_hole_spacing = 30.0
rib_height = 6.0

lever = (
    cq.Workplane("XY")
    .circle(circle_diameter/2)
    .workplane(offset=lever_length)
    .rect(rect_width, rect_height)
    .loft()
)

lever = lever.faces(">Z").workplane().hole(mount_hole_diameter)

side_offset = rect_width/2 - slot_width/2
slot_center_z = lever_length/2
slot_box = (
    cq.Workplane("XY")
    .box(slot_width, rect_height, slot_length)
    .translate((side_offset, 0, slot_center_z))
)

lever = lever.cut(slot_box)

lever = lever.faces(">Z").edges().chamfer(chamfer_dist)

lever = (
    lever.faces("<Z")
    .workplane()
    .pushPoints([(-base_hole_spacing/2, 0), (base_hole_spacing/2, 0)])
    .hole(base_hole_diameter)
)

rib_profile = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(0, rib_height)
    .lineTo(rib_height, 0)
    .close()
    .extrude(rect_height)
    .translate((-(rect_width/2 - rib_height), 0, lever_length*0.1))
)

lever = lever.union(rib_profile)

pocket_width = rect_width * 0.6
pocket_height = rect_height * 0.5
pocket_depth = lever_length * 0.2
pocket = (
    cq.Workplane("XY")
    .workplane(offset=lever_length*0.6)
    .rect(pocket_width, pocket_height)
    .extrude(-pocket_depth)
)

lever = lever.cut(pocket)

result = lever