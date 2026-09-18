import cadquery as cq

body_length = 60
inlet_length = 15
outer_radius = 20
inlet_radius = 10
wall_thickness = 3
fillet_radius = 2
rib_width = 4
rib_height = 6
overlap = 0.5

# Base body and inlet
main_body = cq.Workplane('XY').circle(outer_radius).extrude(body_length)
inlet = cq.Workplane('XY').workplane(offset=-inlet_length).circle(inlet_radius).extrude(inlet_length)
union_body = main_body.union(inlet)
# Fillet the external junction edge
union_body = union_body.edges().fillet(fillet_radius)
# Create thin-walled hollow body via shell
hollow_body = union_body.shell(-wall_thickness)
# Compute inner radius after shell
inner_radius = outer_radius - wall_thickness
# Rib attached to inner wall with small overlap for fusion
rib = cq.Workplane('XY').rect(rib_width, rib_height).extrude(body_length)
rib_center_x = -(inner_radius) + overlap - rib_width/2
rib = rib.translate((rib_center_x, 0, 0))
result = hollow_body.union(rib)
