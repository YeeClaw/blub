class Private:

    with open("secret_sauce.csv") as secretFile:
        next(secretFile)
        for line in secretFile:
            line.strip()
            columns = line.split(",")

            token = columns[0]
            ip = columns[1]
