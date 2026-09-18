import cadquery as cq

# Parameters
main_diameter = 60.0
wall_thickness = 5.0
housing_length = 80.0
lip_height = 5.0
lip_radius = 3.0
tab_width = 30.0
tab_height = 15.0
tab_thickness = wall_thickness
set_screw_dia = 4.0
set_screw_cbore_dia = 7.0
set_screw_cbore_depth = 5.0
chamfer_dist = 1.0

# Derived dimensions
inner_radius = main_diameter/2 - wall_thickness
outer_radius = main_diameter/2

# Housing profile and revolve
housing = (
    cq.Workplane("XZ")
    .moveTo(inner_radius, 0)
    .lineTo(inner_radius, housing_length)
    .threePointArc((inner_radius - lip_radius, housing_length + lip_height), (inner_radius, housing_length + lip_height))
    .lineTo(outer_radius, housing_length + lip_height)
    .threePointArc((outer_radius + lip_radius, housing_length + lip_height/2), (outer_radius + lip_height, housing_length))
    .lineTo(outer_radius + lip_height, 0)
    .lineTo(inner_radius, 0)
    .close()
    .revolve()
)

# Tab block
tab = (
    cq.Workplane("XY")
    .box(tab_thickness, tab_height, tab_width)
    .translate((outer_radius + tab_thickness/2, 0, 0))
)

result = housing.union(tab)

# Counterbore set screw on outward face of tab
result = (
    result
    .faces(">X")
    .workplane(centerOption="CenterOfMass")
    .cskHole(set_screw_cbore_dia, set_screw_dia, set_screw_cbore_depth)
)

# Chamfer the top lip edge (horizontal edge on top face)
result = result.edges(">Z").chamfer(chamfer_dist)
