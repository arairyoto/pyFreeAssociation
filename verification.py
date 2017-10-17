from FreeAssociation import FreeAssociation

fa = FreeAssociation()

cue = "design"

associations = fa.associations(cue)

result = {}

for target in associations:
    fsg = fa.cue_to_target_strength(cue, target)
    result[target] = fsg

print(result)

second_associations = list(set(fa.associations(cue, step=2))-set(associations))

print(second_associations)
