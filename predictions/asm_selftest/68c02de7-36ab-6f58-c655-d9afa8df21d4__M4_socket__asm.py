parts = [base]
parts.append(place(fastener("washer", 'M4', 0), axis=(0, 0, 1), point=(5, 0, 34), seat=34, flip=False))
parts.append(place(fastener("screw", 'M4-0.7', 74, 0), axis=(0, 0, 1), point=(5, 0, 34), seat=34.9, flip=False))
parts.append(place(fastener("nut", 'M4-0.7', 'M4', 0), axis=(0, 0, 1), point=(5, 0, 34), seat=-34, flip=True))
