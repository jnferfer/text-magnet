
SIDEBAR_LOGO = """
    <style>
        [data-testid=stImage]{
            text-align: center;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
    </style>
"""

SIDEBAR_TEXT = "<center><h2>{}</h2><p style='line-height: 1.3;'>{}<br><br><em>{}</em></p><br></center>"

TEXT = "line-height: 2.5; padding-right: 15px; overflow-y: scroll; max-height:450px;"

HIGHLIGHTED_SENT = "background-color: #cde8f7"

TEXT_HYPERLINK = "text-decoration: underline dotted; color: #262730;"

NODE = {
    "size": 11,
    "color": {
        "central": "#cbddf7",
        "intermediate": {
            "EQUIVALENT": "#ADD8E6",
            "CAUSE_IS": "#FFA07A",
            "CONSEQUENCE_IS": "#90EE90",
            "SIMILARLY": "#FFFFE0",
            "ADDITIONALLY": "#E6E6FA",
            "FOR_EXAMPLE": "#FFDAB9",
            "INTERVENTION_IS": "#FFB6C1",
            "THE_OPPOSITE_IS": "#D3D3D3"
        },
        "end": {
            "EQUIVALENT": "#00008B",
            "CAUSE_IS": "#8B0000",
            "CONSEQUENCE_IS": "#006400",
            "SIMILARLY": "#FFD700",
            "ADDITIONALLY": "#800080",
            "FOR_EXAMPLE": "#FF8C00",
            "INTERVENTION_IS": "#FF1493",
            "THE_OPPOSITE_IS": "#A9A9A9"
        }
    },
    "relation_label": {
        "EQUIVALENT": "EQUIVALENTS",
        "CAUSE_IS": "CAUSES",
        "CONSEQUENCE_IS": "CONSEQUENCES",
        "SIMILARLY": "SIMILARITIES",
        "ADDITIONALLY": "ADDITIONALLY",
        "FOR_EXAMPLE": "EXAMPLES",
        "INTERVENTION_IS": "INTERVENTIONS",
        "THE_OPPOSITE_IS": "OPPOSITES"
    }
}

GOAL_TEXT = "padding-left:20px; line-height: 1.6;"

GOAL_DOT = "color: {}; line-height:0.5; font-size:30px;"

