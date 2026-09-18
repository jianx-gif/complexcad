import cadquery as cq

leaf_length = 80.0
leaf_width = 30.0
leaf_thickness = 5.0
hinge_pin_diameter = 8.0
hinge_pin_offset = 12.0
slot_width = 6.0
slot_height = 8.0
rib_width = 6.0
rib_height = leaf_thickness
rib_offset = 10.0
tab_width = 20.0
tab_height = 8.0
set_screw_diameter = 3.0
set_screw_head_diameter = 6.0
set_screw_counterbore_depth = 3.0
chamfer_distance = 0.5

leaf_sketch = (
    cq.Sketch()
    .rect(leaf_length, leaf_width)
    .slot(slot_width, slot_height, mode='s')
)
leaf = (
    cq.Workplane("XY")
    .placeSketch(leaf_sketch)
    .extrude(leaf_thickness)
)
leaf = leaf.faces('>Z').workplane().center(leaf_length/2 - hinge_pin_offset, 0).hole(hinge_pin_diameter)
rib = (
    cq.Workplane("XY")
    .transformed(offset=(-leaf_length/2 + rib_offset, 0, -rib_height))
    .rect(rib_width, leaf_width)
    .extrude(rib_height)
)
part = leaf.union(rib)

tab = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, leaf_thickness))
    .rect(tab_width, leaf_width)
    .extrude(tab_height)
)
part = part.union(tab)

counterbore = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, leaf_thickness + tab_height - set_screw_counterbore_depth))
    .circle(set_screw_head_diameter/2)
    .extrude(set_screw_counterbore_depth)
)
shaft = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, 0))
    .circle(set_screw_diameter/2)
    .extrude(leaf_thickness + tab_height)
)
part = part.cut(counterbore).cut(shaft)
part = part.edges().chamfer(chamfer_distance)
result = part