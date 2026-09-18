import cadquery as cq

# Parameters
hub_radius = 20.0
frame_width = 80.0
frame_height = 40.0
carrier_thickness = 10.0
key_slot_width = 5.0
key_slot_length = 30.0
chamfer_distance = 1.0
mount_hole_dia = 5.0
mount_hole_spacing = 60.0

class SprocketCarrier:
    def __init__(self):
        self.hub_radius = hub_radius
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.thickness = carrier_thickness
        self.key_width = key_slot_width
        self.key_length = key_slot_length
        self.chamfer = chamfer_distance
        self.hole_dia = mount_hole_dia
        self.hole_spacing = mount_hole_spacing

    def build(self):
        # Base loft between hub and frame
        part = (
            cq.Workplane("XY")
            .circle(self.hub_radius)
            .workplane(offset=self.thickness)
            .rect(self.frame_width, self.frame_height)
            .loft()
        )
        # Key slot through hub region
        part = (
            part.faces(">Z")
            .workplane(centerOption="CenterOfMass")
            .rect(self.key_width, self.key_length)
            .cutBlind(-self.thickness)
        )
        # Mounting holes on rectangular face
        hole_positions = [
            (-self.hole_spacing / 2, 0),
            (self.hole_spacing / 2, 0),
        ]
        part = (
            part.faces(">Z")
            .workplane()
            .pushPoints(hole_positions)
            .hole(self.hole_dia)
        )
        # Chamfer outer vertical edges
        part = part.edges("|Z").chamfer(self.chamfer)
        return part

result = SprocketCarrier().build()
