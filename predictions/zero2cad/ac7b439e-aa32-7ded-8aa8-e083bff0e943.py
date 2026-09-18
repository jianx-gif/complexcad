import cadquery as cq

handle_length = 80.0
handle_width = 30.0
handle_height = 20.0
wall_thickness = 3.0
grip_radius = 12.0
grip_length = 15.0
fillet_radius = 2.0
rib_thickness = 2.0
rib_height = 15.0
rib_spacing = 10.0
rib_count = 3

base = cq.Workplane('XY').rect(handle_width, handle_height).extrude(handle_length)

grip = cq.Workplane('XY').center(0, 0).circle(grip_radius + wall_thickness).extrude(grip_length)
grip = grip.translate((0, 0, handle_length - grip_length))

solid = base.union(grip)

solid = solid.edges().fillet(fillet_radius)

hollow = solid.shell(wall_thickness)

rib = cq.Workplane('XY').rect(handle_width - 2 * wall_thickness, rib_thickness).extrude(rib_height)
rib = rib.translate((0, 0, handle_length - grip_length + rib_height / 2))

ribs = rib
for i in range(1, rib_count):
    offset = i * rib_spacing
    ribs = ribs.union(rib.translate((0, 0, offset)))

result = hollow.union(ribs)
