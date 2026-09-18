import cadquery as cq

class Measures:
    pass

m = Measures()
# Dimensions (max 100 units)
m.width = 60.0          # overall width of clip
m.thickness = 5.0       # material thickness
m.height = 30.0         # upright height
m.latch_radius = 8.0    # radius of rounded latch
m.hinge_gap = 2.0       # clearance gap at hinge side
m.spring_thick = 2.0    # thickness of spring tab slot
m.spring_len = 12.0     # length of spring slot
m.chamfer = 0.5         # chamfer size

# Base profile sketch
profile = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(m.width, 0)
    .lineTo(m.width, m.height)
    .lineTo(m.latch_radius, m.height)
    .threePointArc((0, m.height), (0, m.height - m.latch_radius))
    .lineTo(0, m.hinge_gap + m.spring_thick)
    .lineTo(m.hinge_gap, m.hinge_gap + m.spring_thick)
    .lineTo(m.hinge_gap, 0)
    .close()
)

solid = profile.extrude(m.thickness)

# Chamfer outer edges
solid = solid.edges("|Z").chamfer(m.chamfer)

# Rounded latch cut (through)
solid = solid.faces(">Z").workplane()
solid = solid.center(m.width/2, m.height - m.latch_radius)
solid = solid.hole(2*m.latch_radius, depth=m.thickness)

# Spring hinge slot (cut through)
solid = solid.faces(">Z").workplane()
solid = solid.center(m.hinge_gap/2, m.spring_thick/2)
solid = solid.rect(m.spring_len, m.spring_thick).cutBlind(-m.thickness)

result = solid