import os
import json
from datetime import datetime
from openai import OpenAI

PLAN_SCHEMA = {
    "name": "exercise_plan",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,  # ⭐ 必须
        "properties": {
            "exerciseTheme": {"type": "string"},
            "classes": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,  # ⭐ 必须
                    "properties": {
                        "name": {"type": "string"},
                        "type": {"type": "string"},
                        "file": {"type": "string"},
                        "package": {"type": "string"},
                        "methods": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                    "implements": {
                        "type": ["array", "null"],
                        "items": {"type": "string"}
                    },

                    "extends": {
                        "type": ["string", "null"]
                    },
                        "providedToStudent": {"type": "boolean"}
                    },
                    "required": [
                        "name",
                        "type",
                        "file",
                        "package",
                        "methods",
                        "implements",
                        "extends",
                        "providedToStudent"
                    ]
                }
            },
            "designPatterns": {
                "type": ["array", "null"],
                "items": {"type": "string"}
            },
            "studentTodos": {"type": "number"},
            "estimatedSolutionLOC": {"type": "number"},
            "testClasses": {
                "type": ["array", "null"],
                "items": {
                    "type": "object",
                    "additionalProperties": False,  # ⭐ 必须
                    "properties": {
                        "name": {"type": "string"},
                        "file": {"type": "string"},
                        "testMethods": {
                            "type": "array",
                            "items": {"type": "string"}
                        }
                    },
                    "required": ["name", "file", "testMethods"]
                }
            },
            "coveredCompetencies": {
                "type": ["array", "null"],
                "items": {"type": "string"}
            },
            "coveredPrerequisites": {
                "type": ["array", "null"],
                "items": {"type": "string"}
            }
        },
        "required": [
            "exerciseTheme",
            "classes",
            "designPatterns",          # ⭐ 加
            "studentTodos",
            "estimatedSolutionLOC",
            "testClasses",
            "coveredCompetencies",     # ⭐ 加
            "coveredPrerequisites"     # ⭐ 加
        ]
    }
}


TEMPLATE_SCHEMA = {
    "name": "generated_files",
    "strict": True,
    "schema": {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "files": {
                "type": "array",
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "path": {"type": "string"},
                        "content": {"type": "string"}
                    },
                    "required": ["path", "content"]
                }
            }
        },
        "required": ["files"]
    }
}

