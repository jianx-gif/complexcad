import cadquery as cq

outer_diameter = 80
length = 50
wall_thickness = 4
inner_diameter = outer_diameter - 2 * wall_thickness
step_diameter = inner_diameter + 8
step_height = 12
knurl_width = 2
knurl_depth = 1.5
knurl_pitch_angle = 20

base = cq.Workplane('XY').circle(outer_diameter / 2).extrude(length)
shell = base.shell(wall_thickness)
inner_cyl = cq.Workplane('XY').cylinder(length, inner_diameter / 2).translate((0, 0, length / 2))
step_cyl = cq.Workplane('XY').cylinder(step_height, step_diameter / 2).translate((0, 0, step_height / 2))
retainer = shell.cut(inner_cyl).cut(step_cyl)
num_knurl = int(360 / knurl_pitch_angle)
knurl_solids = []
for i in range(num_knurl):
    angle = i * knurl_pitch_angle
    solid = (
        cq.Workplane('XY')
        .center(outer_diameter / 2 - knurl_depth / 2, 0)
        .rect(knurl_depth, knurl_width)
        .extrude(length)
        .rotate((0, 0, 0), (0, 0, 1), angle)
        .val()
    )
    knurl_solids.append(solid)
knurl_compound = cq.Compound.makeCompound(knurl_solids)
result = retainer.cut(knurl_compound)
