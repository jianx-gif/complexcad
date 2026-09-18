import cadquery as cq

flange_length = 80.0
flange_width = 60.0
flange_thickness = 8.0
lip_thickness = 4.0
lip_height = 4.0
chamfer_distance = 2.0
countersink_hole_diameter = 4.0
countersink_diameter = 8.0
countersink_angle = 82.0
hole_spacing_x = 30.0
hole_spacing_y = 20.0
hole_columns = 3
hole_rows = 2
rib_width = 5.0
rib_height = 3.0
fillet_radius = 1.0

base = cq.Workplane("XY").rect(flange_length, flange_width).extrude(flange_thickness)

lip = (cq.Workplane("XY")
    .rect(flange_length + 2*lip_thickness, flange_width + 2*lip_thickness)
    .extrude(lip_height)
    .translate((0, 0, flange_thickness)))

result = base.union(lip)

result = result.edges("|Z").chamfer(chamfer_distance)

# Countersunk hole pattern on top surface
hole_plane = result.faces(">Z").workplane()
hole_positions = hole_plane.rect(
    (hole_columns - 1) * hole_spacing_x,
    (hole_rows - 1) * hole_spacing_y,
    forConstruction=True).vertices()

result = hole_positions.cskHole(
    countersink_hole_diameter,
    countersink_diameter,
    countersink_angle,
    flange_thickness + lip_height)

# Stiffening ribs on bottom side, orthogonal layout
rib1 = (cq.Workplane("XY")
    .rect(flange_length - 10, rib_width)
    .extrude(rib_height)
    .translate((0, 0, rib_height/2)))

rib2 = rib1.rotate((0,0,0), (0,0,1), 90)

result = result.union(rib1).union(rib2)

# Internal fillet on inner vertical edges
result = result.edges("<<Z and (not |Z)").fillet(fillet_radius)

# Add mounting slots on one side
slot_length = 20.0
slot_width = 5.0
slot = (cq.Workplane("XY")
    .center(-flange_length/2 + lip_thickness/2, 0)
    .rect(slot_width, slot_length)
    .extrude(flange_thickness + lip_height)
    .translate((0,0,0)))

result = result.cut(slot)
