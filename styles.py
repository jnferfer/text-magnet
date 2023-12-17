
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

SIDEBAR_TEXT = "<center><h2>{}</h2><p style='line-height: 1.3;'><b>{}</b></p></center>"

TEXT = "line-height: 2.5; padding-right: 15px; overflow-y: scroll; max-height:450px;"

HIGHLIGHTED_SENT = "background-color: #cde8f7"

TEXT_HYPERLINK = "text-decoration: underline; text-decoration-thickness: 0.2px; color: #262730;"

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


def generate_goal_head(color, node_label):
    return f"""
<style>
    @keyframes blink {{
        0% {{color: transparent;}}
        50% {{color: {color};}}
        100% {{color: transparent;}}
    }}
    #blinking {{
        animation: blink 3s linear infinite;
        font-size: 33px;
        padding-left: 20px;
        vertical-align: middle;
        line-height: 0.5;
    }}
    #text {{
        font-size: 16px;
        font-family: 'Arial', sans-serif;
        vertical-align: middle;
    }}
</style>
<p><span id="blinking">●</span><span id="text"> {node_label}</span></p>
"""

