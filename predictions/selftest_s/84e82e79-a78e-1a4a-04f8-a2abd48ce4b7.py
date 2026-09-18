import cadquery as cq
cover_diameter = 80
cover_thickness = 5
flange_overhang = 6
flange_height = 8
clearance_hole_diameter = 20
mount_hole_diameter = 4
mount_hole_count = 6
mount_hole_radius = cover_diameter/2 + flange_overhang/2
chamfer_size = 0.5
rib_width = 8
rib_length = cover_diameter/2 - 12
rib_thickness = 2
base = cq.Workplane('XY').circle(cover_diameter/2).extrude(cover_thickness)
flange = base.faces('>Z').workplane().circle(cover_diameter/2 + flange_overhang).extrude(flange_height)
result = base.union(flange)
result = result.edges('>Z').chamfer(chamfer_size)
result = result.faces('<Z').workplane().hole(clearance_hole_diameter)
result = result.faces('>Z').workplane().polarArray(count=mount_hole_count, radius=mount_hole_radius, startAngle=0, angle=360).hole(mount_hole_diameter)
ribs = result.faces('<Z').workplane().rect(rib_width, rib_length).extrude(rib_thickness)
ribs = ribs.union(ribs.rotate((0,0,0),(0,0,1),90))
result = result.union(ribs)
result = result.edges().fillet(0.5)
