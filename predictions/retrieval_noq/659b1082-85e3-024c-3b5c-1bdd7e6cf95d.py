import cadquery as cq

outer_diameter = 80
housing_height = 60
wall_thickness = 5
opening_diameter = 30
fillet_radius = 2
rib_thickness = 2
rib_width = 5
rib_height = housing_height - 10
num_ribs = 6

outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

base = cq.Workplane("XY").circle(outer_radius).extrude(housing_height)

hollow = base.shell(-wall_thickness)

housing_with_opening = hollow.faces(">Z").workplane().circle(opening_diameter / 2.0).cutBlind(-housing_height)

inner_edges = housing_with_opening.edges().filter(lambda e: e.Length() < 150)

housing_fillet = inner_edges.fillet(fillet_radius)

rib_angle_increment = 360.0 / num_ribs
ribs = cq.Workplane("XY")
for i in range(num_ribs):
    rib = (
        cq.Workplane("XY")
        .center(inner_radius + rib_thickness / 2.0, 0)
        .rect(rib_thickness, rib_width)
        .extrude(rib_height)
        .rotate((0, 0, 0), (0, 0, 1), i * rib_angle_increment)
    )
    ribs = ribs.union(rib)

result = housing_fillet.union(ribs)
