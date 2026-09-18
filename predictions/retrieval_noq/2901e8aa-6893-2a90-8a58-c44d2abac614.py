import cadquery as cq

# Parameters
housing_height = 80.0
outer_radius_bottom = 20.0
outer_radius_top = 30.0
wall_thickness = 3.0
rib_thickness = 4.0
rib_clearance = 1.0
chamfer_size = 1.0
thread_minor_diameter = 6.0
thread_major_diameter = 8.0
thread_pitch = 2.5
thread_length = 30.0

# Loft steps
steps = 5
height_step = housing_height / steps
radius_step = (outer_radius_top - outer_radius_bottom) / steps

# Build outer loft
outer = cq.Workplane('XY')
outer = outer.circle(outer_radius_bottom)
for i in range(1, steps + 1):
    r = outer_radius_bottom + i * radius_step
    outer = outer.workplane(offset=height_step * i).circle(r)
outer = outer.loft(combine=True)

# Shell to create interior cavity
hollow = outer.shell(-wall_thickness)

# Internal rib (disc) positioned at mid-height
mid_z = housing_height / 2.0 - rib_thickness / 2.0
inner_radius_mid = (outer_radius_bottom + outer_radius_top) / 2.0 - wall_thickness - rib_clearance
rib = cq.Workplane('XY').center(0, 0).circle(inner_radius_mid).extrude(rib_thickness).translate((0, 0, mid_z))

# Combine rib with housing
result = hollow.union(rib)

# Chamfer entrance (top outer edge)
result = result.faces('>Z').edges().chamfer(chamfer_size)

# Blind hole for thread (minor diameter)
result = result.faces('>Z').workplane().hole(thread_minor_diameter, thread_length)

# Thread geometry using helix wire
thread_wire = cq.Wire.makeHelix(pitch=thread_pitch, height=thread_length, radius=thread_major_diameter/2.0)
# Triangular thread profile in XY plane
thread_profile = cq.Workplane('XY').polygon(3, thread_pitch).translate((thread_major_diameter/2.0, 0, 0))
thread = thread_profile.sweep(path=thread_wire)
# Align thread start with top face of blind hole
thread = thread.translate((0, 0, -thread_length))
# Cut thread from part to create internal threads
result = result.cut(thread)
