import json
from pathlib import Path

def matches(facts, conditions):
    """A rule matches only when every condition is satisfied."""
    for name, condition in conditions.items():
        if name not in facts:
            return False
        actual = facts[name]

        # Simple conditions, such as ingredients_available = True.
        if not isinstance(condition, dict):
            if actual != condition:
                return False
            continue

        # Numeric conditions compare with a fixed value or another fact.
        if "fact" in condition:
            other_name = condition["fact"]
            if other_name not in facts:
                return False
            expected = facts[other_name]
        else:
            expected = condition["value"]

        operation = condition["op"]
        if operation == "eq":
            satisfied = actual == expected
        elif operation == "gt":
            satisfied = actual > expected
        elif operation == "le":
            satisfied = actual <= expected
        else:
            raise ValueError("Unknown comparison: " + operation)

        if not satisfied:
            return False
    return True


def infer(facts, rules):
    """Apply matching rules until no further conclusions can be added."""
    facts = dict(facts)
    trace = []
    fired = set()
    while True:
        changed = False
        for rule in rules:
            if rule["id"] in fired:
                continue
            if matches(facts, rule["when"]):
                fired.add(rule["id"])
                for key, value in rule["then"].items():
                    if key in facts and facts[key] != value:
                        raise ValueError("Conflicting conclusion for " + key)
                    if key not in facts:
                        facts[key] = value
                        changed = True
                trace.append(rule)
        if not changed:
            return facts, trace


def ask(question):
    while True:
        answer = input(question + " [y/n]: ").strip().lower()
        if answer in {"y", "yes", "n", "no"}:
            return answer in {"y", "yes"}
        print("Please enter y or n.")


def ask_number(question):
    while True:
        try:
            value = int(input(question + ": ").strip())
            if value >= 0:
                return value
        except ValueError:
            pass
        print("Please enter a whole number of zero or more.")


def main():
    kb = json.loads(Path(__file__).with_name("knowledge_base.json").read_text())
    print("Café Shift Advisor (prototype)")
    print("\nDecision: should we start preparing another cake?\n")
    facts = {}
    for question in kb["questions"]:
        if question.get("type") == "number":
            answer = ask_number(question["text"])
        else:
            answer = ask(question["text"])
        facts[question["fact"]] = answer
        conclusions, trace = infer(facts, kb["rules"])
        recommendations = []
        for item in kb["recommendations"]:
            if conclusions.get(item["fact"]) is True:
                recommendations.append(item["text"])
        if recommendations:
            break

    print("\nRecommendations:")
    for recommendation in recommendations:
        print("-", recommendation)
    if not recommendations:
        print("- No recommendation: this situation is outside the prototype's rules.")
    print("\nReasoning (rules used):")
    for rule in trace:
        print("-", rule["id"] + ":", rule["explanation"])
    if not trace:
        print("- No rules matched.")


if __name__ == "__main__":
    main()
