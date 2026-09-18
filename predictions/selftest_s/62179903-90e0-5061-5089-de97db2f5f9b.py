import cadquery as cq

# Parameters
knob_diameter = 60.0
knob_height = 30.0
wall_thickness = 2.0
groove_width = 8.0
groove_depth = 3.0
central_hole_diameter = 12.0
chamfer_distance = 1.0
tab_width = 20.0
tab_length = 10.0
tab_thickness = 4.0

# Extend Workplane with firstSolid helper
def firstSolid(self):
    return self.newObject([self.findSolid()])

cq.Workplane.firstSolid = firstSolid

# Base knob cylinder
base = (
    cq.Workplane("XY")
    .circle(knob_diameter / 2)
    .extrude(knob_height)
)

# Top chamfer
base = base.faces(">Z").chamfer(chamfer_distance)

# Central blind hole
blind_depth = knob_height - 2 * wall_thickness
base = (
    base.faces(">Z")
    .workplane()
    .circle(central_hole_diameter / 2)
    .cutBlind(blind_depth)
)

# Groove profile (wire) on XZ plane – rectangular with rounded ends via fillet on wire edges
profile_wire = (
    cq.Workplane("XZ")
    .center(groove_width / 2, 0)
    .rect(groove_width, groove_depth)
    .wire()
)

# Circular sweep path coaxial with knob
path_wire = (
    cq.Workplane("XY")
    .circle(knob_diameter / 2 - groove_depth / 2)
    .wire()
)

groove_cut = profile_wire.sweep(path_wire, makeSolid=True)

# Subtract groove from base
base = base.cut(groove_cut)

# Attachment tab on side
tab = (
    cq.Workplane("XY")
    .center(0, knob_diameter / 2 + tab_thickness / 2)
    .rect(tab_width, tab_length)
    .extrude(tab_thickness)
)

result = base.union(tab)
