# policy_engine/risk_scoring.rego
package vanguard.risk_scoring

default refined_score = "Low"

# If a High-severity finding occurs on an asset tagged CUI/FedRAMP,
# its Refined Risk Score becomes Critical.
refined_score = "Critical" {
    input.severity == "High"
    contains(input.tags, "CUI/FedRAMP")
}

# Medium-severity findings on Production assets are elevated to High.
refined_score = "High" {
    input.severity == "Medium"
    contains(input.tags, "Production")
}

# All other High-severity findings are just High.
refined_score = "High" {
    input.severity == "High"
}

# All other Medium-severity findings are just Medium.
refined_score = "Medium" {
    input.severity == "Medium"
}
