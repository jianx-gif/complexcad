parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(-25, -8, 3), seat=3, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 0), axis=(0, 0, 1), point=(-25, -8, 3), seat=3.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(-25, -8, 3), seat=-3, flip=True))
parts.append(place(fastener("washer", 'M4', 1), axis=(0, 0, 1), point=(25, -8, 3), seat=2.8, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 12, 1), axis=(0, 0, 1), point=(25, -8, 3), seat=3.7, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 1), axis=(0, 0, 1), point=(25, -8, 3), seat=-3, flip=True))
