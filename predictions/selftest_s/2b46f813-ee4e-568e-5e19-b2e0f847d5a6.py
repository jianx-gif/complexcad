import cadquery as cq

outer_diameter = 80
wall_thickness = 4
length = 60
top_flange_height = 10
flange_extension = 12
inlet_diameter = 20
inlet_center_offset = 30
inlet_chamfer = 2
top_fillet_radius = 5
rib_thickness = 2
rib_height = 12
rib_spacing = 15
mounting_hole_dia = 5
mounting_hole_spacing = 30
reinforcement_height = 8
reinforcement_radius = 10

outer_radius = outer_diameter / 2.0
base_height = length - top_flange_height

base_body = cq.Workplane('XY').cylinder(base_height, outer_radius, centered=False)
flange = (
    cq.Workplane('XY')
    .cylinder(top_flange_height, outer_radius + flange_extension, centered=False)
    .translate((0, 0, base_height))
)
combined = base_body.union(flange)

hollow = combined.shell(-wall_thickness)

inlet_cutter = (
    cq.Workplane('YZ')
    .cylinder(wall_thickness + 2, inlet_diameter / 2.0, centered=False)
    .translate((outer_radius - wall_thickness / 2.0, 0, inlet_center_offset))
)
inlet_cutter = inlet_cutter.edges().chamfer(inlet_chamfer)
result = hollow.cut(inlet_cutter)

result = result.faces('>Z').edges().fillet(top_fillet_radius)

rib = (
    cq.Workplane('YZ')
    .rect(rib_height, rib_thickness)
    .extrude(wall_thickness)
    .translate((outer_radius - wall_thickness / 2.0, 0, 0))
)
rib_positions = []
for i in range(1, int(base_height / rib_spacing)):
    rib_positions.append((0, 0, i * rib_spacing))
rib_pattern = rib
for pos in rib_positions:
    rib_pattern = rib_pattern.union(rib.translate(pos))
result = result.union(rib_pattern)

mount_hole = (
    cq.Workplane('YZ')
    .cylinder(wall_thickness + 2, mounting_hole_dia / 2.0, centered=False)
    .translate((outer_radius - wall_thickness / 2.0, 0, base_height / 2.0))
)
result = result.cut(mount_hole)

reinforcement = (
    cq.Workplane('XY')
    .cylinder(reinforcement_height, reinforcement_radius, centered=False)
    .translate((wall_thickness + reinforcement_radius, 0, 0))
)
result = result.union(reinforcement)
