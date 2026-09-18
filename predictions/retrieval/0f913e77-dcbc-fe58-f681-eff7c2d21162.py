import cadquery as cq

# Parameters
bracket_width = 60.0  # total width in mm (max 100)
bracket_height = 80.0  # total height in mm
bracket_thickness = 18.0  # extrusion thickness
entry_radius = 15.0  # radius of conduit entry cutout
entry_fillet_radius = 2.0  # fillet on entry side
clearance_hole_dia = 4.5  # M4 clearance hole diameter
clearance_hole_count = 3
hole_spacing = 20.0

# Tab (mounting gusset) parameters
tab_width = 20.0
tab_height = 30.0
tab_thickness = 5.0

class ConduitBracket:
    def __init__(self, workplane, measures=None):
        self.workplane = workplane
        self.build()

    def build(self):
        # Base profile with rounded entry side
        base = (
            cq.Workplane("XY")
            .moveTo(0, 0)
            .lineTo(0, bracket_height)
            .lineTo(bracket_width - entry_radius, bracket_height)
            .threePointArc((bracket_width, bracket_height), (bracket_width, bracket_height - entry_radius))
            .lineTo(bracket_width, entry_radius)
            .threePointArc((bracket_width, 0), (bracket_width - entry_radius, 0))
            .lineTo(0, 0)
            .close()
            .extrude(bracket_thickness)
        )
        # Fillet on entry side (front face)
        base = base.faces(">Z").edges().fillet(entry_fillet_radius)
        # Clearance holes through the back face
        hole_x = bracket_width / 2.0
        start_y = bracket_height * 0.3
        hole_positions = []
        for i in range(clearance_hole_count):
            hole_positions.append((hole_x, start_y + i * hole_spacing))
        base = (
            base.faces("<Z")
            .workplane()
            .pushPoints(hole_positions)
            .hole(clearance_hole_dia)
        )
        # Add a mounting tab on the back side within the bracket footprint
        offset_x = tab_width / 2.0  # place near lower-left corner
        offset_y = tab_height / 2.0
        tab = (
            cq.Workplane("XY")
            .rect(tab_width, tab_height)
            .extrude(tab_thickness)
            .translate((offset_x, offset_y, 0))
        )
        # Union base and tab into a single solid
        global result
        result = base.union(tab)

# Build the part
ConduitBracket(cq.Workplane("XY"))
