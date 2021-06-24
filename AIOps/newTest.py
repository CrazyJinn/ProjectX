import neo4j_helper as nh

graph = nh.get_graph()

nh.set_interface_error_flag(graph, "Customer/GetCustomerWithExemptCVV2", 0.3)
