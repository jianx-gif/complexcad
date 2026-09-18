import cadquery as cq

# Parameters
base_width = 80.0
base_height = 30.0
base_thickness = 6.0
wall_thickness = 0.8
boss_diameter = 25.0
boss_height = 8.0
slot_width = 5.0
slot_length = 20.0
slot_offset = 20.0
chamfer_size = 0.5
fillet_radius = 2.0
central_hole_diameter = 6.0

# Helper to get the first solid for edge/face selections
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base block with fillet and chamfer
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
    .firstSolid()
    .edges("|Z")
    .fillet(fillet_radius)
    .firstSolid()
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

# Central boss on top of base
boss = (
    base
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# Central through hole for sliding rod
with_hole = (
    boss
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .circle(central_hole_diameter / 2)
    .cutBlind(- (base_thickness + boss_height))
)

# Side slots for sliding clearance
result = (
    with_hole
    .faces(">Z")
    .workplane()
    .center(-slot_offset, 0)
    .rect(slot_width, slot_length)
    .cutBlind(- (base_thickness + boss_height))
    .center(2 * slot_offset, 0)
    .rect(slot_width, slot_length)
    .cutBlind(- (base_thickness + boss_height))
)
