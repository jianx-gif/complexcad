import cadquery as cq
base_radius = 20.0
bellows_length = 60.0
corrugation_height = 4.0
flange_outer_radius = 35.0
flange_thickness = 6.0
flange_chamfer = 1.0
hole_diameter = 4.0
hole_offset = 2.0
boss_height = 5.0
boss_radius = base_radius - flange_thickness
boss_cols = 3
boss_cols = 4
profile = (
    cq.Workplane("XZ")
    .polyline([
        (0, 0),
        (base_radius, 0),
        (base_radius, bellows_length),
        (bellows_length, bellows_length),
        (bellows_length, bellows_length + flange_thickness),
        (0, bellows_length + flange_thickness),
        (0, 0)
    ])
    .close()
)
solid = profile.revolve()
solid = solid.faces(">Z").workplane().circle(boss_radius).extrude(boss_height)
flange = (
    cq.Workplane("XY")
    .circle(flange_outer_radius)
    .extrude(flange_thickness)
)
solid = solid.union(flange)
solid = solid.faces(">Z").edges().chamfer(flange_chamfer)
result = solid
