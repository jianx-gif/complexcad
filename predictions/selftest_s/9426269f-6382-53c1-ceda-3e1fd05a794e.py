import cadquery as cq

panel_length = 90.0
panel_width = 60.0
panel_thickness = 4.0
slot_width = 2.0
slot_length = 70.0
slot_angle = 45.0
slot_spacing = 8.0
chamfer_size = 0.5
mount_hole_dia = 4.0
mount_hole_offset = 10.0
stiff_rib_width = 5.0
stiff_rib_spacing = 12.0
stiff_rib_depth = 2.0

base = cq.Workplane("XY").rect(panel_length, panel_width).extrude(panel_thickness)

num_slots = int((panel_width - slot_spacing) // slot_spacing)
result = base
for i in range(num_slots):
    y_off = -panel_width/2 + slot_spacing + i*slot_spacing
    result = (result.faces(">Z").workplane()
              .center(0, y_off)
              .rect(slot_width, slot_length)
              .rotate((0,0,0), (0,0,1), slot_angle)
              .cutBlind(-panel_thickness))

hole_positions = [
    (panel_length/2 - mount_hole_offset, panel_width/2 - mount_hole_offset),
    (-panel_length/2 + mount_hole_offset, panel_width/2 - mount_hole_offset),
    (-panel_length/2 + mount_hole_offset, -panel_width/2 + mount_hole_offset),
    (panel_length/2 - mount_hole_offset, -panel_width/2 + mount_hole_offset)
]
for x, y in hole_positions:
    result = (result.faces(">Z").workplane()
              .center(x, y)
              .hole(mount_hole_dia))

num_ribs = int((panel_length - 2*mount_hole_offset) // stiff_rib_spacing)
for i in range(num_ribs):
    x_off = -panel_length/2 + mount_hole_offset + i*stiff_rib_spacing
    result = (result.faces("<Z").workplane()
              .center(x_off, 0)
              .rect(stiff_rib_width, panel_width - 2*mount_hole_offset)
              .cutBlind(stiff_rib_depth))

result = result.edges("|Z").chamfer(chamfer_size)
