import cadquery as cq

base_width = 70
base_height = 30
base_thickness = 8
wall_thickness = 0.4
fillet_radius = 2.5
chamfer_dist = 0.5
slot_width = 4
slot_height = 20
slot_depth = base_thickness
slot_count = 5
slot_spacing = (base_width - 2*wall_thickness - slot_count*slot_width) / (slot_count - 1)
axle_radius = 3
tab_width = 12
tab_height = 6
tab_thickness = 4

def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# generate slot positions centered on X axis
slot_positions = []
start_x = -base_width/2 + wall_thickness + slot_width/2
for i in range(slot_count):
    x = start_x + i * (slot_width + slot_spacing)
    slot_positions.append((x, 0))

result = (
    cq.Workplane("XZ")
    .rect(base_width, base_height)
    .extrude(base_thickness)
    # fillet vertical edges
    .firstSolid()
    .edges("|Y")
    .fillet(fillet_radius)
    # chamfer front face
    .firstSolid()
    .faces("<Y")
    .chamfer(chamfer_dist)
    # attachment tab on side
    .faces(">Y")
    .workplane()
    .center(-0.5 * base_width + 20, 0)
    .tag("attachment_workplane")
    .rect(tab_width, tab_height)
    .extrude(tab_thickness)
    # vent slots on top surface
    .faces(">Y")
    .workplane()
    .pushPoints(slot_positions)
    .rect(slot_width, slot_height)
    .cutBlind(-slot_depth)
    # central axle hole
    .faces(">Y")
    .workplane()
    .center(0, 0)
    .circle(axle_radius)
    .cutBlind(-base_thickness)
)
