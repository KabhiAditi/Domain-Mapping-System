import random
import json

FALLBACK_DOMAIN = "Generic"

def load_mapping(file_path="domain_mapping.json"):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def validate_mapping(mapping):
    if not mapping:
        return False, "Question generation blocked: domain mapping is empty."

    for domain, topics in mapping.items():
        if not topics:
            return False, f"Domain '{domain}' has no topics."

        for topic, subtopics in topics.items():
            if not subtopics:
                return False, f"Topic '{topic}' in domain '{domain}' has no subtopics."

    return True, "Mapping is valid."

def select_domain(mapping, requested_domain=None, random_mode=True, switch_prob=0.5):
    """
    random_mode: enables random switching across domains
    switch_prob: probability to ignore requested_domain
    """

    if not mapping:
        raise ValueError("Question generation blocked: domain mapping is empty.")

    domains = list(mapping.keys())

    if requested_domain is None:
        return random.choice(domains)

    if requested_domain in mapping:
        if random_mode and random.random() < switch_prob:
            # 🔁 randomly switch domain
            other_domains = [d for d in domains if d != requested_domain]
            return random.choice(other_domains)
        return requested_domain

    if FALLBACK_DOMAIN in mapping:
        return FALLBACK_DOMAIN

    return random.choice(domains)

def select_topic(mapping, domain):
    topics = list(mapping[domain].keys())
    return random.choice(topics)

def select_subtopic(mapping, domain, topic):
    subtopics = mapping[domain][topic]
    return random.choice(subtopics)

def generate_prompt(mapping, requested_domain=None, difficulty="medium",
                    random_mode=True, switch_prob=0.5):

    is_valid, message = validate_mapping(mapping)

    if not is_valid:
        return {
            "status": "blocked",
            "message": message
        }

    domain = select_domain(mapping, requested_domain, random_mode, switch_prob)
    topic = select_topic(mapping, domain)
    subtopic = select_subtopic(mapping, domain, topic)

    prompt = f"""
Generate one interview-style question.

Domain: {domain}
Topic: {topic}
Subtopic: {subtopic}
Difficulty: {difficulty}

The question must strictly belong to the selected domain, topic, and subtopic.
"""

    return {
        "status": "success",
        "domain": domain,
        "topic": topic,
        "subtopic": subtopic,
        "difficulty": difficulty,
        "prompt": prompt.strip()
    }

if __name__ == "__main__":
    mapping = load_mapping()
    result = generate_prompt(mapping, requested_domain="DSA", difficulty="medium")
    print(json.dumps(result, indent=2))
