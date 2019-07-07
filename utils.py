def handleArgs(args):
    argc = len(args)
    if argc > 1:
        period = args[1]
    else:
        print("Missing input for short vs long term forecast...")
    if argc > 2:
        limit = int(args[2])
    else:
        print("Missing input for limit on wind force...")
    if argc > 3:
        enable_slack = True
    else:
        enable_slack = False
    return period, limit, enable_slack
