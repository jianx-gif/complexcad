import cadquery as cq

# Parameters
total_length = 80.0
num_sections = 6
section_height = total_length / (num_sections - 1)
outer_width_start = 30.0
outer_width_end = 15.0
outer_height_start = 20.0
outer_height_end = 10.0
inner_width_start = 15.0
inner_width_end = 7.0
inner_height_start = 10.0
inner_height_end = 5.0
web_thickness = 2.0
port_diameter = 5.0
port_spacing = 20.0
chamfer_distance = 0.2

def lerp(start, end, t):
    return start + (end - start) * t

# Build outer loft profile chain
outer = cq.Workplane("XY").rect(outer_width_start, outer_height_start)
for i in range(1, num_sections):
    t = i / (num_sections - 1)
    w = lerp(outer_width_start, outer_width_end, t)
    h = lerp(outer_height_start, outer_height_end, t)
    outer = outer.workplane(offset=section_height).rect(w, h)
outer = outer.loft(combine=True)

# Build inner loft profile chain
inner = cq.Workplane("XY").rect(inner_width_start, inner_height_start)
for i in range(1, num_sections):
    t = i / (num_sections - 1)
    w = lerp(inner_width_start, inner_width_end, t)
    h = lerp(inner_height_start, inner_height_end, t)
    inner = inner.workplane(offset=section_height).rect(w, h)
inner = inner.loft(combine=True)

# Create hollow runner
runner = outer.cut(inner)

# Add webbing ribs
webs = cq.Workplane("XY")
for i in range(1, num_sections - 1):
    z = i * section_height
    t = i / (num_sections - 1)
    outer_h = lerp(outer_height_start, outer_height_end, t)
    inner_h = lerp(inner_height_start, inner_height_end, t)
    gap = (outer_h - inner_h) / 2.0
    rib_pos = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .center(0, inner_h / 2.0 + gap / 2.0)
        .rect(web_thickness, gap)
        .extrude(section_height)
    )
    rib_neg = (
        cq.Workplane("XY")
        .workplane(offset=z)
        .center(0, -(inner_h / 2.0 + gap / 2.0))
        .rect(web_thickness, gap)
        .extrude(section_height)
    )
    webs = webs.union(rib_pos).union(rib_neg)

result = runner.union(webs)

# Drill fuel ports through the +X side
num_ports = int(total_length / port_spacing) + 1
for i in range(num_ports):
    z = i * port_spacing
    if z > total_length:
        break
    result = (
        result.faces(">X")
        .workplane()
        .transformed(offset=(0, 0, z))
        .hole(port_diameter)
    )
# Chamfer edges of drilled ports for safety
result = result.faces(">X").edges().chamfer(chamfer_distance)
