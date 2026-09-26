from pathlib import Path
import json
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parent


# ============================================================
# Utility
# ============================================================

def write_text(path: Path, content: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"[CREATE] {path.relative_to(ROOT)}")


def write_json(path: Path, data):
    content = json.dumps(
        data,
        ensure_ascii=False,
        indent=2
    ) + "\n"

    write_text(path, content)


# ============================================================
# Directory structure
# ============================================================

DIRECTORIES = [
    "schema",
    "nodes",
    "experiments",
    "manifests",
    "evidence",
    "lineage",
    "ea",
    "scripts",
    "site",
    ".github/workflows",
]


def create_directories():
    print("\n=== Creating directories ===")

    for directory in DIRECTORIES:
        path = ROOT / directory
        path.mkdir(parents=True, exist_ok=True)
        print(f"[DIR]    {directory}")


# ============================================================
# protocol.json
# ============================================================

def create_protocol():

    protocol = {
        "protocol": "EA Evolution Ledger",
        "protocol_version": "0.1",
        "description": (
            "Lineage, mutation, experiment and evidence ledger "
            "for EA evolution."
        ),

        "node_model": {
            "unit": "EA_VERSION",
            "parent_type": "SINGLE_PARENT",
            "graph_type": "TREE"
        },

        "experiment_model": {
            "node_contains_multiple_experiments": True,
            "supported_types": [
                "backtest",
                "forward_test",
                "live_operation"
            ]
        },

        "decision_model": {
            "supported_decision_makers": [
                "human",
                "ai",
                "system",
                "hybrid"
            ],

            "supported_directions": [
                "buy",
                "sell",
                "both",
                "none",
                "unknown"
            ]
        },

        "mutation_model": {
            "type_is_label_only": True,
            "evaluation_is_actual_basis": True
        },

        "integrity": {
            "algorithm": "SHA-256"
        },

        "identity": {
            "node_id_prefix": "EL-EA-",
            "experiment_id_prefix": "EXP-"
        }
    }

    write_json(ROOT / "protocol.json", protocol)


# ============================================================
# JSON Schema
# ============================================================

