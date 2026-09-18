import cadquery as cq

# Parameters
total_length = 80.0
start_diameter = 20.0
end_major_axis = 30.0
end_minor_axis = 15.0
wall_thickness = 3.0
chamfer_size = 0.6
mount_hole_diameter = 4.0
mount_hole_spacing = 25.0
central_hole_diameter = 6.0
rib_width = 4.0
rib_height = 2.0
rib_spacing = 15.0

# Base lofted solid (circle to ellipse)
base = (
    cq.Workplane("XY")
    .circle(start_diameter / 2)
    .workplane(offset=total_length)
    .ellipse(end_major_axis / 2, end_minor_axis / 2)
    .loft()
)

# Shell to create hollow interior
hollow = base.shell(-wall_thickness)

# Central through hole
hollow = hollow.faces(">Z").workplane().hole(central_hole_diameter)

# Mounting holes on top face
hollow = (
    hollow.faces(">Z")
    .workplane()
    .pushPoints([(-mount_hole_spacing / 2, 0), (mount_hole_spacing / 2, 0)])
    .hole(mount_hole_diameter)
)

# Internal ribs for stiffness (cut from interior)
rib_count = int(total_length / rib_spacing)
for i in range(rib_count):
    z_pos = (i + 0.5) * rib_spacing
    hollow = (
        hollow.workplane(offset=z_pos)
        .center(0, 0)
        .rect(rib_width, rib_height)
        .cutBlind(-wall_thickness)
    )

# Chamfer outer edges
result = hollow.edges().chamfer(chamfer_size)
