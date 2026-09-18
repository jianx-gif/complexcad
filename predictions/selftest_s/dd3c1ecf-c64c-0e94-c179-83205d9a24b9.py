import cadquery as cq

plate_width = 80.0
plate_height = 60.0
plate_thickness = 5.0
vent_size = 30.0
vent_margin = 5.0
hole_diameter = 5.0
countersink_diameter = 9.0
countersink_angle = 90.0
chamfer_dist = 1.0
rib_width = 6.0
rib_thickness = 2.0
rib_spacing = 20.0
rib_margin = 8.0

base = cq.Workplane("XY").rect(plate_width, plate_height).extrude(plate_thickness)

# central square vent
with_vent = base.faces('>Z').workplane().rect(vent_size, vent_size).cutBlind(-plate_thickness)

# countersunk holes pattern
hole_positions = [
    (-plate_width/2 + vent_margin + hole_diameter/2, 0),
    (plate_width/2 - vent_margin - hole_diameter/2, 0),
    (0, plate_height/2 - vent_margin - hole_diameter/2)
]
with_holes = with_vent.faces('>Z').workplane().pushPoints(hole_positions).cskHole(
    hole_diameter, countersink_diameter, countersink_angle, plate_thickness
)

# add stiffening ribs on the back side
back_wp = with_holes.faces('<Z').workplane()
rib_solid = cq.Workplane('XY')
num_ribs = int((plate_width - 2 * rib_margin) // (rib_width + rib_spacing))
for i in range(num_ribs):
    x_center = -plate_width/2 + rib_margin + i * (rib_width + rib_spacing) + rib_width/2
    rib = back_wp.center(x_center, 0).rect(rib_width, plate_height - 2 * rib_margin).extrude(rib_thickness)
    rib_solid = rib_solid.union(rib)

result = with_holes.union(rib_solid)
result = result.edges('|Z').chamfer(chamfer_dist)
