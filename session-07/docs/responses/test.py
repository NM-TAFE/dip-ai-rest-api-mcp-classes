{"meta": {
    # ---- Permissions & governance (advertised to the MCP host) ----
    "permissions": {
        "required_roles":  ["utility.read", "conversion.run"],
        "required_scopes": ["miles:convert"],
        "policy": "deny-by-default",
        "reason": "Conversion tools restricted to authorized users only."
    },
    # ---- Safety / side-effects (helps planning & review UIs) ----
    "side_effects": "none",   # read-only, deterministic mapping
    "deterministic": True,    # same input -> same output
    # ---- Rate limiting hints (host or gateway can enforce) ----
    "rate_limit": {
        "unit": "minute",
        "limit": 300,   # per principal (suggested)
        "burst": 50
    },
    # ---- Auditability (names/log keys the host can capture) ----
    "audit": {
        "log_fields": ["miles", "result", "operation"],
        "pii": "none"
    },
    # ---- Versioning for change control ----
    "version": "1.1.0"
}
}