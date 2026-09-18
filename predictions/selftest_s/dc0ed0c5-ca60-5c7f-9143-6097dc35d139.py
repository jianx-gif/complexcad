
import cadquery as cq

housing_length = 100.0
inlet_radius = 12.0
outlet_radius = 30.0
section_count = 6
height_step = housing_length / (section_count - 1)
wall_thickness = 2.0
fillet_radius = 0.8
vent_hole_diameter = 3.0
vent_spacing = 8.0
vent_rows = 4
vent_cols = 5

# Build outer loft profile
outer = cq.Workplane("XY").circle(inlet_radius)
for i in range(1, section_count):
    radius = inlet_radius + (outlet_radius - inlet_radius) * i / (section_count - 1)
    outer = outer.workplane(offset=height_step).circle(radius)
outer = outer.loft(combine=True)
# Fillet on inlet face edges before shelling
outer = outer.faces("<Z").edges().fillet(fillet_radius)
# Create thin-walled shell
hollow = outer.shell(wall_thickness)
# Vent pattern on outer surface (largest Z face)
result = (
    hollow.faces(">Z")
    .workplane()
    .rarray(vent_spacing, vent_spacing, vent_cols, vent_rows)
    .hole(vent_hole_diameter)
)
