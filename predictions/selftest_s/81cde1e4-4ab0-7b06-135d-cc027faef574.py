import cadquery as cq

# Parameters
knob_total_width = 80.0
knob_base_height = 30.0
knob_base_thickness = 6.0
central_boss_radius = 12.0
central_boss_height = 8.0
vent_slot_width = 5.0
vent_slot_height = 20.0
vent_slot_offset = 20.0
wall_fillet_radius = 2.0
edge_chamfer = 0.5
mount_hole_diameter = 6.0
rib_thickness = 1.5
rib_height = 4.0
rib_spacing = 15.0

# Helper to get the first solid for chained operations
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base knob body
knob = (
    cq.Workplane('XY')
    .rect(knob_total_width, knob_base_height)
    .extrude(knob_base_thickness)
    # Tag the top workplane for further features
    .faces('>Z')
    .workplane()
    .tag('top_face')
    # Fillet base vertical edges
    .firstSolid()
    .edges('|Z')
    .fillet(wall_fillet_radius)
    # Chamfer the top edges for safety
    .firstSolid()
    .edges('>Z')
    .chamfer(edge_chamfer)
)

# Central boss on top of the knob
knob = (
    knob
    .workplaneFromTagged('top_face')
    .center(0, 0)
    .circle(central_boss_radius)
    .extrude(central_boss_height)
)

# Side vent slots cut through the body (both sides)
knob = (
    knob
    .workplaneFromTagged('top_face')
    .center(-knob_total_width/2 + vent_slot_offset, 0)
    .rect(vent_slot_width, vent_slot_height)
    .cutBlind(-knob_base_thickness - central_boss_height)
    .workplaneFromTagged('top_face')
    .center(knob_total_width/2 - vent_slot_offset, 0)
    .rect(vent_slot_width, vent_slot_height)
    .cutBlind(-knob_base_thickness - central_boss_height)
)

# Mounting hole through central boss
knob = (
    knob
    .workplaneFromTagged('top_face')
    .center(0, 0)
    .circle(mount_hole_diameter/2)
    .cutThruAll()
)

# Internal ribs for stiffness, placed on the base side walls
rib_count = int((knob_total_width - 2 * rib_spacing) // rib_spacing)
for i in range(rib_count):
    x_pos = -knob_total_width/2 + rib_spacing + i * rib_spacing
    knob = (
        knob
        .workplaneFromTagged('top_face')
        .center(x_pos, 0)
        .rect(rib_thickness, rib_height)
        .extrude(-knob_base_thickness)
    )

result = knob