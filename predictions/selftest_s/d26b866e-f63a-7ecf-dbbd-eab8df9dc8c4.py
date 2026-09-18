import cadquery as cq

# Parameters
flange_radius = 40.0
flange_thickness = 10.0
pin_radius = 5.0
pin_length = 15.0
blind_hole_diameter = 6.0
blind_hole_depth = 6.0
chamfer_size = 2.0
mounting_hole_diameter = 4.0
mounting_hole_spacing = 30.0
base_width = 70.0
base_height = 30.0
base_thickness = 8.0
rib_height = 3.0
rib_width = 5.0
rib_spacing = 15.0

# Base plate
base = (
    cq.Workplane("XY")
    .rect(base_width, base_height)
    .extrude(base_thickness)
)

# Circular flange (hub) on top of base
hub = (
    cq.Workplane("XY")
    .circle(flange_radius)
    .extrude(flange_thickness)
    .translate((0, 0, base_thickness))
)

# Integral pin protruding radially from hub center
pin = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness + flange_thickness / 2)
    .transformed(rotate=(0, 90, 0))
    .circle(pin_radius)
    .extrude(pin_length)
)

# Stiffening ribs on top surface of base
rib1 = (
    cq.Workplane("XY")
    .rect(base_width - 2 * rib_spacing, rib_width)
    .extrude(rib_height)
    .translate((0, -(base_height / 2 - rib_spacing - rib_width / 2), base_thickness / 2))
)
rib2 = (
    cq.Workplane("XY")
    .rect(base_width - 2 * rib_spacing, rib_width)
    .extrude(rib_height)
    .translate((0, (base_height / 2 - rib_spacing - rib_width / 2), base_thickness / 2))
)

# Assemble base, hub, pin, and ribs
assembly = (
    base
    .union(hub)
    .union(pin)
    .union(rib1)
    .union(rib2)
)

# Apply 45° chamfer on vertical edges of flange and pin
assembly = assembly.edges("|Z").chamfer(chamfer_size)

# Blind drilled hole on top face of flange (radial direction)
assembly = (
    assembly
    .faces(">Z")
    .workplane()
    .pushPoints([(flange_radius - blind_hole_depth / 2, 0)])
    .hole(blind_hole_diameter, depth=blind_hole_depth)
)

# Mounting holes on bottom face of base (four symmetric points)
assembly = (
    assembly
    .faces("<Z")
    .workplane()
    .pushPoints([
        (-mounting_hole_spacing / 2, -mounting_hole_spacing / 2),
        ( mounting_hole_spacing / 2, -mounting_hole_spacing / 2),
        ( mounting_hole_spacing / 2,  mounting_hole_spacing / 2),
        (-mounting_hole_spacing / 2,  mounting_hole_spacing / 2)
    ])
    .hole(mounting_hole_diameter)
)

result = assembly
