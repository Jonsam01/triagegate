from router import route_decision

high_confidence = {"confidence": 0.95}
low_confidence = {"confidence": 0.4}
edge_case = {"confidence": 0.80}

print(route_decision(high_confidence))  # expect: auto_resolved
print(route_decision(low_confidence))   # expect: escalated
# expect: auto_resolved (boundary is inclusive)
print(route_decision(edge_case))
