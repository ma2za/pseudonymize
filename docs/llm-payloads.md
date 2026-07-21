# LLM payloads

`Pseudonymizer.process_data` recursively handles dictionaries, lists, and tuples while passing
primitive values through unchanged. Use path inclusion rules when only selected fields should be
processed. Tool arguments, tool outputs, retrieved documents, metadata, logs, and traces need the
same protection as chat content.
