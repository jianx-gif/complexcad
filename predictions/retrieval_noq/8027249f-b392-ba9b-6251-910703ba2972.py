import cadquery as cq
bracket_length = 70
bracket_width = 30
bracket_thickness = 8
rib_width = 2
rib_height = 4
rib_spacing = 4
margin = 4
hole_diameter = 4
counterbore_diameter = 6
counterbore_depth = 4
set_screw_offset = 5
mount_hole_diameter = 3
mount_hole_offset = 10
chamfer_distance = 0.5
num_ribs = int((bracket_width - 2 * margin) // (rib_width + rib_spacing))
base = cq.Workplane("XY").rect(bracket_length, bracket_width).extrude(bracket_thickness).edges().chamfer(chamfer_distance)
result = base
rib_length = bracket_length - 2 * margin
rib_base = cq.Workplane("XY").workplane(offset=bracket_thickness).center(0,0).rect(rib_width, rib_length).extrude(rib_height)
start = -bracket_width/2 + margin + rib_width/2
rib_positions = [(0, start + i * (rib_width + rib_spacing)) for i in range(num_ribs)]
for pos in rib_positions:
    result = result.union(rib_base.translate((pos[0], pos[1], 0)))
set_screw_center_x = bracket_length/2 - set_screw_offset
result = result.faces(">Z").workplane().cboreHole(hole_diameter, counterbore_diameter, counterbore_depth)
for direction in ["<X", ">X"]:
    result = result.faces(direction).workplane(centerOption="CenterOfMass").pushPoints([(0, mount_hole_offset), (0, -mount_hole_offset)]).hole(mount_hole_diameter)
