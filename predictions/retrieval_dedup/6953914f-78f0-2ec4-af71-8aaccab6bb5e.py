import cadquery as cq

# Parameters
cap_outer_radius = 30.0
cap_wall_thickness = 2.0
cap_inner_radius = cap_outer_radius - cap_wall_thickness
cap_length = 20.0
rib_thickness = 1.5
rib_length = 6.0
set_screw_diameter = 4.0
set_screw_depth = 12.0
set_screw_offset = cap_outer_radius - cap_wall_thickness - set_screw_diameter/2 - 2.0
chamfer_size = 0.5

# Base outer cylinder
outer = cq.Workplane('XY').circle(cap_outer_radius).extrude(cap_length)
# Inner cavity cut
inner = cq.Workplane('XY').circle(cap_inner_radius).extrude(cap_length)
base = outer.cut(inner)
# Internal rib as a rectangular block attached to inner wall
rib = (cq.Workplane('XY')
       .box(rib_thickness, rib_length, cap_length - 2 * cap_wall_thickness)
       .translate((cap_inner_radius - rib_thickness/2,
                   0,
                   cap_wall_thickness + (cap_length - 2 * cap_wall_thickness)/2)))
solid_with_rib = base.union(rib)
# Blind set‑screw hole (non‑through)
hole = (cq.Workplane('XY')
        .center(set_screw_offset, 0)
        .circle(set_screw_diameter/2)
        .extrude(-set_screw_depth))
solid_with_hole = solid_with_rib.cut(hole)
# Chamfer exterior edges for safety
result = solid_with_hole.edges().chamfer(chamfer_size)