def create_schema():

    schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",

        "title": "EA Evolution Ledger Node",

        "type": "object",

        "required": [
            "protocol_version",
            "node_id",
            "parent_id",
            "generation",
            "name",
            "status",
            "mutation",
            "experiments",
            "evaluation",
            "integrity",
            "created_at",
            "created_by"
        ],

        "properties": {

            "protocol_version": {
                "type": "string"
            },

            "node_id": {
                "type": "string",
                "pattern": "^EL-EA-[0-9]{6}$"
            },

            "parent_id": {
                "type": ["string", "null"]
            },

            "generation": {
                "type": "integer",
                "minimum": 0
            },

            "name": {
                "type": "string"
            },

            "status": {
                "type": "string",
                "enum": [
                    "experimental",
                    "active",
                    "archived",
                    "deprecated"
                ]
            },

            "mutation": {
                "type": "object",

                "required": [
                    "type",
                    "version"
                ],

                "properties": {

                    "type": {
                        "type": "string",
                        "enum": [
                            "original",
                            "logic",
                            "entry",
                            "exit",
                            "filter",
                            "risk_management",
                            "money_management",
                            "parameter",
                            "time_filter",
                            "symbol",
                            "timeframe",
                            "execution",
                            "optimization",
                            "architecture",
                            "ui",
                            "documentation",
                            "other"
                        ]
                    },

                    "version": {
                        "type": "string"
                    },

                    "source_experiment_id": {
                        "type": ["string", "null"]
                    }
                }
            },

            "experiments": {
                "type": "array",

                "items": {
                    "type": "object",

                    "required": [
                        "experiment_id",
                        "type",
                        "hypothesis",
                        "conditions",
                        "result"
                    ],

                    "properties": {

                        "experiment_id": {
                            "type": "string",
                            "pattern": "^EXP-[0-9]{6}$"
                        },

                        "type": {
                            "type": "string",
                            "enum": [
                                "backtest",
                                "forward_test",
                                "live_operation"
                            ]
                        },

                        "hypothesis": {
                            "type": "string"
                        },

                        "decision": {
                            "type": "object",

                            "properties": {

                                "decision_maker": {
                                    "type": "string",
                                    "enum": [
                                        "human",
                                        "ai",
                                        "system",
                                        "hybrid"
                                    ]
                                },

                                "direction": {
                                    "type": "string",
                                    "enum": [
                                        "buy",
                                        "sell",
                                        "both",
                                        "none",
                                        "unknown"
                                    ]
                                },

                                "reason": {
                                    "type": "string"
                                }
                            }
                        },

                        "conditions": {
                            "type": "object"
                        },

                        "result": {
                            "type": "object"
                        },

                        "evidence": {
                            "type": "array"
                        },

                        "conclusion": {
                            "type": "string"
                        }
                    }
                }
            },

            "evaluation": {
                "type": "object",

                "properties": {

                    "evaluation_version": {
                        "type": "string"
                    },

                    "baseline_node_id": {
                        "type": ["string", "null"]
                    },

                    "baseline": {
                        "type": "object"
                    },

                    "child": {
                        "type": "object"
                    },

                    "delta": {
                        "type": "object"
                    }
                }
            },

            "integrity": {
                "type": "object",

                "properties": {

                    "source_hash": {
                        "type": ["string", "null"]
                    },

                    "binary_hash": {
                        "type": ["string", "null"]
                    },

                    "manifest_hash": {
                        "type": ["string", "null"]
                    }
                }
            },

            "created_at": {
                "type": "string"
            },

            "created_by": {
                "type": "string"
            }
        }
    }

    write_json(
        ROOT / "schema" / "node.schema.json",
        schema
    )


# ============================================================
# Sample Node
# ============================================================

def make_node(
    node_id,
    parent_id,
    generation,
    name,
    mutation_type,
    experiment_id,
    direction="buy"
):

    now = datetime.now(timezone.utc).isoformat()

    return {
        "protocol_version": "0.1",

        "node_id": node_id,

        "parent_id": parent_id,

        "generation": generation,

        "name": name,

        "status": "experimental",

        "mutation": {
            "type": mutation_type,
            "version": "1",
            "source_experiment_id": (
                experiment_id if parent_id else None
            )
        },

        "experiments": [
            {
                "experiment_id": experiment_id,

                "type": "live_operation",

                "hypothesis": (
                    "Initial experimental operation."
                ),

                "decision": {
                    "decision_maker": "human",
                    "direction": direction,
                    "reason": (
                        "Sample data generated by init.py."
                    )
                },

                "conditions": {
                    "environment": "Demo",
                    "symbol": "EURUSD",
                    "timeframe": "M15",
                    "initial_balance": 100000
                },

                "result": {
                    "status": "inconclusive"
                },

                "evidence": [],

                "conclusion": (
                    "Sample experiment."
                )
            }
        ],

        "evaluation": {
            "evaluation_version": "0.1",

            "baseline_node_id": parent_id,

            "baseline": {},

            "child": {},

            "delta": {}
        },

        "integrity": {
            "source_hash": None,
            "binary_hash": None,
            "manifest_hash": None
        },

        "created_at": now,

        "created_by": "init.py"
    }


def create_sample_nodes():

    print("\n=== Creating sample nodes ===")

    nodes = [
        make_node(
            "EL-EA-000001",
            None,
            0,
            "Original EA",
            "original",
            "EXP-000001"
        ),

        make_node(
            "EL-EA-000002",
            "EL-EA-000001",
            1,
            "Entry Mutation",
            "entry",
            "EXP-000002"
        ),

        make_node(
            "EL-EA-000003",
            "EL-EA-000001",
            1,
            "Filter Mutation",
            "filter",
            "EXP-000003"
        ),

        make_node(
            "EL-EA-000004",
            "EL-EA-000002",
            2,
            "Risk Management Mutation",
            "risk_management",
            "EXP-000004"
        ),

        make_node(
            "EL-EA-000005",
            "EL-EA-000002",
            2,
            "Parameter Mutation",
            "parameter",
            "EXP-000005"
        )
    ]

    for node in nodes:

        path = (
            ROOT
            / "nodes"
            / f"{node['node_id']}.json"
        )

        write_json(path, node)


