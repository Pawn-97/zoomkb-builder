"""Generic product taxonomy used by all generated Zoom KBs."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class KBCategory:
    """A stable, product-agnostic category for design-facing navigation."""

    key: str
    title: str
    definition: str
    users: tuple[str, ...]
    tasks: tuple[str, ...]
    design_scenarios: tuple[str, ...]
    failure_states: tuple[str, ...]
    keywords: tuple[str, ...]


DEFAULT_TAXONOMY: tuple[KBCategory, ...] = (
    KBCategory(
        key="01-getting-started-deployment",
        title="01 Getting Started & Deployment",
        definition="Initial setup, rollout planning, activation, provisioning, migration, and validation work.",
        users=("IT admin", "implementation owner", "operations lead"),
        tasks=("Plan rollout", "Configure prerequisites", "Activate service", "Validate first successful use"),
        design_scenarios=("First-run setup", "Admin onboarding", "Setup recovery"),
        failure_states=("Missing prerequisite", "Activation blocked", "Configuration incomplete"),
        keywords=(
            "getting started", "setup", "set up", "deployment", "deploy", "activation",
            "activate", "install", "provision", "configure", "configuration", "onboard",
            "migration", "test", "quick start",
        ),
    ),
    KBCategory(
        key="02-core-concepts-product-model",
        title="02 Core Concepts & Product Model",
        definition="Core objects, feature models, domain concepts, and product mental models.",
        users=("UX designer", "PM", "support specialist"),
        tasks=("Understand feature boundaries", "Map product objects", "Compare related concepts"),
        design_scenarios=("Information architecture", "Feature education", "Terminology alignment"),
        failure_states=("Ambiguous object model", "Overloaded feature name", "Missing conceptual dependency"),
        keywords=(
            "overview", "about", "introduction", "feature", "concept", "model", "settings",
            "manage", "management", "workspace", "queue", "number", "room", "clip", "meeting",
        ),
    ),
    KBCategory(
        key="03-user-tasks-workflows",
        title="03 User Tasks & Workflows",
        definition="End-to-end tasks users or admins complete across product surfaces.",
        users=("end user", "admin", "support specialist", "operations lead"),
        tasks=("Complete a task", "Recover from blocked steps", "Compare alternate paths"),
        design_scenarios=("Task flow design", "Guided setup", "Error recovery"),
        failure_states=("Step unavailable", "Wrong actor", "State transition unclear"),
        keywords=(
            "how to", "use ", "using", "create", "add", "edit", "delete", "change",
            "assign", "remove", "enable", "disable", "reserve", "join", "share", "send",
            "receive", "check in", "check-out", "check out",
        ),
    ),
    KBCategory(
        key="04-devices-clients-surfaces",
        title="04 Devices, Clients & Surfaces",
        definition="Hardware, apps, controllers, clients, displays, and other user-facing surfaces.",
        users=("device admin", "IT admin", "end user", "facilities owner"),
        tasks=("Select supported surface", "Pair or manage device", "Diagnose surface-specific behavior"),
        design_scenarios=("Responsive surface behavior", "Device state visibility", "Physical-to-digital handoff"),
        failure_states=("Unsupported device", "Pairing failure", "Client version mismatch"),
        keywords=(
            "device", "hardware", "client", "desktop", "mobile", "app", "appliance",
            "controller", "display", "phone", "camera", "audio", "video", "speaker",
            "headset", "kiosk", "room", "rooms", "zdm",
        ),
    ),
    KBCategory(
        key="05-scheduling-meetings-collaboration",
        title="05 Scheduling, Meetings & Collaboration",
        definition="Calendar, meetings, joining, sharing, collaboration, and real-time interaction experiences.",
        users=("meeting participant", "host", "scheduler", "workspace user"),
        tasks=("Schedule", "Join", "Share", "Collaborate", "Manage live controls"),
        design_scenarios=("Entry point clarity", "Meeting state design", "Collaboration affordances"),
        failure_states=("Meeting missing", "Join blocked", "Sharing unavailable"),
        keywords=(
            "meeting", "calendar", "schedule", "scheduling", "join", "one-tap", "one tap",
            "invite", "host", "participant", "share", "sharing", "whiteboard", "caption",
            "recording", "waiting room", "webinar", "collaboration",
        ),
    ),
    KBCategory(
        key="06-admin-roles-policy",
        title="06 Admin, Roles & Policy",
        definition="Account settings, role permissions, policy controls, hierarchy, and visibility rules.",
        users=("account admin", "role admin", "compliance owner", "support specialist"),
        tasks=("Control access", "Set policy", "Understand visibility", "Delegate management"),
        design_scenarios=("Permission-gated UI", "Admin hierarchy", "Policy inheritance"),
        failure_states=("Permission denied", "Setting hidden", "Policy conflict"),
        keywords=(
            "admin", "administrator", "role", "permission", "policy", "account", "group",
            "site", "location", "hierarchy", "visibility", "privacy", "security", "lock",
            "passcode", "authentication", "sso",
        ),
    ),
    KBCategory(
        key="07-integrations-interop",
        title="07 Integrations & Interop",
        definition="External systems, APIs, calendar providers, telephony, identity, and cross-product integrations.",
        users=("integration admin", "IT admin", "developer", "partner admin"),
        tasks=("Connect external system", "Map integration dependencies", "Diagnose interoperability gaps"),
        design_scenarios=("Cross-product handoff", "Third-party affordances", "Integration status visibility"),
        failure_states=("Authorization failed", "Sync broken", "Third-party capability mismatch"),
        keywords=(
            "integration", "integrate", "api", "webhook", "microsoft", "teams", "google",
            "office 365", "exchange", "salesforce", "slack", "sip", "h.323", "interop",
            "crc", "lti", "pbx", "contact center", "zoom phone",
        ),
    ),
    KBCategory(
        key="08-requirements-licenses-platform-support",
        title="08 Requirements, Licenses & Platform Support",
        definition="Prerequisites, plan availability, licenses, OS/app support, limits, and end-of-support notices.",
        users=("PM", "UX designer", "IT admin", "support specialist"),
        tasks=("Verify eligibility", "Explain unavailable states", "Plan upgrade or migration"),
        design_scenarios=("Unavailable feature states", "Upgrade prompts", "Compatibility messaging"),
        failure_states=("License missing", "Version unsupported", "Limit exceeded", "End of support"),
        keywords=(
            "requirement", "requirements", "prerequisite", "license", "licence", "plan",
            "subscription", "support", "supported", "unsupported", "os", "version",
            "limit", "limitation", "availability", "end of support", "eos", "beta",
        ),
    ),
    KBCategory(
        key="09-monitoring-logs-troubleshooting",
        title="09 Monitoring, Logs & Troubleshooting",
        definition="Operational monitoring, logs, diagnostics, alerts, known issues, and root-cause workflows.",
        users=("support specialist", "IT admin", "operations lead", "incident owner"),
        tasks=("Diagnose symptom", "Collect evidence", "Resolve failure", "Escalate with context"),
        design_scenarios=("Status visibility", "Recovery path design", "Support handoff"),
        failure_states=("Cannot connect", "Sync failure", "Alert unresolved", "Logs missing"),
        keywords=(
            "troubleshoot", "troubleshooting", "problem", "issue", "error", "cannot",
            "can't", "unable", "fail", "failure", "logs", "log", "diagnostic", "alert",
            "dashboard", "monitor", "offline", "connectivity", "root cause",
        ),
    ),
    KBCategory(
        key="10-automation-ai-advanced-capabilities",
        title="10 Automation, AI & Advanced Capabilities",
        definition="AI-assisted features, automation, recommendations, bots, workflow rules, and advanced controls.",
        users=("power user", "admin", "automation owner", "UX designer"),
        tasks=("Configure automation", "Understand AI behavior", "Review generated recommendations"),
        design_scenarios=("AI transparency", "Automation setup", "Human override"),
        failure_states=("Recommendation unavailable", "Automation rule conflict", "AI output not trusted"),
        keywords=(
            "ai", "artificial intelligence", "automation", "automated", "workflow",
            "bot", "assistant", "recommendation", "smart", "agent", "auto", "scheduler",
        ),
    ),
)


def normalize_category_title(value: str) -> str:
    """Return a known category title for fuzzy user/model category labels."""
    value = (value or "").strip()
    if not value:
        return ""

    lower = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    for category in DEFAULT_TAXONOMY:
        title_lower = re.sub(r"[^a-z0-9]+", " ", category.title.lower()).strip()
        key_lower = re.sub(r"[^a-z0-9]+", " ", category.key.lower()).strip()
        if lower in {title_lower, key_lower} or lower in title_lower or lower in key_lower:
            return category.title

    return ""


def get_category(title: str) -> KBCategory:
    normalized = normalize_category_title(title)
    for category in DEFAULT_TAXONOMY:
        if category.title == normalized:
            return category
    return DEFAULT_TAXONOMY[1]


def categorize_text(*parts: str) -> str:
    """Classify arbitrary article/entity text into the default taxonomy."""
    text = " ".join(p for p in parts if p).lower()
    if not text.strip():
        return DEFAULT_TAXONOMY[1].title

    scores: list[tuple[int, KBCategory]] = []
    for category in DEFAULT_TAXONOMY:
        score = 0
        for keyword in category.keywords:
            if keyword in text:
                score += 3 if " " in keyword else 1
        scores.append((score, category))

    scores.sort(key=lambda item: item[0], reverse=True)
    if scores[0][0] == 0:
        return DEFAULT_TAXONOMY[1].title
    return scores[0][1].title


def category_filename(title: str) -> str:
    """Convert a category title into a stable markdown filename."""
    category = get_category(title)
    name = re.sub(r"^\d+\s+", "", category.title)
    name = name.replace("&", "and")
    name = re.sub(r"[^A-Za-z0-9]+", " ", name).strip()
    return f"{name}.md"


def taxonomy_prompt(product: str) -> str:
    """Render taxonomy guidance for extraction prompts."""
    lines = [
        f"Use this product taxonomy for {product}. Pick one primary_category for every entity:",
        "",
    ]
    for category in DEFAULT_TAXONOMY:
        lines.append(f"- {category.title}: {category.definition}")
    return "\n".join(lines)
