def some_parameter_processing_function(p):
	if p.type == COLLECTION:
		for elem in p.content:
			some_parameter_processing_function(elem)
	process_parameter(p)