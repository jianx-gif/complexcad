import cadquery as cq

jaw_length = 80.0
jaw_width = 30.0
jaw_thickness = 10.0
boss_diameter = 20.0
boss_height = 15.0
fillet_radius = 2.0
chamfer_distance = 1.0
clearance_hole_diameter = 5.0
clearance_hole_spacing = 40.0
overlap = 0.5

base = (
    cq.Workplane("XY")
    .rect(jaw_length, jaw_width)
    .circle(boss_diameter / 2.0)
    .extrude(jaw_thickness)
)

base = base.edges("|Z and >X").fillet(fillet_radius)
base = base.edges("|Z and >Y").chamfer(chamfer_distance)

boss = (
    base.faces(">Z").workplane()
    .center(0.0, 0.0)
    .circle(boss_diameter / 2.0)
    .extrude(boss_height)
    .translate((0, 0, -overlap))
)

combined = base.union(boss)

hole_centers = [(-clearance_hole_spacing / 2.0, 0.0), (clearance_hole_spacing / 2.0, 0.0)]

result = (
    combined.faces(">Z").workplane()
    .pushPoints(hole_centers)
    .hole(clearance_hole_diameter)
)
