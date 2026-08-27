"""Artifact Boundary Contract — single machine-readable source of truth.

report.html is the interface between the Generation plane (produces it) and
the Delivery plane (consumes it). This module is the ONLY place where that
interface's namespace vocabulary is defined; the injector, the validators
and the contract document (postprocess/references/editor-contract.md
§Artifact Boundary) all consume it from here.

MUST   — traceability syntax the Generation side is required to write on
         semantic carriers (references/24 §13, mandated).
FREE   — the Huashu design plane zone. The editor must never read, rewrite,
         or strip anything in this zone.
FORBIDDEN — the Delivery plane's private namespace. The base report must
         contain zero of these; they may only appear via PostProcess
         injection, and are stripped again by the clean export.
"""

DU_ATTRIBUTE = 'data-du-id'

MUST_ATTRIBUTES = (
    'data-du-id',
    'data-obligation-refs',
    'data-source-table-id',
)

FREE_ZONE_NOTE = (
    'class / style / id / aria-* and any custom visual-semantics attributes '
    'belong to the Huashu design plane; PostProcess never touches them'
)

FORBIDDEN_ATTR_PREFIXES = ('data-edit-', 'data-he-', 'data-human-edit-')
FORBIDDEN_ATTRS = ('data-motion-reveal',)
FORBIDDEN_IDS = (
    'he-editor-style', 'he-editor-script', 'human-edit-ledger',
    'human-edit-base-state', 'human-edit-meta',
)
FORBIDDEN_CLASS_PREFIX = 'he-'

# Attributes the injector adds (and the validators strip). By definition this
# equals everything the base report must NOT contain.
INJECTED_ATTRS = (
    'data-edit-id', 'data-edit-type', 'data-edit-authority',
    'data-edit-obligation-refs', 'data-edit-module-id', 'data-edit-movable',
    'data-motion-reveal', 'data-he-runtime-ui', 'data-human-edit-layer',
)


def attr_is_forbidden(name: str) -> bool:
    name = name.lower()
    return name in FORBIDDEN_ATTRS or name.startswith(FORBIDDEN_ATTR_PREFIXES)


def element_violations(el) -> list:
    """All boundary violations found on one DOM element (injector-shaped)."""
    hits = []
    eid = el.attrs.get('id')
    if eid in FORBIDDEN_IDS:
        hits.append(f'id={eid}')
    for name in el.attrs:
        if attr_is_forbidden(name):
            hits.append(f'<{el.tag}> {name}')
    for cls in (el.attrs.get('class') or '').split():
        if cls.startswith(FORBIDDEN_CLASS_PREFIX):
            hits.append(f'<{el.tag}> .{cls}')
    return hits
