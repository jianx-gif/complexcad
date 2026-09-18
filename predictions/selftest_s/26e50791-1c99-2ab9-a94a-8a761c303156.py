import cadquery as cq

socket_radius = 40
outer_wall_thickness = 5
outer_radius = socket_radius + outer_wall_thickness
block_height = 30
flat_surface_depth = 6
fillet_radius = 2
mount_hole_diameter = 5
mount_hole_spacing = 30
rib_thickness = 3
rib_height = 12
rib_count = 4
rib_spacing_angle = 360 / rib_count

base_cylinder = cq.Workplane('XY').cylinder(block_height, outer_radius)

sphere_cut = cq.Workplane('XY').sphere(socket_radius).translate((0, 0, block_height/2))
part = base_cylinder.cut(sphere_cut)

flat_cut = cq.Workplane('XY').box(2*outer_radius, 2*outer_radius, flat_surface_depth).translate((0, 0, block_height/2 + socket_radius - flat_surface_depth/2))
part = part.cut(flat_cut)

part = part.faces('>Z').edges().fillet(fillet_radius)

hole_positions = [
    ( mount_hole_spacing/2,  mount_hole_spacing/2),
    (-mount_hole_spacing/2,  mount_hole_spacing/2),
    (-mount_hole_spacing/2, -mount_hole_spacing/2),
    ( mount_hole_spacing/2, -mount_hole_spacing/2)
]
part = (part
    .faces('>Z')
    .workplane()
    .pushPoints(hole_positions)
    .hole(mount_hole_diameter)
)

for i in range(rib_count):
    angle = i * rib_spacing_angle
    rib = (part
        .faces('>Z')
        .workplane()
        .center(outer_radius - rib_thickness/2, 0)
        .rotate((0,0,0), (0,0,1), angle)
        .rect(rib_thickness, rib_height)
        .extrude(rib_thickness)
    )
    part = part.union(rib)

result = part