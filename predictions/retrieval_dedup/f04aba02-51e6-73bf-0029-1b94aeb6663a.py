import cadquery as cq
import copy
import math

def combine_wires(self):
    wires = [obj for obj in self.objects if isinstance(obj, cq.Wire)]
    if len(wires) < 2:
        return self
    temp = cq.Workplane('XY')
    for w in wires:
        temp = temp.add(w).toPending().extrude(0.01)
    combined = temp.combine()
    return combined.faces('<Z').wires()

cq.Workplane.combine_wires = combine_wires

class Measures:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

params = Measures(
    outer_width=80.0,
    outer_depth=60.0,
    cover_height=12.0,
    wall_thickness=3.0,
    draft_angle=5.0,
    boss_diameter=8.0,
    boss_height=6.0,
    boss_offset_x=15.0,
    boss_offset_y=12.0,
    slot_width=4.0,
    slot_height=12.0,
    slot_pitch_x=12.0,
    slot_pitch_y=15.0,
    socket_width=30.0,
    socket_depth=20.0,
    socket_height=6.0,
    socket_chamfer=1.0,
    chamfer_edge=0.8,
)

m = params

outer_wire = (
    cq.Workplane('XY')
    .polyline([
        (0, 0),
        (m.outer_width, 0),
        (m.outer_width, m.outer_depth),
        (0, m.outer_depth),
        (0, 0)
    ])
    .close()
)

off = m.wall_thickness
inner_wire = (
    cq.Workplane('XY')
    .polyline([
        (off, off),
        (m.outer_width - off, off),
        (m.outer_width - off, m.outer_depth - off),
        (off, m.outer_depth - off),
        (off, off)
    ])
    .close()
)

profile_wire = (
    cq.Workplane('XY')
    .add(outer_wire)
    .add(inner_wire)
    .combine_wires()
    .toPending()
)

shell = profile_wire.extrude(m.cover_height, taper=m.draft_angle)

# Vent slots
num_x = int((m.outer_width - 2*m.wall_thickness) // m.slot_pitch_x)
num_y = int((m.outer_depth - 2*m.wall_thickness) // m.slot_pitch_y)
slots = cq.Workplane('XY')
for i in range(-num_x//2, num_x//2 + 1):
    for j in range(-num_y//2, num_y//2 + 1):
        slots = slots.union(
            cq.Workplane('XY')
            .center(i * m.slot_pitch_x, j * m.slot_pitch_y)
            .rect(m.slot_width, m.slot_height)
            .extrude(m.cover_height + 0.1)
        )

shell = shell.cut(slots)

# Mounting bosses
boss_solids = []
for x_sign in (-1, 1):
    for y_sign in (-1, 1):
        bx = m.outer_width/2 + x_sign * m.boss_offset_x
        by = m.outer_depth/2 + y_sign * m.boss_offset_y
        boss = (
            cq.Workplane('XY')
            .center(bx, by)
            .circle(m.boss_diameter/2)
            .extrude(m.boss_height)
        )
        boss_solids.append(boss.val())

bosses = cq.Workplane('XY').union(*boss_solids)

shell = shell.union(bosses)

# Countersunk holes through top surface
shell = shell.faces('>Z').cskHole(
    m.boss_diameter*0.6,
    m.boss_diameter*0.8,
    90,
    depth=m.cover_height + m.boss_height
)

# X-Mount style socket recess with chamfer
socket = (
    cq.Workplane('XY')
    .center(0, 0)
    .rect(m.socket_width, m.socket_depth)
    .extrude(m.socket_height)
    .faces('>Z')
    .edges()
    .chamfer(m.socket_chamfer)
)

shell = shell.cut(socket)

result = shell
