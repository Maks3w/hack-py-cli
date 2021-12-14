def before_scenario(context, scenario):
    context.account = None
    context.exception = None
    context.tx_index = 0