# ===== 读取 config.json =====
def load_config(path="config.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

config = load_config()

# ===== 初始化 client =====
client = OpenAI(api_key=config["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"  # 

OUTPUT_DIR = "logs"
os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================
# SYSTEM PROMPTS（严格对齐JS）
# =========================
SYSTEM_PROMPT_PLAN = """You are an expert Java programming exercise architect for university courses.
You respond ONLY with valid JSON matching the ExercisePlan schema.
Design a clear, well-structured exercise architecture before any code is generated."""

SYSTEM_PROMPT_TEMPLATE = """You are an expert Java programming exercise generator for university courses.
You respond ONLY with valid JSON containing a "files" array.
Each file has "path" (relative) and "content" (full file content) fields.
Do NOT include build.gradle, .gitignore, or configuration files.
For each method that requires implementation:
- Add a TODO comment describing what needs to be implemented
- The TODO should be concrete and task-oriented
- Do NOT include the solution
- Do NOT reference abstract programming concepts explicitly

"""


# =========================
# UTILS
# =========================
def save_log(step, prompt, response, timestamp):
    base = f"{OUTPUT_DIR}/{timestamp}_{step}"

    # 保存 prompt
    with open(f"{base}_prompt.txt", "w", encoding="utf-8") as f:
        f.write(prompt)

    # 保存 response（JSON 格式）
    try:
        parsed = json.loads(response)
        with open(f"{base}_response.json", "w", encoding="utf-8") as f:
            json.dump(parsed, f, indent=2, ensure_ascii=False)
    except Exception:
        # fallback（如果解析失败）
        with open(f"{base}_response.txt", "w", encoding="utf-8") as f:
            f.write(response)


def call_llm(system_prompt, user_prompt, schema, max_tokens=2000):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        response_format={
            "type": "json_schema",
            "json_schema": schema
        },
        max_completion_tokens=max_tokens,
    )

    content = response.choices[0].message.content

    if content is None:
        raise ValueError(f"Empty response: {response}")

    try:
        parsed = json.loads(content)
    except Exception:
        raise ValueError(f"JSON parse failed:\n{content}")

    return parsed, content


def load_competency_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

# =========================
# STEP 1: PLANNING
# =========================
def generate_plan(prompt: str, timestamp: str):
    parsed, raw = call_llm(
        SYSTEM_PROMPT_PLAN,
        prompt,
        PLAN_SCHEMA
    )
    save_log("planning", prompt, raw, timestamp)
    return parsed


# =========================
# STEP 2: TEMPLATE GENERATION
# =========================
def generate_template(prompt: str, timestamp: str):
    parsed, raw = call_llm(
        SYSTEM_PROMPT_TEMPLATE,
        prompt,
        TEMPLATE_SCHEMA,
        max_tokens=4000
    )
    save_log("template", prompt, raw, timestamp)
    return parsed


# =========================
# utils for prompt builders
# =========================
def build_competency_registry(competency_dict):
    registry = {}

    def add(label, description, taxonomy=None):
        if label not in registry:
            registry[label] = {
                "description": description,
                "taxonomy": set()
            }

        if taxonomy:
            registry[label]["taxonomy"].update(taxonomy)

    def traverse_dep(dep):
        add(dep["label"], dep["description"], dep.get("taxonomy", []))

        for sub in dep.get("sub_dependencies", []):
            traverse_dep(sub)

    for _, comp in competency_dict.items():
        add(comp["title"], comp["description"], comp.get("taxonomy", []))

        for dep in comp.get("dependencies", []):
            traverse_dep(dep)

    # 转回 list
    for k in registry:
        registry[k]["taxonomy"] = list(registry[k]["taxonomy"])

    return registry


def collect_prerequisites(competency_dict, registry):
    result = {}

    def traverse(dep):
        label = dep["label"]
        if label not in result:
            result[label] = registry[label]  # ⭐ 从 registry 取完整信息

        for sub in dep.get("sub_dependencies", []):
            traverse(sub)

    for _, comp in competency_dict.items():
        for dep in comp.get("dependencies", []):
            traverse(dep)

    return result


def collect_main_competencies(competency_dict, registry):
    result = {}

    for _, comp in competency_dict.items():
        label = comp["title"]
        result[label] = registry[label]

    return result


def collect_all_competencies(competency_dict):
    result = {}

    def add_comp(label, description, taxonomy=None):
        if label not in result:
            result[label] = {
                "description": description,
                "taxonomy": taxonomy or []
            }

    def traverse_dep(dep):
        add_comp(dep["label"], dep["description"])
        for sub in dep.get("sub_dependencies", []):
            traverse_dep(sub)

    for _, comp in competency_dict.items():
        add_comp(comp["title"], comp["description"], comp.get("taxonomy", []))

        for dep in comp.get("dependencies", []):
            traverse_dep(dep)

    return result

def collect_dependencies(competency_dict):
    relations = set()  # ⭐ 用 set 自动去重

    def traverse(parent_label, dep):
        for rel in dep.get("relations", []):
            relations.add((parent_label, rel, dep["label"]))

        for sub in dep.get("sub_dependencies", []):
            for rel in sub.get("relations", []):
                relations.add((dep["label"], rel, sub["label"]))
            traverse(dep["label"], sub)

    for _, comp in competency_dict.items():
        parent = comp["title"]
        for dep in comp.get("dependencies", []):
            traverse(parent, dep)

    return sorted(list(relations))  # ⭐ 可选排序（稳定输出）

def format_competency_section(comp_map):
    text = ""
    for label, data in comp_map.items():
        taxonomy = ", ".join(data.get("taxonomy", [])) or "N/A"
        text += f"- {label}\n"
        text += f"  Taxonomy: {taxonomy}\n"
        text += f"  Description: {data['description']}\n\n"
    return text


def format_dependencies(relations, main_comp_labels):
    group1 = []
    group2 = []

    for a, rel, b in relations:
        if a in main_comp_labels:
            group1.append((a, rel, b))
        else:
            group2.append((a, rel, b))

    # 可选：各组内部排序（稳定输出）
    group1.sort()
    group2.sort()

    ordered = group1 + group2

    return "\n".join([f"{a} [{rel}] {b}" for a, rel, b in ordered])

# =========================
# PROMPT BUILDERS
# =========================
def build_planning_prompt_kg(competency_json, metadata, config):
    
    exercise_type = metadata.get("exerciseType", "medium")
    safe_title = metadata.get("title", "")
    safe_package = metadata.get("packageName", "")
    safe_additional = metadata.get("additionalRequirements", "")

    # ⭐ 数据处理
    registry = build_competency_registry(competency_json)
    main_comps = collect_main_competencies(competency_json, registry)
    prereqs = collect_prerequisites(competency_json, registry)
    main_text = format_competency_section(main_comps)
    prereq_text = format_competency_section(prereqs)
    relations = collect_dependencies(competency_json)
    main_labels = set(main_comps.keys())
    rel_text = format_dependencies(relations, main_labels)

    return f"""
You are planning a Java programming exercise. Output ONLY valid JSON matching this schema, no markdown, no explanation.

## Dependency Constraints (MANDATORY)

The exercise MUST:
- Cover all prerequisite competencies required for the target competencies
- Not omit any required prerequisite
- Ensure that all dependencies are satisfied before advanced concepts are used
- Each prerequisite MUST be explicitly demonstrated in the code structure or behavior

The exercise MUST NOT:
- Use any concept that is not included in the listed competencies or their prerequisites
- Introduce advanced concepts without their prerequisites being covered

## Validation Requirement

You MUST explicitly list:
- All competencies covered in the exercise
- All prerequisite competencies that are required and covered

## Exercise Type: {config['label']} ({exercise_type})

Targets:
- Classes: {config['targetClasses']}
- Student TODOs: {config['targetTodos']}
- Test methods: {config['targetTests']}
- Solution LOC range: {config['targetLOC']}

## Exercise Context

- **Title**: {safe_title}
- **Package**: {safe_package}

### Competencies

{main_text}

### Prerequisites

{prereq_text}

### Competency Dependencies

{rel_text}

{f"### Additional Requirements\n{safe_additional}\n" if safe_additional else ""}

## Required JSON Schema

{{
  "exerciseTheme": "string — a brief thematic description",
  "classes": [
    {{
      "name": "string — class name",
      "type": "class | interface | enum | abstract class | record",
      "file": "string — relative file path",
      "package": "string — Java package",
      "methods": ["string — method signatures"],
      "implements": ["string — interface names (optional)"],
      "extends": "string — parent class (optional)",
      "providedToStudent": "boolean"
    }}
  ],
  "designPatterns": ["string"],
  "studentTodos": "number — choose a value within target range",
  "estimatedSolutionLOC": "number",
  "testClasses": [
    {{
      "name": "string",
      "file": "string",
      "testMethods": ["string"]
    }}
  ],
  "coveredCompetencies": ["string"],
  "coveredPrerequisites": ["string"]
}}

Output ONLY the JSON object. No markdown fences, no commentary.
"""


def build_planning_prompt_nl(description, metadata, config):

    exercise_type = metadata.get("exerciseType", "medium")
    safe_title = metadata.get("title", "")
    safe_package = metadata.get("packageName", "")
    safe_additional = metadata.get("additionalRequirements", "")

    return f"""
You are planning a Java programming exercise. Output ONLY valid JSON matching this schema, no markdown, no explanation.

## Dependency Constraints (MANDATORY)

The exercise MUST:
- Cover all prerequisite competencies required for the target competencies
- Not omit any required prerequisite
- Ensure that all dependencies are satisfied before advanced concepts are used
- Each prerequisite MUST be explicitly demonstrated in the code structure or behavior

The exercise MUST NOT:
- Use any concept that is not included in the described competencies or their prerequisites
- Introduce advanced concepts without their prerequisites being covered

## Validation Requirement

You MUST explicitly list:
- All competencies covered in the exercise
- All prerequisite competencies that are required and covered

## Exercise Type: {config['label']} ({exercise_type})

Targets:
- Classes: {config['targetClasses']}
- Student TODOs: {config['targetTodos']}
- Test methods: {config['targetTests']}
- Solution LOC range: {config['targetLOC']}

## Exercise Context

- **Title**: {safe_title}
- **Package**: {safe_package}

### Competency and Prerequisites Description

{description}

{f"### Additional Requirements\n{safe_additional}\n" if safe_additional else ""}

## Required JSON Schema

{{
  "exerciseTheme": "string — a brief thematic description",
  "classes": [
    {{
      "name": "string — class name",
      "type": "class | interface | enum | abstract class | record",
      "file": "string — relative file path",
      "package": "string — Java package",
      "methods": ["string — method signatures"],
      "implements": ["string — interface names (optional)"],
      "extends": "string — parent class (optional)",
      "providedToStudent": "boolean"
    }}
  ],
  "designPatterns": ["string"],
  "studentTodos": "number",
  "estimatedSolutionLOC": "number",
  "testClasses": [
    {{
      "name": "string",
      "file": "string",
      "testMethods": ["string"]
    }}
  ],
  "coveredCompetencies": ["string"],
  "coveredPrerequisites": ["string"]
}}

Output ONLY the JSON object. No markdown fences, no commentary.
"""


def build_template_prompt_kg(plan, competency_json):
    return f"""
Based on the following plan:

{json.dumps(plan, indent=2)}

And competencies:

{json.dumps(competency_json, indent=2)}

Generate:
- problem-statement.md
- Java template code

The generated files MUST strictly follow the plan and reflect all listed competencies and prerequisites.
Return files JSON.
"""


def build_template_prompt_nl(plan, description):
    return f"""
Based on the following plan:

{json.dumps(plan, indent=2)}

And description:

{description}

Generate:
- problem-statement.md
- Java template code

The generated files MUST strictly follow the plan and reflect all listed competencies and prerequisites.
Return files JSON.
"""


# =========================
# PIPELINE
# =========================
from datetime import datetime

def run_pipeline_kg(competency_json, metadata, config):
    run_id = "kg"
    timestamp = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{run_id}"

    plan_prompt = build_planning_prompt_kg(
        competency_json,
        metadata,
        config
    )
    plan = generate_plan(plan_prompt, timestamp)

    template_prompt = build_template_prompt_kg(plan, competency_json)
    result = generate_template(template_prompt, timestamp)

    return plan, result


def run_pipeline_nl(description, metadata, config):
    run_id = "nl"
    timestamp = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{run_id}"

    plan_prompt = build_planning_prompt_nl(description, metadata, config)
    plan = generate_plan(plan_prompt, timestamp)

    template_prompt = build_template_prompt_nl(plan, description)
    result = generate_template(template_prompt, timestamp)

    return plan, result


# =========================
# MAIN TEST
# =========================
if __name__ == "__main__":

    # ===== CONFIG =====
    config = {
        "label": "Standard Exercise",
        "targetClasses": "6-8",
        "targetTodos": "4-5",
        "targetTests": "8-20",
        "targetLOC": "50-120"
    }

    metadata = {
        "title": "File Processing System",
        "packageName": "de.tum.test",
        "exerciseType": "standard"
    }

    # ===== LOAD KG =====
    competency_json = load_competency_json("output.json")

    # ===== NL DESCRIPTION =====
    description = """
The exercise should focus on the following competencies:

Try-Catch Blocks
Apply try-catch-finally blocks to handle exceptions gracefully and maintain program stability. Use appropriate exception handling strategies including catching specific exceptions, resource cleanup, and meaningful error recovery or reporting.
    
Exceptions: 
Explain Java's exception mechanism including the distinction between checked and unchecked exceptions. Understand how exceptions represent error conditions, propagate through the call stack, and differ from normal return values.
"""

    # =========================
    # RUN KG PIPELINE
    # =========================
    print("\n===== RUNNING KG PIPELINE =====\n")

    kg_plan, kg_result = run_pipeline_kg(
        competency_json,
        metadata,
        config
    )

    print("\n===== KG PLAN =====\n")
    print(json.dumps(kg_plan, indent=2))

    print("\n===== KG TEMPLATE RESULT =====\n")
    print(json.dumps(kg_result, indent=2))

    # =========================
    # RUN NL PIPELINE
    # =========================
    print("\n===== RUNNING NL PIPELINE =====\n")

    nl_plan, nl_result = run_pipeline_nl(
        description,
        metadata,
        config
    )

    print("\n===== NL PLAN =====\n")
    print(json.dumps(nl_plan, indent=2))

    print("\n===== NL TEMPLATE RESULT =====\n")
    print(json.dumps(nl_result, indent=2))