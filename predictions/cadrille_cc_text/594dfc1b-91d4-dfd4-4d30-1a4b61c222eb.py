import cadquery as cq
outer_diameter = 80.0
wall_thickness = 4.0
head_height = 20.0
port_width = 15.0
port_depth = 25.0
port_chamfer = 1.0
mount_hole_diameter = 6.0
mount_hole_distance = 30.0
rib_height = 10.0
rib_width = outer_diameter - 2 * wall_thickness
rib_depth = head_height - 2 * wall_thickness
rib_height = 10.0
base = cq.Workplane('XY').circle(outer_diameter / 2).extrude(head_height)
base = base.faces('>Z').workplane().circle(outer_diameter / 2).extrude(head_height)
base = base.faces('>Z').workplane().circle(port_width / 2).extrude(head_height)
base = base.faces('>Z').workplane().polarArray(radius=mount_hole_distance, count=mount_hole_distance, startAngle=0, angle=360).hole(mount_hole_diameter)
rib = cq.Workplane('XY').circle(outer_diameter / 2).extrude(rib_height)
rib = rib.translate((0, 0, head_height - rib_height))
rib = rib.translate((0, 0, head_height - rib_height))
rib = rib.translate((0, 0, head_height - rib_height))
result = base.union(rib)
result = result.faces('>Z').workplane().circle(port_width / 2).circle(port_depth / 2).extrude(port_height + 0.1)
result = result.faces('>Z').workplane().polarArray(radius=mount_hole_distance, count=mount_hole_distance, startAngle=0, angle=360).hole(mount_hole_diameter)
result = result.faces('>Z').workplane().polarArray(radius=mount_hole_distance, count=mount_hole_distance, startAngle=0, angle=360).hole(mount_hole_diameter)
