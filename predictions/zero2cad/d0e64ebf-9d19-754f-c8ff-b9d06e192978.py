import cadquery as cq

outer_diameter = 80.0
inner_diameter = 30.0
length = 60.0
wall_thickness = (outer_diameter - inner_diameter) / 2.0
set_screw_diameter = 8.0
set_screw_offset = 20.0
fillet_radius = 0.5
rib_width = 12.0
rib_height = 6.0
rib_thickness = 4.0
rib_spacing = 15.0

base = cq.Workplane('XY').circle(outer_diameter / 2.0).extrude(length)
base = base.edges().fillet(fillet_radius)
base = base.faces('>Z').workplane().hole(inner_diameter)
set_screw_cyl = (
    cq.Workplane('YZ')
    .center(set_screw_offset, length / 2.0)
    .circle(set_screw_diameter / 2.0)
    .extrude(outer_diameter)
)
base = base.cut(set_screw_cyl)
rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_thickness)
    .extrude(rib_height)
)
rib1 = rib.translate((0, outer_diameter / 2.0 - rib_thickness / 2.0, length / 2.0 - rib_spacing / 2.0))
rib2 = rib.translate((0, -(outer_diameter / 2.0 - rib_thickness / 2.0), length / 2.0 - rib_spacing / 2.0))
result = base.union(rib1).union(rib2)
