import cadquery as cq
leg_length = 80.0
leg_width = 30.0
thickness = 10.0
wall_thickness = 2.0
chamfer_distance = 0.5
hole_diameter = 4.0
hole_spacing = 20.0
hole_offset = 15.0
rib_width = 6.0
rib_height = 3.0
rib_spacing = 12.0
rib_count = 4
rib_count = 2
base = cq.Workplane('XY').rect(leg_length, leg_width).extrude(thickness)
base = base.edges('|Z').chamfer(chamfer_distance)
hole_positions = [
    (hole_offset, leg_width/2 - wall_thickness/2),
    (hole_offset, leg_width/2 - wall_thickness/2),
    (leg_length - hole_offset, leg_width/2 - wall_thickness/2),
    (leg_length - hole_offset, leg_width/2 - wall_thickness/2),
    (leg_length - hole_offset, leg_width/2),
    (leg_length, leg_width/2),
    (leg_length, leg_width/2),
    (leg_width/2, leg_width/2),
    (leg_width/2, leg_width/2),
    (0, leg_width/2)
]
base = base.faces('>Z').workplane().pushPoints(hole_positions).hole(hole_diameter)
rib = cq.Workplane('XY').center(leg_width/2, leg_width/2).rect(rib_width, rib_height).extrude(rib_height)
result = base.union(rib)
