import cadquery as cq

# Parameters
cap_outer_diameter = 80.0
cap_total_height = 15.0
cap_thickness = 10.0
flange_thickness = 5.0
flange_outer_diameter = 70.0
flange_inner_diameter = 60.0
hole_diameter = 5.0
hole_depth = 8.0
chamfer_size = 1.0
boss_radius = 8.0
boss_height = 4.0
slot_width = 12.0
slot_depth = 4.0

# Derived dimensions
R_outer = cap_outer_diameter / 2.0
R_flange_outer = flange_outer_diameter / 2.0
R_flange_inner = flange_inner_diameter / 2.0

# Outer cylinder (main body)
outer_cyl = cq.Workplane("XY").circle(R_outer).extrude(cap_total_height)

# Internal flange ring (at bottom)
inner_flange = cq.Workplane("XY").circle(R_flange_outer).extrude(flange_thickness)

# Combine body and flange
combined = outer_cyl.union(inner_flange)

# Cavity cutter (creates hollow interior up to cap_thickness)
cavity_cutter = cq.Workplane("XY").circle(R_flange_inner).extrude(cap_thickness)
part = combined.cut(cavity_cutter)

# Central boss on exterior (protrudes from top)
part = part.faces(">Z").workplane().circle(boss_radius).extrude(boss_height)

# Top slot cut (centered on top face)
part = part.faces(">Z").workplane().rect(slot_width, slot_depth).cutBlind(slot_depth)

# Blind holes on internal flange top (plane offset from top face)
hole_plane = part.faces(">Z").workplane(offset=-cap_thickness)
hole_radius = (R_flange_inner + R_flange_outer) / 2.0
part = (
    hole_plane
    .polarArray(radius=hole_radius, count=3, angle=360, startAngle=0)
    .hole(hole_diameter, hole_depth)
)

# Chamfer outer lip and top edge for safety
part = part.edges(">Z").chamfer(chamfer_size)

result = part