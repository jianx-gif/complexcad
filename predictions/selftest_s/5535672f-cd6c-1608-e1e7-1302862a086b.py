import cadquery as cq
from types import SimpleNamespace as Measures
import math

# Parameters (max dimension 100)
plate_width = 70.0
plate_height = 100.0
plate_thickness = 8.0
chamfer = 1.0
hole_dia = 5.0
hole_spacing_x = 30.0
hole_spacing_y = 30.0
rib_width = 5.0
rib_height = 12.0
rib_spacing = 15.0
rib_thickness = 4.0
slot_width = 10.0
slot_height = 40.0

class WallMountHingePlate:
    def __init__(self, workplane, measures):
        self.wp = workplane
        self.meas = measures
        self.build()

    def build(self):
        m = self.meas
        # Base rectangular plate
        base = (
            cq.Workplane("XY")
            .rect(m.width, m.height)
            .extrude(m.thickness)
            .edges("|Z")
            .chamfer(m.chamfer)
        )

        # Rib reinforcement on top face, fused with base via combine=True
        with_ribs = (
            base.faces(">Z").workplane()
            .rarray(m.rib_spacing, 0, int(m.width // m.rib_spacing), 1, center=True)
            .rect(m.rib_width, m.rib_height)
            .extrude(m.rib_thickness, combine=True)
        )

        # Side slot cut for hinge clearance on the -X face
        with_slot = (
            with_ribs.faces("<X").workplane()
            .rect(m.slot_width, m.slot_height)
            .cutBlind(-(m.thickness + 2))
        )

        # Drill four Ø5 holes through the entire thickness on top face
        final = (
            with_slot.faces(">Z").workplane()
            .rarray(m.hole_spacing_x, m.hole_spacing_y, 2, 2, center=True)
            .hole(m.hole_diameter)
        )

        self.model = final

# Measure container
measures = Measures(
    width = plate_width,
    height = plate_height,
    thickness = plate_thickness,
    chamfer = chamfer,
    rib_width = rib_width,
    rib_height = rib_height,
    rib_spacing = rib_spacing,
    rib_thickness = rib_thickness,
    hole_diameter = hole_dia,
    hole_spacing_x = hole_spacing_x,
    hole_spacing_y = hole_spacing_y,
    slot_width = slot_width,
    slot_height = slot_height,
)

result = WallMountHingePlate(cq.Workplane("XY"), measures).model
