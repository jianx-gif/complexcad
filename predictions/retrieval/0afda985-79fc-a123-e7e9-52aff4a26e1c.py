import cadquery as cq

# dimensional parameters
housing_total_length = 80.0
housing_base_diameter = 60.0
housing_top_diameter = 40.0
loft_step_height = 8.0
outlet_diameter = 20.0
outlet_length = 15.0
chamfer_distance = 1.5
passage_radius = 5.0
passage_bend_offset = 10.0
tab_width = 12.0
tab_height = 20.0
tab_thickness = 4.0
mounting_hole_diameter = 4.0

# compute number of loft steps
num_loft_steps = int(housing_total_length / loft_step_height)

# build lofted outer shell
outer_shell = cq.Workplane('XY').circle(housing_base_diameter/2)
for i in range(1, num_loft_steps+1):
    z_offset = i * loft_step_height
    interp_ratio = i/num_loft_steps
    radius_at_z = (housing_base_diameter/2) * (1 - interp_ratio) + (housing_top_diameter/2) * interp_ratio
    outer_shell = outer_shell.workplane(offset=z_offset).circle(radius_at_z)
outer_shell = outer_shell.loft(combine=True)

# outlet cylinder with chamfer
outlet = cq.Workplane('XY').workplane(offset=housing_total_length).circle(outlet_diameter/2).extrude(outlet_length)
outlet = outlet.edges().chamfer(chamfer_distance)

housing_body = outer_shell.union(outlet)

# internal passage sweep path
path = (
    cq.Workplane('XZ')
    .lineTo(0, housing_total_length/2)
    .lineTo(passage_bend_offset, housing_total_length)
    .wire()
)
passage = cq.Workplane('XY').circle(passage_radius).sweep(path)
housing_body = housing_body.cut(passage)

# add mounting tabs with holes on opposite sides, intersecting the main body
for sign in (-1, 1):
    offset_x = sign * (housing_base_diameter/2 - tab_thickness)
    tab = (
        cq.Workplane('XY')
        .workplane(offset=housing_total_length/2)
        .transformed(offset=(offset_x, 0, 0))
        .rect(tab_thickness, tab_height)
        .extrude(tab_width)
    )
    hole1 = (
        cq.Workplane('XY')
        .workplane(offset=housing_total_length/2)
        .transformed(offset=(offset_x, 0, 0))
        .center(0, -tab_height/4)
        .circle(mounting_hole_diameter/2)
        .extrude(tab_width+2)
    )
    hole2 = (
        cq.Workplane('XY')
        .workplane(offset=housing_total_length/2)
        .transformed(offset=(offset_x, 0, 0))
        .center(0, tab_height/4)
        .circle(mounting_hole_diameter/2)
        .extrude(tab_width+2)
    )
    tab = tab.cut(hole1).cut(hole2)
    housing_body = housing_body.union(tab)

result = housing_body