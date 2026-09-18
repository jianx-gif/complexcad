parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(-20, 0, 2.5), seat=2.5, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 0), axis=(0, 0, 1), point=(-20, 0, 2.5), seat=3.4, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-20, 0, 2.5), seat=-2.5, flip=True))
