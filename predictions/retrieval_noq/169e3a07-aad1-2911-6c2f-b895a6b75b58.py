import cadquery as cq

# Parameters
cap_outer_diameter = 50.0
cap_height = 30.0
cap_thickness = 4.0
chamfer_size = 1.0
groove_depth = 2.0
groove_width = 3.0
bolt_hole_diameter = 5.0
rib_count = 4
rib_height = 12.0
rib_thickness = 2.0
rib_width = 6.0
mounting_hole_diameter = 4.0

# Base solid: outer cylinder
outer = cq.Workplane('XY').circle(cap_outer_diameter / 2).extrude(cap_height)
# Inner hollow
inner_diameter = cap_outer_diameter - 2 * cap_thickness
hollow = cq.Workplane('XY').circle(inner_diameter / 2).extrude(cap_height)
base = outer.cut(hollow)

# Recessed groove for gasket (cylindrical pocket inside)
groove_radius = (inner_diameter / 2) - (groove_width / 2)
groove_start_z = cap_height - 1.0 - groove_depth
groove = (
    cq.Workplane('XY')
    .circle(groove_radius)
    .extrude(groove_depth)
    .translate((0, 0, groove_start_z))
)
base = base.cut(groove)

# Chamfer on top outer edge
base = base.faces('>Z').edges().chamfer(chamfer_size)

# External ribs around circumference
rib = (
    cq.Workplane('XZ')
    .moveTo(cap_outer_diameter / 2 - rib_thickness / 2, 0)
    .rect(rib_thickness, rib_height)
    .extrude(rib_width)
)
rib = rib.translate((0, 0, (cap_height - rib_height) / 2))

ribs = cq.Workplane('XY')
for i in range(rib_count):
    angle = 360.0 / rib_count * i
    ribs = ribs.union(rib.rotate((0, 0, 0), (0, 0, 1), angle))
base = base.union(ribs)

# Mounting holes on opposite sides of the side wall
base = base.faces('>X').workplane().hole(mounting_hole_diameter)
base = base.faces('<X').workplane().hole(mounting_hole_diameter)

# Central bolt clearance through top
base = base.faces('>Z').workplane().hole(bolt_hole_diameter)

result = base