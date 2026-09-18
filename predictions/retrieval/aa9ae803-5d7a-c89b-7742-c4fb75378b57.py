import cadquery as cq
import math

outer_radius = 30.0
inner_radius_large = 15.0
inner_radius_small = 10.0
taper_length = 20.0
cyl_section_length = 20.0
housing_length = taper_length + cyl_section_length
flange_thickness = 10.0
flange_outer_radius = 40.0
vent_section_length = 30.0
vent_hole_diameter = 5.0
vent_rows = 4
vent_cols = 6
chamfer_distance = 1.0

outer = cq.Workplane('XY').circle(outer_radius).extrude(housing_length)

bore_profile = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(inner_radius_large, 0)
    .lineTo(inner_radius_large, taper_length)
    .lineTo(inner_radius_small, taper_length)
    .lineTo(inner_radius_small, taper_length + cyl_section_length)
    .lineTo(0, taper_length + cyl_section_length)
    .close()
)

bore = bore_profile.revolve(360)

housing = outer.cut(bore)

flange = cq.Workplane('XY').circle(flange_outer_radius).extrude(flange_thickness)
flange = flange.translate((0, 0, -flange_thickness))

housing = housing.union(flange)

wall_thickness = outer_radius - inner_radius_large
vent_start_z = (housing_length - vent_section_length) / 2.0
axial_positions = [vent_start_z + i * (vent_section_length / (vent_rows - 1)) for i in range(vent_rows)]

holes = []
for col in range(vent_cols):
    angle = 360.0 * col / vent_cols
    for z in axial_positions:
        hole = (
            cq.Workplane('YZ')
            .center(outer_radius - wall_thickness / 2.0, z)
            .circle(vent_hole_diameter / 2.0)
            .extrude(outer_radius * 2.0)
            .rotate((0, 0, 0), (0, 0, 1), angle)
        )
        holes.append(hole)

vent_holes = cq.Workplane('XY')
for h in holes:
    vent_holes = vent_holes.union(h)

housing = housing.cut(vent_holes)

result = housing.edges().chamfer(chamfer_distance)
