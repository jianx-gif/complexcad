import cadquery as cq

# Parameters
total_length = 80.0
base_width = 30.0
base_height = 20.0
tip_width = 15.0
tip_height = 10.0
section_count = 6
section_spacing = total_length / (section_count - 1)
width_step = (base_width - tip_width) / (section_count - 1)
height_step = (base_height - tip_height) / (section_count - 1)
rib_thickness = 2.0
rib_height = 12.0
rib_spacing = 15.0
rib_count = int(total_length / rib_spacing)
hole_diameter = 5.0
hole_spacing = 20.0
hole_count = int(total_length / hole_spacing)
chamfer_distance = 0.2

# Build outer lofted body
outer = cq.Workplane("XY").rect(base_width, base_height)
for i in range(1, section_count):
    w = base_width - i * width_step
    h = base_height - i * height_step
    outer = outer.workplane(offset=section_spacing).rect(w, h)
outer = outer.loft(combine=True)

# Build inner cavity loft
inner = cq.Workplane("XY").rect(base_width * 0.4, base_height * 0.4)
for i in range(1, section_count):
    w = (base_width * 0.4) - i * (width_step * 0.6)
    h = (base_height * 0.4) - i * (height_step * 0.6)
    inner = inner.workplane(offset=section_spacing).rect(w, h)
inner = inner.loft(combine=True)

# Subtract cavity
result = outer.cut(inner)

# Add ribs on +Y side
for i in range(rib_count):
    z_pos = i * rib_spacing + rib_spacing / 2
    rib = (
        cq.Workplane("XY")
        .rect(rib_thickness, rib_height)
        .extrude(rib_spacing * 0.8)
        .translate((0, base_height / 2 - rib_height / 2, z_pos))
    )
    result = result.union(rib)

# Add ribs on -Y side
for i in range(rib_count):
    z_pos = i * rib_spacing + rib_spacing / 2
    rib = (
        cq.Workplane("XY")
        .rect(rib_thickness, rib_height)
        .extrude(rib_spacing * 0.8)
        .translate((0, -base_height / 2 + rib_height / 2, z_pos))
    )
    result = result.union(rib)

# Add mounting holes on +X side
for i in range(hole_count):
    z_pos = i * hole_spacing + hole_spacing / 2
    result = (
        result.faces(">X")
        .workplane()
        .center(0, z_pos)
        .hole(hole_diameter)
    )

# Apply chamfer to edges on +X side
result = result.edges(">X").chamfer(chamfer_distance)
