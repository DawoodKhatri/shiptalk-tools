response_format = {
    "type": "json_schema",
    "json_schema": {
            "name": "shiptalk_just_in_time_inventory_tool_response",
            "schema": {
                "type": "object",
                "properties": {
                    "results": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "description": {"type": "string"},
                                "chartType": {"type": "string", "enum": ["barChart", "lineChart", "pieChart"]},
                                "plotData": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "label": {"type": "string"},
                                            "value": {"type": "number"}
                                        },
                                        "required": ["label", "value"],
                                        "additionalProperties": False
                                    }
                                },
                                "conclusion": {"type": "string"}
                            },
                            "required": ["description", "chartType", "plotData", "conclusion"],
                            "additionalProperties": False
                        }
                    }
                },
                "required": ["results"],
                "additionalProperties": False
            },
        "strict": True
    },
}
