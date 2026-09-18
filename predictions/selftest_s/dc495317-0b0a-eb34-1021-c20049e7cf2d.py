import cadquery as cq

# parameters
rod_length = 80.0
large_diam = 30.0
small_diam = 20.0
step_height = 40.0
shell_thk = -2.0
edge_chamfer = 0.5
central_hole_diam = 5.0
side_hole_diam = 6.0
side_hole_offset = large_diam / 2 - 5.0

class SteppedRod:
    def __init__(self):
        self.large_rad = large_diam / 2.0
        self.small_rad = small_diam / 2.0
    def model(self):
        profile = (
            cq.Workplane("XY")
            .moveTo(self.large_rad, 0)
            .lineTo(self.large_rad, step_height)
            .lineTo(self.small_rad, step_height)
            .lineTo(self.small_rad, rod_length)
            .lineTo(0, rod_length)
            .lineTo(0, 0)
            .close()
        )
        solid = profile.revolve()
        hollow = solid.shell(shell_thk)
        chamfered = hollow.edges().chamfer(edge_chamfer)
        # central axial bore after shell
        bore = cq.Workplane("XY").circle(central_hole_diam / 2).extrude(rod_length * 1.2)
        with_central_hole = chamfered.cut(bore)
        side_face = with_central_hole.faces("|Z").first()
        result = (
            side_face.workplane(centerOption="CenterOfMass")
            .polarArray(side_hole_offset, 0, 360, 4)
            .hole(side_hole_diam)
        )
        return result

result = SteppedRod().model()
