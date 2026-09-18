import cadquery as cq

# Parameters
max_dimension = 100.0
total_length = 70.0  # length of conical nose
base_diameter = 60.0
tip_diameter = 20.0
hub_diameter = 40.0
hub_length = 15.0
draft_angle_deg = 3.0
shaft_diameter = 10.0
mounting_hole_diameter = 6.0
mounting_hole_count = 4
mounting_hole_offset = 5.0
rib_count = 6
rib_thickness = 2.0
rib_height = 5.0
rib_length = 30.0
vent_slot_width = 3.0
vent_slot_length = 30.0
chamfer_size = 0.5

# Derived dimensions
import math
draft_angle_rad = math.radians(draft_angle_deg)
base_radius = base_diameter / 2.0
tip_radius = base_radius - total_length * math.tan(draft_angle_rad)
if tip_radius < 0:
    tip_radius = 0.1
hub_radius = hub_diameter / 2.0

# Hub cylinder
hub = (
    cq.Workplane("XY")
    .circle(hub_radius)
    .extrude(hub_length)
)

# Conical nose created by revolving a profile sketch on XZ plane
cone_profile = (
    cq.Workplane("XZ")
    .lineTo(base_radius, 0)
    .lineTo(tip_radius, total_length)
    .lineTo(0, total_length)
    .close()
    .revolve()
)
# Position cone on top of hub
cone = cone_profile.translate((0, 0, hub_length))

# Combine hub and cone
part = hub.union(cone)

# Central shaft bore through entire part
part = part.faces("<Z").workplane().hole(shaft_diameter)

# Mounting holes on hub cylindrical surface
mounting_face = part.faces("<Z").workplane().center(hub_radius - mounting_hole_offset, 0)
part = mounting_face.polarArray(hub_radius - mounting_hole_offset, 0, 360, mounting_hole_count).hole(mounting_hole_diameter)

# External ribs distributed around circumference on cone surface
rib = (
    cq.Workplane("XY")
    .rect(rib_thickness, rib_height)
    .extrude(rib_length)
)
# Position first rib at base of cone
rib = rib.translate((base_radius - rib_thickness/2, 0, hub_length + rib_height/2))
# Create pattern of ribs around axis
ribs = rib.rotate((0,0,0), (0,0,1), 0)
for i in range(1, rib_count):
    angle = i * 360.0 / rib_count
    ribs = ribs.union(rib.rotate((0,0,0), (0,0,1), angle))
part = part.union(ribs)

# Vent slots cut through outer surface of cone
slot = (
    cq.Workplane("YZ")
    .rect(vent_slot_width, vent_slot_length)
    .extrude(base_radius*2)
)
slot = slot.translate((base_radius, 0, hub_length + total_length/2))
slot = slot.rotate((0,0,0), (0,0,1), 90)
part = part.cut(slot)

# Chamfer tip edge
part = part.edges(">Z").chamfer(chamfer_size)

result = part