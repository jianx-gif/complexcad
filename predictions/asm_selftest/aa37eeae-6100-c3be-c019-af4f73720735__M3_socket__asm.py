parts = [base]
parts.append(place(fastener("washer", 'M3', 0), axis=(0, 0, 1), point=(-25, -10, 4), seat=4, flip=False))
parts.append(place(fastener("screw", 'M3-0.5', 14, 0), axis=(0, 0, 1), point=(-25, -10, 4), seat=4.55, flip=False))
parts.append(place(fastener("nut", 'M3-0.5', 'M3', 0), axis=(0, 0, 1), point=(-25, -10, 4), seat=-4, flip=True))
parts.append(place(fastener("washer", 'M3', 1), axis=(0, 0, 1), point=(-25, 10, 4), seat=4, flip=False))
parts.append(place(fastener("screw", 'M3-0.5', 14, 1), axis=(0, 0, 1), point=(-25, 10, 4), seat=4.55, flip=False))
parts.append(place(fastener("nut", 'M3-0.5', 'M3', 1), axis=(0, 0, 1), point=(-25, 10, 4), seat=-4, flip=True))
