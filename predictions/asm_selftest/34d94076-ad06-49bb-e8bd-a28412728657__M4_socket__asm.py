parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 1, 0), point=(0, -19, 15), seat=39, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 46, 0), axis=(0, 1, 0), point=(0, -19, 15), seat=39.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 1, 0), point=(0, -19, 15), seat=-1, flip=True))
