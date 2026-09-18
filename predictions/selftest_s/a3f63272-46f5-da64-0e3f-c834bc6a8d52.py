import cadquery as cq
from types import SimpleNamespace as Measures

# Parameter definitions
outer_radius = 45.0  # max dimension 100 units
wall_thickness = 2.0
base_thickness = 5.0
boss_height = 6.0
boss_diameter = 20.0
chamfer = 0.5
mount_hole_diameter = 4.0
mount_hole_spacing = 30.0

measures = Measures(
    outer_radius=outer_radius,
    wall_thickness=wall_thickness,
    base_thickness=base_thickness,
    boss_height=boss_height,
    boss_diameter=boss_diameter,
    chamfer=chamfer,
    mount_hole_diameter=mount_hole_diameter,
    mount_hole_spacing=mount_hole_spacing,
)

class LightFixtureBase:
    def __init__(self, workplane, measures):
        self.workplane = workplane
        self.measures = measures
        self.build()

    def build(self):
        m = self.measures
        # Create base disc with central boss
        base = (
            cq.Workplane("XY")
            .circle(m.outer_radius)
            .extrude(m.base_thickness + m.boss_height)
        )
        boss = (
            cq.Workplane("XY")
            .circle(m.boss_diameter / 2)
            .extrude(m.boss_height)
            .translate((0, 0, m.base_thickness))
        )
        solid = base.union(boss)
        # Shell to generate wall thickness and flanged rim
        shelled = solid.shell(-m.wall_thickness)
        # Chamfer mounting face outer edge
        chamfered = (
            shelled.faces(">Z")
            .edges()
            .chamfer(m.chamfer)
        )
        # Add mounting holes in a 2x2 grid centered
        self.model = (
            chamfered.faces(">Z")
            .workplane()
            .rarray(m.mount_hole_spacing, m.mount_hole_spacing, 2, 2, center=True)
            .hole(m.mount_hole_diameter)
        )

# Build the part
result = LightFixtureBase(cq.Workplane("XY"), measures).model
