import cadquery as cq
outer_diameter = 80.0
plate_thickness = 10.0
inner_diameter = 50.0
central_dome_radius = 12.0
central_fillet = 0.8
groove_width = 4.0
groove_depth = 2.0
groove_height = 5.0
countersink_top_diameter = 8.0
countersink_bottom_diameter = 6.0
countersink_angle = 90.0
rib_width = 4.0
rib_height = 3.0
rib_spacing = 20.0
edge_chamfer = 1.0
outer_radius = outer_diameter / 2.0
inner_radius = inner_diameter / 2.0
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(plate_thickness)
)
base = base.edges().fillet(inner_fillet)
base = base.edges().chamfer(edge_chamfer)
base = base.faces(">Z").workplane().circle(central_diameter / 2.0).extrude(plate_thickness)
base = base.faces(">Z").workplane().circle(inner_radius).extrude(plate_thickness)
base = base.faces(">Z").edges().chamfer(edge_chamfer)
rib = (
    cq.Workplane("XY")
    .rect(rib_width, rib_height)
    .extrude(rib_height)
    .translate((0, 0, plate_thickness))
)
base = base.union(rib)
base = base.faces(">Z").edges().chamfer(edge_chamfer)
base = base.faces(">Z").edges().fillet(0.5)
base = base.faces(">Z").edges().chamfer(edge_chamfer)
base = base.faces("<Z").edges().fillet(0.5)
base = base.faces(">Z").edges().chamfer(edge_chamfer)
result = base
