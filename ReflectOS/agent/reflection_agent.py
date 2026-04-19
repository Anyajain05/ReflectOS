import argparse
import json
import re
from pathlib import Path


class ReflectionAgent:
    def __init__(self, tree_path: Path):
        data = json.loads(tree_path.read_text(encoding="utf-8"))
        self.meta = data["meta"]
        self.nodes = {node["id"]: node for node in data["nodes"]}
        self.answers = {}
        self.signals = {
            "axis1": {"internal": 0, "external": 0},
            "axis2": {"contribution": 0, "entitlement": 0},
            "axis3": {"self": 0, "other": 0},
        }
        self.history = []

    def dominant(self, axis: str) -> str:
        poles = self.signals[axis]
        items = list(poles.items())
        if items[0][1] == items[1][1]:
            return "mixed"
        return max(poles, key=poles.get)

    def dominant_label(self, axis: str) -> str:
        labels = {
            "axis1": {
                "internal": "internal",
                "external": "external",
                "mixed": "mixed"
            },
            "axis2": {
                "contribution": "contribution-oriented",
                "entitlement": "entitlement-leaning",
                "mixed": "mixed"
            },
            "axis3": {
                "self": "self-focused",
                "other": "other-oriented",
                "mixed": "mixed"
            }
        }
        return labels[axis][self.dominant(axis)]

    def summary_prompt(self) -> str:
        a1 = self.dominant("axis1")
        a2 = self.dominant("axis2")
        a3 = self.dominant("axis3")
        lookup = {
            ("internal", "contribution", "other"): "Repeat the smallest choice that helped both you and someone else",
            ("external", "entitlement", "self"): "Look for one action, one contribution, and one person beyond yourself before the day closes",
            ("internal", "entitlement", "self"): "Use your agency in service of contribution, not just self-protection",
            ("external", "contribution", "other"): "Keep the outward care, but anchor it in one clear choice that is yours",
        }
        return lookup.get((a1, a2, a3), "Notice one choice that is yours, one useful thing you can add, and one other person your work touches")

    def apply_signals(self, signal_list):
        for signal in signal_list or []:
            axis, pole = signal.split(":")
            self.signals[axis][pole] += 1

    def interpolate(self, text: str) -> str:
        def replace(match):
            key = match.group(1)
            if key.endswith(".answer"):
                node_id = key[:-7]
                return self.answers.get(node_id, "")
            if key == "axis1.dominantLabel":
                return self.dominant_label("axis1")
            if key == "axis2.dominantLabel":
                return self.dominant_label("axis2")
            if key == "axis3.dominantLabel":
                return self.dominant_label("axis3")
            if key == "summaryPrompt":
                return self.summary_prompt()
            return match.group(0)

        return re.sub(r"\{([^}]+)\}", replace, text)

    def route_decision(self, node):
        for rule in node["rules"]:
            condition = rule["if"]
            if condition.startswith("answer:"):
                left, values = condition.split(" in ")
                node_id = left.split(":", 1)[1]
                choices = [item.strip() for item in values.strip("[]").split(",")]
                if self.answers.get(node_id) in choices:
                    return rule["target"]
            elif condition.startswith("dominant:"):
                axis, expected = condition.split("=")
                axis = axis.split(":", 1)[1].strip()
                expected = expected.strip()
                if self.dominant(axis) == expected:
                    return rule["target"]
            elif condition.startswith("tie:"):
                axis = condition.split(":", 1)[1].strip()
                if self.dominant(axis) == "mixed":
                    return rule["target"]
        raise ValueError(f"No decision rule matched for node {node['id']}")

    def choose_option(self, node, scripted_choice=None):
        options = node["options"]
        if scripted_choice is not None:
            index = scripted_choice - 1
            if index < 0 or index >= len(options):
                raise ValueError(f"Choice {scripted_choice} out of range for {node['id']}")
            return options[index]

        print()
        for idx, option in enumerate(options, start=1):
            print(f"  {idx}. {option['label']}")
        while True:
            raw = input("Choose an option: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return options[int(raw) - 1]
            print("Please enter a valid number.")

    def run(self, scripted_choices=None, transcript=False):
        scripted_choices = scripted_choices or []
        scripted_index = 0
        current_id = self.meta["startNodeId"]

        while current_id:
            node = self.nodes[current_id]
            node_type = node["type"]
            text = self.interpolate(node.get("text", ""))

            if node_type in {"start", "reflection", "bridge", "summary", "end"}:
                print()
                print(text)
                self.history.append((node_type, text))
                if node_type == "end":
                    break
                current_id = node.get("target")
                continue

            if node_type == "question":
                print()
                print(text)
                choice_number = None
                if scripted_index < len(scripted_choices):
                    choice_number = scripted_choices[scripted_index]
                    scripted_index += 1
                option = self.choose_option(node, choice_number)
                self.answers[node["id"]] = option["label"]
                self.apply_signals(option.get("signal"))
                line = f"{text}\n> {option['label']}"
                self.history.append((node_type, line))
                print(f"> {option['label']}")
                current_id = option["target"]
                continue

            if node_type == "decision":
                current_id = self.route_decision(node)
                continue

            raise ValueError(f"Unsupported node type: {node_type}")

        if transcript:
            return "\n\n".join(entry for _, entry in self.history)
        return None


def main():
    parser = argparse.ArgumentParser(description="Run the deterministic daily reflection agent.")
    parser.add_argument(
        "--tree",
        default=str(Path(__file__).resolve().parents[1] / "tree" / "reflection-tree.json"),
        help="Path to the tree JSON file."
    )
    parser.add_argument(
        "--choices",
        nargs="*",
        type=int,
        help="Optional scripted numeric choices, one per question."
    )
    parser.add_argument(
        "--save-transcript",
        help="Optional file path to save the transcript."
    )
    args = parser.parse_args()

    agent = ReflectionAgent(Path(args.tree))
    transcript = agent.run(scripted_choices=args.choices, transcript=bool(args.save_transcript))

    if args.save_transcript:
        Path(args.save_transcript).write_text(transcript + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
