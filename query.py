from rdflib import Graph, Namespace
import json

# Namespaces
EX = Namespace("https://aet.cit.tum.de/tpo/example#")
TPO = Namespace("https://aet.cit.tum.de/tpo#")

# Load graph
g = Graph()
g.parse("infered-kg.ttl", format="ttl")

# Target competencies
competencies = [
    EX.Comp_NullReferences,
    EX.Comp_References,
    EX.Comp_ObjectEquality
]

values_str = "\n".join(f"<{c}>" for c in competencies)

# SPARQL query (2-hop with taxonomy)
query = f"""
PREFIX tpo: <https://aet.cit.tum.de/tpo#>
PREFIX dct: <http://purl.org/dc/terms/>

SELECT ?comp ?title ?description ?taxonomy 
       ?dep1 ?dep1Label ?dep1Desc ?rel1 ?dep1Taxonomy
       ?dep2 ?dep2Label ?dep2Desc ?rel2 ?dep2Taxonomy
WHERE {{
    VALUES ?comp {{ {values_str} }}

    OPTIONAL {{ ?comp dct:title ?title }}
    OPTIONAL {{ ?comp dct:description ?description }}
    OPTIONAL {{ ?comp tpo:hasCompetencyTaxonomy ?taxonomy }}

    OPTIONAL {{
        ?comp tpo:hasCompetencyDependency ?dep1 .

        OPTIONAL {{ ?dep1 dct:title ?dep1Label }}
        OPTIONAL {{ ?dep1 dct:description ?dep1Desc }}
        OPTIONAL {{ ?dep1 tpo:hasCompetencyTaxonomy ?dep1Taxonomy }}

        OPTIONAL {{ ?comp ?rel1 ?dep1 }}

        OPTIONAL {{
            ?dep1 tpo:hasCompetencyDependency ?dep2 .

            OPTIONAL {{ ?dep2 dct:title ?dep2Label }}
            OPTIONAL {{ ?dep2 dct:description ?dep2Desc }}
            OPTIONAL {{ ?dep2 tpo:hasCompetencyTaxonomy ?dep2Taxonomy }}

            OPTIONAL {{ ?dep1 ?rel2 ?dep2 }}
        }}
    }}
}}
"""

results = g.query(query)


def get_local_name(uri):
    if uri is None:
        return None
    return str(uri).split("#")[-1]


# Parse
output = {}

for row in results:
    (comp, title, desc, taxonomy,
     dep1, dep1Label, dep1Desc, rel1, dep1Taxonomy,
     dep2, dep2Label, dep2Desc, rel2, dep2Taxonomy) = row

    comp_uri = str(comp)

    if comp_uri not in output:
        output[comp_uri] = {
            "title": None,
            "description": None,
            "taxonomy": set(),
            "dependencies": {}
        }

    entry = output[comp_uri]

    if title:
        entry["title"] = str(title)
    if desc:
        entry["description"] = str(desc)

    if taxonomy:
        entry["taxonomy"].add(get_local_name(taxonomy))

    # -------- dep1 --------
    if dep1:
        rel1_name = get_local_name(rel1) if rel1 else None

        # skip structural edge
        if rel1_name == "hasCompetencyDependency":
            continue

        dep1_uri = str(dep1)

        if dep1_uri not in entry["dependencies"]:
            entry["dependencies"][dep1_uri] = {
                "label": str(dep1Label) if dep1Label else None,
                "description": str(dep1Desc) if dep1Desc else None,
                "taxonomy": set(),
                "relations": set(),
                "sub_dependencies": {}
            }

        if rel1_name:
            entry["dependencies"][dep1_uri]["relations"].add(rel1_name)

        if dep1Taxonomy:
            entry["dependencies"][dep1_uri]["taxonomy"].add(get_local_name(dep1Taxonomy))

        # -------- dep2 --------
        if dep2:
            rel2_name = get_local_name(rel2) if rel2 else None

            if rel2_name == "hasCompetencyDependency":
                continue

            dep2_uri = str(dep2)
            sub = entry["dependencies"][dep1_uri]["sub_dependencies"]

            if dep2_uri not in sub:
                sub[dep2_uri] = {
                    "label": str(dep2Label) if dep2Label else None,
                    "description": str(dep2Desc) if dep2Desc else None,
                    "taxonomy": set(),
                    "relations": set()
                }

            if rel2_name:
                sub[dep2_uri]["relations"].add(rel2_name)

            if dep2Taxonomy:
                sub[dep2_uri]["taxonomy"].add(get_local_name(dep2Taxonomy))


# finalize
for comp_uri, entry in output.items():
    entry["taxonomy"] = list(entry["taxonomy"])

    for dep1_uri, dep1_val in entry["dependencies"].items():
        dep1_val["taxonomy"] = list(dep1_val["taxonomy"])
        dep1_val["relations"] = list(dep1_val["relations"])

        dep1_val["sub_dependencies"] = [
            {
                "label": v["label"],
                "description": v["description"],
                "taxonomy": list(v["taxonomy"]),
                "relations": list(v["relations"])
            }
            for v in dep1_val["sub_dependencies"].values()
        ]

    entry["dependencies"] = [
        {
            "label": v["label"],
            "description": v["description"],
            "taxonomy": v["taxonomy"],
            "relations": v["relations"],
            "sub_dependencies": v["sub_dependencies"]
        }
        for v in entry["dependencies"].values()
    ]

# save to json
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("Saved to output.json")
