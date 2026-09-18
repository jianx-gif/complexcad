import cadquery as cq

length = 80
height_start = 30
height_end = 15
width_start = 40
width_end = 20
thickness_start = 8
thickness_end = 4
fillet_radius = 2
mount_hole_diameter = 5
mount_hole_offset = 15
rib_thickness = 3
rib_height = 10
rib_spacing = 20
pocket_depth = 6
pocket_width = 12
pocket_height = 8

start_plate = (
    cq.Workplane("XY")
    .rect(width_start, height_start)
    .extrude(thickness_start)
)

end_plate = (
    cq.Workplane("XY")
    .rect(width_end, height_end)
    .extrude(thickness_end)
    .translate((0, 0, length))
)

start_wire = start_plate.faces(">Z").wire()
end_wire = end_plate.faces(">Z").wire()

lofted = (
    cq.Workplane("XY")
    .add(start_wire)
    .add(end_wire)
    .loft(combine="s")
)

result = (
    lofted
    .edges()
    .fillet(fillet_radius)
    .faces("<Z")
    .workplane()
    .hole(mount_hole_diameter, depth=length)
    .faces("+Z")
    .workplane()
    .hole(mount_hole_diameter, depth=length)
)

num_ribs = int((length - 2 * mount_hole_offset) / rib_spacing)
for i in range(num_ribs):
    rib = (
        cq.Workplane("XY")
        .center(0, -(height_start / 2 + rib_thickness / 2))
        .rect(rib_thickness, rib_height)
        .extrude(thickness_start / 2)
        .translate((0, 0, mount_hole_offset + i * rib_spacing))
    )
    result = result.union(rib)

result = (
    result
    .faces("+X")
    .workplane(centerOption="CenterOfMass")
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
    .edges("<<Z")
    .chamfer(fillet_radius)
)
