TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "search_restaurant_information",
            "description": "Search restaurant information such as opening hours, menu, reservation policy, cancellation policy, and contact details.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user question or search query.",
                    }
                },
                "required": ["query"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check whether a table is available for a given date, time, and number of guests.",
            "parameters": {
                "type": "object",
                "properties": {
                    "booking_date": {
                        "type": "string",
                        "description": "Booking date in YYYY-MM-DD format.",
                    },
                    "booking_time": {
                        "type": "string",
                        "description": "Booking time in HH:MM format.",
                    },
                    "guests": {
                        "type": "integer",
                        "description": "Number of guests.",
                    },
                },
                "required": ["booking_date", "booking_time", "guests"],
                "additionalProperties": False,
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "create_booking",
            "description": "Create a restaurant booking after collecting customer name, contact number, date, time, and guest count.",
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_name": {
                        "type": "string",
                        "description": "Customer full name.",
                    },
                    "contact_number": {
                        "type": "string",
                        "description": "Customer phone number.",
                    },
                    "booking_date": {
                        "type": "string",
                        "description": "Booking date in YYYY-MM-DD format.",
                    },
                    "booking_time": {
                        "type": "string",
                        "description": "Booking time in HH:MM format.",
                    },
                    "guests": {
                        "type": "integer",
                        "description": "Number of guests.",
                    },
                },
                "required": [
                    "customer_name",
                    "contact_number",
                    "booking_date",
                    "booking_time",
                    "guests",
                ],
                "additionalProperties": False,
            },
        },
    },
]