# ============================================================
# EA EvolutionLedger.mqh
# ============================================================

def create_ea_files():

    print("\n=== Creating EA metadata files ===")

    node_ids = [
        "EL-EA-000001",
        "EL-EA-000002",
        "EL-EA-000003",
        "EL-EA-000004",
        "EL-EA-000005"
    ]

    for node_id in node_ids:

        content = f"""//+------------------------------------------------------------------+
//| EvolutionLedger.mqh                                             |
//| EA Evolution Ledger                                             |
//+------------------------------------------------------------------+

#ifndef __EVOLUTION_LEDGER_MQH__
#define __EVOLUTION_LEDGER_MQH__

#define EL_PROTOCOL_VERSION "0.1"

#define EL_NODE_ID "{node_id}"

#define EL_PARENT_ID ""

#define EL_MUTATION_TYPE "experimental"

#define EL_MUTATION_VERSION "1"

#define EL_MANIFEST_HASH ""

#define EL_LICENSE_ID ""

#define EL_LEDGER_URL ""

#endif
"""

        path = (
            ROOT
            / "ea"
            / node_id
            / "EvolutionLedger.mqh"
        )

        write_text(path, content)


# ============================================================
# Lineage
# ============================================================

def create_lineage():

    print("\n=== Creating lineage index ===")

    nodes = []

    for path in sorted(
        (ROOT / "nodes").glob("*.json")
    ):

        data = json.loads(
            path.read_text(encoding="utf-8")
        )

        nodes.append({
            "node_id": data["node_id"],
            "parent_id": data["parent_id"],
            "generation": data["generation"],
            "name": data["name"],
            "status": data["status"],
            "mutation_type": data["mutation"]["type"]
        })

    lineage = {
        "protocol_version": "0.1",
        "nodes": nodes
    }

    write_json(
        ROOT / "lineage" / "index.json",
        lineage
    )


# ============================================================
# Validation script
# ============================================================

def create_validate_script():

    content = r'''from pathlib import Path
import json
import sys

try:
    import jsonschema
except ImportError:
    print("jsonschema is not installed.")
    print("Run: pip install jsonschema")
    sys.exit(1)


ROOT = Path(__file__).resolve().parents[1]

schema_path = ROOT / "schema" / "node.schema.json"

schema = json.loads(
    schema_path.read_text(encoding="utf-8")
)

errors = 0

for path in sorted(
    (ROOT / "nodes").glob("*.json")
):

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    try:
        jsonschema.validate(
            instance=data,
            schema=schema
        )

        print(f"[OK] {path.name}")

    except jsonschema.ValidationError as e:

        print(f"[ERROR] {path.name}")
        print(e.message)

        errors += 1


if errors:
    print(f"\nValidation failed: {errors} error(s)")
    sys.exit(1)

print("\nAll nodes are valid.")
'''

    write_text(
        ROOT / "scripts" / "validate_nodes.py",
        content
    )


# ============================================================
# Hash generator
# ============================================================

def create_hash_script():

    content = r'''from pathlib import Path
import hashlib
import sys


def sha256_file(path):

    h = hashlib.sha256()

    with path.open("rb") as f:

        while True:

            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return "sha256:" + h.hexdigest()


if len(sys.argv) != 2:

    print("Usage:")
    print("python generate_hash.py <file>")

    sys.exit(1)


path = Path(sys.argv[1])

if not path.exists():

    print(f"File not found: {path}")

    sys.exit(1)


print(sha256_file(path))
'''

    write_text(
        ROOT / "scripts" / "generate_hash.py",
        content
    )


