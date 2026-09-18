parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(10, 2, 2), seat=1, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 10, 0), axis=(0, 0, 1), point=(10, 2, 2), seat=1.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(10, 2, 2), seat=-2, flip=True))
