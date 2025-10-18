import re
from dataclasses import dataclass

@dataclass
class RouteDecision:
    index: str
    filters: dict

def decide_route(query: str) -> RouteDecision:
    q = query.lower()
    # very light heuristics
    if any(k in q for k in ["style", "artistic", "brush", "painterly", "impressionist"]):
        return RouteDecision(index="art_text_artistic", filters={})
    if any(k in q for k in ["mood", "feeling", "romantic", "mysterious", "calm", "serene", "happy", "sad", "blue"]):
        return RouteDecision(index="art_mood", filters={})
    if any(k in q for k in ["color", "palette", "hue"]):
        return RouteDecision(index="art_image", filters={})
    # default: literal captions
    return RouteDecision(index="art_text_literal", filters={})
