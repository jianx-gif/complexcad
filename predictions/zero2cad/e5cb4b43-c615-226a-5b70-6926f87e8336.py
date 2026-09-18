import cadquery as cq

plate_width = 80.0
plate_height = 80.0
plate_thickness = 5.0
dome_radius = 20.0
dome_height = 10.0
hole_diameter = 5.0
hole_spacing = 15.0
hole_margin = 10.0
chamfer_size = 1.0
rib_width = 10.0
rib_height = 20.0
rib_thickness = 3.0

base_plate = cq.Workplane('XY').rect(plate_width, plate_height).extrude(plate_thickness)

rib_positions = [
    (0, plate_height/2 - rib_height/2),
    (0, -plate_height/2 + rib_height/2),
    (plate_width/2 - rib_width/2, 0),
    (-plate_width/2 + rib_width/2, 0)
]

ribs = (
    cq.Workplane('XY')
    .workplane(offset=plate_thickness)
    .pushPoints(rib_positions)
    .rect(rib_width, rib_height)
    .extrude(rib_thickness)
)

plate_with_ribs = base_plate.union(ribs)

hole_points = []
start_x = -plate_width/2 + hole_margin
end_x = plate_width/2 - hole_margin
start_y = -plate_height/2 + hole_margin
end_y = plate_height/2 - hole_margin
x = start_x
while x <= end_x:
    y = start_y
    while y <= end_y:
        if (x**2 + y**2) >= (dome_radius + hole_margin)**2:
            hole_points.append((x, y))
        y += hole_spacing
    x += hole_spacing

plate_with_holes = (
    plate_with_ribs
    .faces('>Z')
    .workplane()
    .pushPoints(hole_points)
    .hole(hole_diameter)
)

profile = (
    cq.Workplane('XZ')
    .moveTo(0, 0)
    .lineTo(0, dome_height)
    .threePointArc((dome_radius, dome_height/2), (dome_radius, 0))
    .close()
)

dome = profile.revolve(360).translate((0, 0, plate_thickness))

combined = plate_with_holes.union(dome)

result = combined.edges('|Z').chamfer(chamfer_size)
