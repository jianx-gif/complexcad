import cadquery as cq

cap_outer_diameter = 80
cap_height = 30
wall_thickness = 5
boss_diameter = 30
boss_height = 15
top_chamfer = 3
thread_hole_diameter = 10
mount_hole_diameter = 8
mount_hole_radius = (cap_outer_diameter/2) - wall_thickness - 5
rib_thickness = 2
rib_height = 8
rib_count = 4
pocket_depth = 5
bottom_chamfer = 2

# Base cap solid
result = (
    cq.Workplane("XY")
    .circle(cap_outer_diameter/2)
    .extrude(cap_height)
    .shell(-wall_thickness)
)

# Central boss
result = (
    result.faces(">Z").workplane()
    .circle(boss_diameter/2)
    .extrude(boss_height)
)

# Threaded hole in boss (through boss only)
result = (
    result.faces(">Z").workplane()
    .hole(thread_hole_diameter, depth=boss_height)
)

# Top chamfer on outer perimeter (including boss top)
result = result.faces(">Z").edges().chamfer(top_chamfer)

# Pocket on top of boss
result = (
    result.faces(">Z").workplane()
    .rect(boss_diameter*0.6, boss_diameter*0.6)
    .cutBlind(-pocket_depth)
)

# Mounting holes on top face, arranged radially
result = (
    result.faces(">Z").workplane()
    .polarArray(radius=mount_hole_radius, count=4, startAngle=0, angle=360)
    .hole(mount_hole_diameter)
)

# Bottom edge chamfer for safety
result = result.edges("<Z").chamfer(bottom_chamfer)

# Add radial ribs (simple extruded blocks) around outer circumference
for i in range(rib_count):
    angle = i * 360 / rib_count
    rib = (
        cq.Workplane("XY")
        .center((cap_outer_diameter/2) - wall_thickness/2, 0)
        .rect(rib_thickness, rib_height)
        .extrude(cap_height/2)
        .rotate((0, 0, 0), (0, 0, 1), angle)
    )
    result = result.union(rib)

