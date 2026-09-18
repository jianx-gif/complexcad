import cadquery as cq
outer_length = 80.0
outer_length = 100.0
outer_length = 20.0
outer_length = 12.0
outer_length = 15.0
outer_length = 15.0
outer_length = outer_length - 2.0
outer_length = outer_length - 2.0
outer = (
    cq.Workplane('XY')
    .box(outer_length,outer_length,outer_thickness)
    .faces('>Z').workplane()
    .rect(outer_length,outer_length)
    .extrude(outer_length)
    .faces(centered for i in range(outer_radius, 0, 0), (0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), 0, 0, 0), (0, 0, 0, 0, 0), (0, 0, 0), (0, 0, 0), (0, 0, 0, 0), (0, 0, 0), (0, 0, -outer_length), (0, -outer_length), (-outer_length), (0, -outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), (-outer_length), -outer_length), (-outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length), -outer_length, -outer_length), -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length, -outer_length