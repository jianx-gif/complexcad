import cadquery as cq

# Parameters
plate_length = 80.0
plate_width = 50.0
plate_thickness = 5.0
counterbore_diameter = 20.0
counterbore_depth = 3.0
counterbore_hole_diameter = 8.0
fillet_radius = 1.0
hole_diameter = 5.0
hole_rows = 2
hole_cols = 3
hole_spacing_x = 30.0
hole_spacing_y = 20.0
rib_thickness = 2.0
rib_height = 4.0
link_hole_diameter = 10.0
link_hole_offset = 20.0

# Base plate
base = (
    cq.Workplane('XY')
    .rect(plate_length, plate_width)
    .extrude(plate_thickness)
)

# Central link hole (circular cut) offset from center
base = (
    base.faces('>Z')
    .workplane()
    .center(plate_length/2 - link_hole_offset, 0)
    .hole(link_hole_diameter)
)

# Counterbore at plate center
base = (
    base.faces('>Z')
    .workplane()
    .cskHole(counterbore_hole_diameter, counterbore_diameter, counterbore_depth)
)

# Fillet internal vertical edge of counterbore
base = base.edges('|Z').fillet(fillet_radius)

# Drilled hole pattern on top surface (rectangular array)
base = (
    base.faces('>Z')
    .workplane()
    .rarray(hole_spacing_x, hole_spacing_y, hole_cols, hole_rows, center=True)
    .hole(hole_diameter)
)

# Single stiffening rib on back side (negative Z)
rib = (
    base.faces('<Z')
    .workplane()
    .rect(plate_length, rib_thickness)
    .extrude(-rib_height)
)

result = base.union(rib)
