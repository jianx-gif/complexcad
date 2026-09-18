parts = [base]
parts.append(place(fastener("heatset", 12), axis=(0, 0, 1), point=(-20, -10, 2.5), seat=1.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 6, 0), axis=(0, 0, 1), point=(-20, -10, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-20, -10, 2.5), seat=-2.5, flip=True))
