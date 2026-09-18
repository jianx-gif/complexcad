import cadquery as cq
import math
outer_radius = 50
height = 20
wall_thickness = 2
inner_radius = outer_radius - wall_thickness
groove_depth = 1.5
groove_width = 2
groove_offset_from_top = 4
screw_hole_dia = 3
vent_dia = 2
vent_rows = 4
vent_cols = 4
vent_spacing = 12
chamfer_size = 0.5
tab_width = 10
tab_thickness = 2
tab_height = 5
tab_radius = outer_radius - wall_thickness/2
tab_angles = [0, 120, 240]
tab_positions = [(tab_radius*math.cos(math.radians(a)), tab_radius*math.sin(math.radians(a))) for a in tab_angles]
base = (
    cq.Workplane("XZ")
    .polyline([
        (outer_radius, 0),
        (outer_radius, height),
        (inner_radius, height),
        (inner_radius + groove_depth, height - groove_offset_from_top),
        (inner_radius, height - groove_offset_from_top - groove_width),
        (inner_radius, 0),
    ])
    .close()
    .revolve()
)
result = (
    base
    .faces(">Z").workplane().hole(screw_hole_dia)
    .faces(">Z").workplane().rarray(vent_spacing, vent_spacing, vent_cols, vent_rows).hole(vent_dia)
    .faces(">Z").workplane().pushPoints(tab_positions).rect(tab_width, tab_thickness).extrude(tab_height)
    .edges("|Z").chamfer(chamfer_size)
)
