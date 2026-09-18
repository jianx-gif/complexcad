parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(0, 0, 75), seat=4, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 8, 0), axis=(0, 0, 1), point=(0, 0, 75), seat=4.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(0, 0, 75), seat=-4, flip=True))
