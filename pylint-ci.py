import argparse
import json

parser = argparse.ArgumentParser(
    prog="PylintReportConverter",
    description="Convert pylint report to the Code Climate format",
)

parser.add_argument("pylint_report", help="pylint report")
parser.add_argument("output", help="outputfile")


SEVERITY_MAP = {
    "fatal": "blocker",
    "error": "critical",
    "warning": "major",
    "convention": "minor",
    "refactor": "minor",
    "info": "info",
    "statement": "info",
}


def convert_pylint_report(
    report_entries: list[dict[str, str]]
) -> list[dict[str, str | dict]]:
    return [convert_entry(e) for e in report_entries]


def convert_entry(entry: dict[str, str]) -> dict[str, str | dict]:
    return {
        "description": f"{entry['message-id']} - {entry['message']}",
        "check_name": entry["symbol"],
        "fingerprint": hash_entry(entry),
        "severity": SEVERITY_MAP[entry["type"]],
        "location": {
            "path": get_abs_path(entry),
            "lines": {"begin": entry["line"]},
        },
    }


def hash_entry(entry: dict[str, str]) -> str:
    from hashlib import md5

    msg = f"{entry['module']}:{entry['line']} - {entry['message-id']}"
    return md5(msg.encode()).hexdigest()


def get_abs_path(entry: dict[str, str]) -> str:
    import os

    return os.path.join("stufidev", entry["path"])


def map_severity(entry: dict[str, str]) -> str:
    return entry["type"]


if __name__ == "__main__":
    args = parser.parse_args()

    with open(args.pylint_report, "r") as inp, open(args.output, "w") as out:
        entries = json.loads(inp.read())
        out.write(json.dumps(convert_pylint_report(entries), indent=2))

    print("Done")