# ============================================================
# Manifest generator
# ============================================================

def create_manifest_script():

    content = r'''from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone


ROOT = Path(__file__).resolve().parents[1]

EA_ROOT = ROOT / "ea"

MANIFEST_ROOT = ROOT / "manifests"


def sha256_file(path):

    h = hashlib.sha256()

    with path.open("rb") as f:

        while True:

            chunk = f.read(1024 * 1024)

            if not chunk:
                break

            h.update(chunk)

    return "sha256:" + h.hexdigest()


for node_dir in sorted(EA_ROOT.iterdir()):

    if not node_dir.is_dir():
        continue

    node_id = node_dir.name

    files = []

    for path in sorted(node_dir.rglob("*")):

        if not path.is_file():
            continue

        files.append({
            "path": str(
                path.relative_to(node_dir)
            ).replace("\\", "/"),

            "sha256": sha256_file(path)
        })

    manifest = {

        "protocol_version": "0.1",

        "node_id": node_id,

        "generated_at":
            datetime.now(timezone.utc).isoformat(),

        "files": files
    }

    output = (
        MANIFEST_ROOT
        / node_id
        / "manifest.json"
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    output.write_text(
        json.dumps(
            manifest,
            ensure_ascii=False,
            indent=2
        ) + "\n",
        encoding="utf-8"
    )

    print(f"[MANIFEST] {node_id}")
'''

    write_text(
        ROOT / "scripts" / "generate_manifest.py",
        content
    )


# ============================================================
# Lineage generator script
# ============================================================

def create_lineage_script():

    content = r'''from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]

nodes = []

for path in sorted(
    (ROOT / "nodes").glob("*.json")
):

    data = json.loads(
        path.read_text(encoding="utf-8")
    )

    nodes.append({
        "node_id": data["node_id"],
        "parent_id": data["parent_id"],
        "generation": data["generation"],
        "name": data["name"],
        "status": data["status"],
        "mutation_type":
            data["mutation"]["type"]
    })


output = ROOT / "lineage" / "index.json"

output.write_text(
    json.dumps(
        {
            "protocol_version": "0.1",
            "nodes": nodes
        },
        ensure_ascii=False,
        indent=2
    ) + "\n",
    encoding="utf-8"
)

print("[LINEAGE] generated")
'''

    write_text(
        ROOT / "scripts" / "generate_lineage.py",
        content
    )


# ============================================================
# GitHub Actions
# ============================================================

def create_github_actions():

    content = """name: Evolution Ledger

on:
  push:
    branches:
      - main

  pull_request:
    branches:
      - main

jobs:

  validate-and-build:

    runs-on: ubuntu-latest

    steps:

      - name: Checkout
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install dependencies
        run: |
          pip install jsonschema

      - name: Validate Nodes
        run: |
          python scripts/validate_nodes.py

      - name: Generate Manifests
        run: |
          python scripts/generate_manifest.py

      - name: Generate Lineage
        run: |
          python scripts/generate_lineage.py

      - name: Show generated files
        run: |
          git status
"""

    write_text(
        ROOT
        / ".github"
        / "workflows"
        / "evolution-ledger.yml",
        content
    )


# ============================================================
# README
# ============================================================

def create_readme():

    content = """# EA Evolution Ledger

EAの進化を記録するためのEvolution Ledger。

## Concept

Evolution Ledger records:

- EA versions
- parent / child lineage
- mutations
- experiments
- results
- evidence
- evaluation
- integrity hashes

The goal is not simply to rank EAs.

The goal is to preserve:

> what was created,
> what was tried,
> what failed,
> what remained,
> and what was inherited.

## Structure

```text
schema/
nodes/
experiments/
manifests/
evidence/
lineage/
ea/
scripts/
site/
.github/
