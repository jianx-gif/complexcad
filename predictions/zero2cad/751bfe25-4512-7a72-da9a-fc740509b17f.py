import cadquery as cq

# Parameters
outer_radius = 45.0
inner_radius = 30.0
thickness = 10.0
groove_width = 5.0
groove_depth = 2.0
fillet_radius = 1.0
hole_diameter = 5.0
hole_count = 2
boss_radius = 10.0
boss_height = 3.0

# Base disc
base = cq.Workplane('XY').circle(outer_radius).extrude(thickness)

# Central boss on top surface
boss = (
    cq.Workplane('XY')
    .circle(boss_radius)
    .extrude(boss_height)
    .translate((0, 0, thickness))
)
base = base.union(boss)

# Mounting holes on top surface, evenly spaced
hole_radius = outer_radius - groove_width / 2.0
base = (
    base.faces('>Z')
    .workplane()
    .polarArray(radius=hole_radius, startAngle=0, count=hole_count, angle=180)
    .hole(hole_diameter)
)

# Groove profile (XZ plane) with built-in fillet at inner corner
profile = (
    cq.Workplane('XZ')
    .moveTo(outer_radius, 0)
    .lineTo(outer_radius, thickness)
    .lineTo(outer_radius - groove_width, thickness)
    .lineTo(outer_radius - groove_width, thickness - groove_depth)
    .threePointArc(
        (outer_radius - groove_width - fillet_radius, thickness - groove_depth - fillet_radius),
        (outer_radius - groove_width - fillet_radius, thickness - groove_depth)
    )
    .lineTo(inner_radius + fillet_radius, thickness - groove_depth)
    .threePointArc(
        (inner_radius, thickness - groove_depth - fillet_radius),
        (inner_radius, thickness - groove_depth)
    )
    .lineTo(inner_radius, 0)
    .close()
)

# Revolve profile to create groove solid
groove = profile.revolve(360)

# Cut groove from base
result = base.cut(groove)
