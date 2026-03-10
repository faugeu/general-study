"""Global subcriteria weights from criteria and local subcriteria weights."""


def compute_global_subcriteria_weights(criteria_weights, local_sub_weights):
    global_weights = {}

    for criterion, c_weight in criteria_weights.items():
        for sub, s_weight in local_sub_weights[criterion].items():
            global_weights[sub] = c_weight * s_weight

    total = sum(global_weights.values())
    global_weights = {k: v / total for k, v in global_weights.items()}
    return global_weights
