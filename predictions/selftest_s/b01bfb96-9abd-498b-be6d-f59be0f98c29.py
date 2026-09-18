import cadquery as cq

base_diameter = 70.0
base_height = 30.0
shoulder_diameter = 50.0
shoulder_height = 15.0
shell_thickness = 4.0
pilot_hole_diameter = 5.0
edge_chamfer = 2.0

class ShellBase:
    def __init__(self, bd, bh, sd, sh, th, ph, cham):
        self.base_diameter = bd
        self.base_height = bh
        self.shoulder_diameter = sd
        self.shoulder_height = sh
        self.shell_thickness = th
        self.pilot_hole_diameter = ph
        self.edge_chamfer = cham

    def create_profile(self):
        wp = cq.Workplane('XZ')
        wp = wp.moveTo(0, 0)
        wp = wp.lineTo(0, self.base_height)
        wp = wp.threePointArc((self.shoulder_diameter/2, self.base_height + self.shoulder_height/2), (self.shoulder_diameter/2, self.base_height + self.shoulder_height))
        wp = wp.lineTo(self.base_diameter/2, self.base_height + self.shoulder_height)
        wp = wp.lineTo(self.base_diameter/2, 0)
        wp = wp.close()
        solid = wp.revolve()
        return solid

    def apply_shell(self, solid):
        return solid.shell(self.shell_thickness)

    def add_features(self, solid):
        result = solid.edges('>Y').chamfer(self.edge_chamfer)
        result = result.faces('+Z').hole(self.pilot_hole_diameter)
        return result

    def model(self):
        base = self.create_profile()
        shelled = self.apply_shell(base)
        final = self.add_features(shelled)
        return final

part = ShellBase(base_diameter, base_height, shoulder_diameter, shoulder_height, shell_thickness, pilot_hole_diameter, edge_chamfer)
result = part.model()
