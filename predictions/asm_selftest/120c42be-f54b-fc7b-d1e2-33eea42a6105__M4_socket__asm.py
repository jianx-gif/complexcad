parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(-20, -15, 2.5), seat=2.3, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 0), axis=(0, 0, 1), point=(-20, -15, 2.5), seat=3.2, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-20, -15, 2.5), seat=-2.5, flip=True))
parts.append(place(fastener("washer", 'M4', 1), axis=(0, 0, 1), point=(0, 0, 2.5), seat=2.3, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 1), axis=(0, 0, 1), point=(0, 0, 2.5), seat=3.2, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 1), axis=(0, 0, 1), point=(0, 0, 2.5), seat=-2.5, flip=True))
