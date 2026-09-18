import cadquery as cq

# Dimensions
total_length = 80.0
inlet_width = 50.0
inlet_height = 30.0
outlet_width = 30.0
outlet_height = 20.0
wall_thickness = 3.0
step_height = 5.0
chamfer_size = 2.0
rib_thickness = 2.0
rib_height = 12.0
rib_spacing = 10.0

class LoftConnector:
    def __init__(self):
        self.outer = None
        self.inner = None
        self.result = None
    def build_outer(self):
        steps = int(total_length / step_height) + 1
        width_step = (inlet_width - outlet_width) / (steps - 1)
        height_step = (inlet_height - outlet_height) / (steps - 1)
        outer = cq.Workplane('XY').rect(inlet_width, inlet_height)
        for i in range(1, steps):
            w = inlet_width - i * width_step
            h = inlet_height - i * height_step
            outer = outer.workplane(offset=step_height).rect(w, h)
        self.outer = outer.loft()
    def apply_chamfer_to_outer(self):
        self.outer = self.outer.faces('<Z').edges().chamfer(chamfer_size)
    def build_inner(self):
        inner_inlet_w = inlet_width - 2 * wall_thickness
        inner_inlet_h = inlet_height - 2 * wall_thickness
        inner_outlet_w = outlet_width - 2 * wall_thickness
        inner_outlet_h = outlet_height - 2 * wall_thickness
        steps = int(total_length / step_height) + 1
        width_step = (inner_inlet_w - inner_outlet_w) / (steps - 1)
        height_step = (inner_inlet_h - inner_outlet_h) / (steps - 1)
        inner = cq.Workplane('XY').rect(inner_inlet_w, inner_inlet_h)
        for i in range(1, steps):
            w = inner_inlet_w - i * width_step
            h = inner_inlet_h - i * height_step
            inner = inner.workplane(offset=step_height).rect(w, h)
        self.inner = inner.loft()
    def add_ribs(self):
        rib_positions = []
        z = step_height
        while z < total_length:
            rib_positions.append(z)
            z += rib_spacing
        ribs = cq.Workplane('XY')
        for zp in rib_positions:
            x_offset = -(inlet_width/2 - wall_thickness/2)
            rib = (
                cq.Workplane('XY')
                .workplane(offset=zp)
                .center(x_offset, 0)
                .box(rib_thickness, wall_thickness + 1.0, rib_height)
            )
            ribs = ribs.union(rib)
        self.result = self.result.union(ribs)
    def build(self):
        self.build_outer()
        self.apply_chamfer_to_outer()
        self.build_inner()
        self.result = self.outer.cut(self.inner)
        self.add_ribs()
        return self.result

connector = LoftConnector()
result = connector.build()
