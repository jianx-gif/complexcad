import cadquery as cq

guide_length = 80.0
inlet_radius = 20.0
mid_radius = 30.0
outlet_radius = 45.0
wall_thickness = 3.0
shaft_hole_diameter = 10.0
mount_hole_diameter = 5.0
mount_hole_spacing = 60.0
rib_thickness = 4.0
rib_height = 10.0
chamfer_size = 1.0

outer = (
    cq.Workplane("XY")
    .circle(inlet_radius)
    .workplane(offset=guide_length/2)
    .circle(mid_radius)
    .workplane(offset=guide_length/2)
    .circle(outlet_radius)
    .loft()
)

inner = (
    cq.Workplane("XY")
    .circle(inlet_radius - wall_thickness)
    .workplane(offset=guide_length/2)
    .circle(mid_radius - wall_thickness)
    .workplane(offset=guide_length/2)
    .circle(outlet_radius - wall_thickness)
    .loft()
)

result = outer.cut(inner)

result = result.faces(">Z").workplane().hole(shaft_hole_diameter)

# side mounting holes through Y direction
hole1 = (
    cq.Workplane('XZ')
    .center(-mount_hole_spacing/2, 0)
    .circle(mount_hole_diameter/2)
    .extrude(guide_length*2)
)

hole2 = (
    cq.Workplane('XZ')
    .center(mount_hole_spacing/2, 0)
    .circle(mount_hole_diameter/2)
    .extrude(guide_length*2)
)

result = result.cut(hole1)
result = result.cut(hole2)

num_ribs = 3
rib_positions = [guide_length * i/(num_ribs+1) for i in range(1, num_ribs+1)]

for pos in rib_positions:
    rib = (
        cq.Workplane("XY")
        .rect(rib_thickness, outlet_radius*2 - 2*wall_thickness)
        .extrude(rib_height)
        .translate((0, 0, pos))
    )
    result = result.union(rib)

result = result.edges("|Z").chamfer(chamfer_size)
