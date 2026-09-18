import cadquery as cq

pulley_radius = 30
pulley_width = 20
shaft_radius = 5
wall_thickness = 3
groove_depth = 6
groove_width = groove_depth * 2
mount_hole_diameter = 6
counterbore_diameter = 12
counterbore_depth = 4
mount_radius = pulley_radius - wall_thickness
rib_height = pulley_width * 0.4
rib_width = pulley_radius * 0.4
rib_thickness = pulley_width * 0.1

result = (
    cq.Workplane('XY')
    .circle(pulley_radius)
    .extrude(pulley_width)
)

result = result.faces('>Z').workplane().hole(2 * shaft_radius)

result = (
    result.faces('<Z')
    .workplane()
    .polarArray(radius=mount_radius, startAngle=0, count=3, angle=360)
    .cboreHole(mount_hole_diameter, counterbore_diameter, counterbore_depth)
)

v_profile = (
    cq.Workplane('XZ')
    .moveTo(pulley_radius, -groove_width / 2)
    .lineTo(pulley_radius - groove_depth, 0)
    .lineTo(pulley_radius, groove_width / 2)
    .close()
    .revolve()
)
result = result.cut(v_profile)

rib = (
    cq.Workplane('XY')
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
    .translate((0, 0, pulley_width - rib_thickness))
)
result = result.union(rib)
