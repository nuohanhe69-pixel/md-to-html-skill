#!/usr/bin/env python3
"""Minimal stdlib DOM for the deterministic postprocess subsystem.

html.parser-based tree builder + serializer + structural comparator + a
selector subset. Zero third-party dependencies so delivery stays
reproducible on any python3 (no BeautifulSoup).

Known limitation: implicit-close handling covers common sibling cases
(p/li/td/th/tr/dt/dd/option and table sections). Base reports are expected
to be well-formed HTML; pathological unclosed markup still round-trips
stably but may nest differently than a browser would interpret it.
"""
from __future__ import annotations
import re
from html.parser import HTMLParser

VOID_ELEMENTS = {
    'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr',
}
RAW_TEXT_ELEMENTS = {'script', 'style'}

IMPLICIT_CLOSE = {
    'p': {'p'},
    'li': {'li'},
    'dt': {'dt', 'dd'},
    'dd': {'dt', 'dd'},
    'option': {'option'},
    'tr': {'td', 'th', 'tr'},
    'td': {'td', 'th'},
    'th': {'td', 'th'},
    'thead': {'td', 'th', 'tr', 'caption'},
    'tbody': {'td', 'th', 'tr', 'thead', 'caption'},
    'tfoot': {'td', 'th', 'tr', 'tbody', 'thead', 'caption'},
}


class Node:
    __slots__ = ('kind', 'tag', 'attrs', 'children', 'parent', 'data')

    def __init__(self, kind, tag=None, attrs=None, data=''):
        self.kind = kind  # 'element' | 'text' | 'comment' | 'decl'
        self.tag = tag
        self.attrs = attrs if attrs is not None else {}
        self.children = []
        self.parent = None
        self.data = data


def make_element(tag, attrs=None, text=None):
    node = Node('element', tag, dict(attrs or {}))
    if text is not None:
        t = Node('text', data=text)
        t.parent = node
        node.children.append(t)
    return node


class _Builder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node('element', '#root')
        self.stack = [self.root]
        self.doctype = None

    def _append_element(self, tag, attrs, self_closing):
        closes = IMPLICIT_CLOSE.get(tag)
        if closes:
            while len(self.stack) > 1 and self.stack[-1].tag in closes:
                self.stack.pop()
        node = Node('element', tag)
        for k, v in attrs:
            if k not in node.attrs:
                node.attrs[k] = v  # None means bare attribute
        parent = self.stack[-1]
        node.parent = parent
        parent.children.append(node)
        if not self_closing and tag not in VOID_ELEMENTS:
            self.stack.append(node)

    def handle_starttag(self, tag, attrs):
        self._append_element(tag, attrs, self_closing=False)

    def handle_startendtag(self, tag, attrs):
        self._append_element(tag, attrs, self_closing=True)

    def handle_endtag(self, tag):
        if tag in VOID_ELEMENTS:
            return
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        if data == '':
            return
        parent = self.stack[-1]
        last = parent.children[-1] if parent.children else None
        if last is not None and last.kind == 'text':
            last.data += data
        else:
            t = Node('text', data=data)
            t.parent = parent
            parent.children.append(t)

    def handle_comment(self, data):
        c = Node('comment', data=data)
        c.parent = self.stack[-1]
        self.stack[-1].children.append(c)

    def handle_decl(self, decl):
        if self.doctype is None and decl.lower().startswith('doctype'):
            self.doctype = decl

    def unknown_decl(self, data):
        d = Node('decl', data=data)
        d.parent = self.stack[-1]
        self.stack[-1].children.append(d)


def parse_html(text: str):
    builder = _Builder()
    builder.feed(text)
    builder.close()
    return builder.root, builder.doctype


def _escape_text(s: str) -> str:
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _escape_attr(s: str) -> str:
    return s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')


def serialize_node(node: Node) -> str:
    if node.kind == 'text':
        if node.parent is not None and node.parent.tag in RAW_TEXT_ELEMENTS:
            return node.data
        return _escape_text(node.data)
    if node.kind == 'comment':
        return f'<!--{node.data}-->'
    if node.kind == 'decl':
        return f'<![{node.data}]>'
    parts = ['<' + node.tag]
    for k, v in node.attrs.items():
        if v is None:
            parts.append(f' {k}')
        else:
            parts.append(f' {k}="{_escape_attr(v)}"')
    inner = ''.join(serialize_node(c) for c in node.children)
    if node.tag in VOID_ELEMENTS:
        return ''.join(parts) + '>' + inner
    return ''.join(parts) + '>' + inner + f'</{node.tag}>'


def serialize_html(root: Node, doctype: str | None = None) -> str:
    out = []
    if doctype:
        out.append(f'<!{doctype}>')
    out.append(''.join(serialize_node(c) for c in root.children))
    return ''.join(out)


def tree_equal(a: Node, b: Node) -> bool:
    if a.kind != b.kind:
        return False
    if a.kind in ('text', 'comment', 'decl'):
        return a.data == b.data
    if a.tag != b.tag or a.attrs != b.attrs:
        return False
    if len(a.children) != len(b.children):
        return False
    return all(tree_equal(x, y) for x, y in zip(a.children, b.children))


def iter_elements(node: Node, include_self: bool = False):
    if include_self and node.kind == 'element':
        yield node
    stack = list(reversed(node.children))
    while stack:
        cur = stack.pop()
        if cur.kind == 'element':
            yield cur
            stack.extend(reversed(cur.children))


def first_tag(root: Node, tag: str):
    for e in iter_elements(root):
        if e.tag == tag:
            return e
    return None


def find_by_id(root: Node, id_value: str):
    for e in iter_elements(root):
        if e.attrs.get('id') == id_value:
            return e
    return None


def get_text(node: Node) -> str:
    out = []

    def walk(n):
        for c in n.children:
            if c.kind == 'text':
                out.append(c.data)
            else:
                walk(c)

    walk(node)
    return ''.join(out)


def classes(node: Node) -> set:
    return set((node.attrs.get('class') or '').split())


def has_class(node: Node, cls: str) -> bool:
    return cls in classes(node)


_SELECTOR_TOKEN = re.compile(
    r"(?P<tag>[A-Za-z][\w-]*|\*)"
    r"|\#(?P<id>[\w-]+)"
    r"|\.(?P<cls>[\w-]+)"
    r"|\[\s*(?P<attr>[\w-]+)\s*(?:=\s*(?P<val>\"[^\"]*\"|'[^']*'|[\w-]+))?\s*\]"
)


def parse_selector(selector: str):
    tag = '*'
    conds = []
    pos = 0
    while pos < len(selector):
        if selector[pos].isspace():
            pos += 1
            continue
        m = _SELECTOR_TOKEN.match(selector, pos)
        if not m:
            raise ValueError(f'unsupported selector: {selector}')
        if m.group('tag'):
            tag = m.group('tag').lower()
        elif m.group('id'):
            conds.append(('id', m.group('id')))
        elif m.group('cls'):
            conds.append(('class', m.group('cls')))
        else:
            name = m.group('attr').lower()
            val = m.group('val')
            if val is None:
                conds.append(('attr', name))
            else:
                if val[0] in ('"', "'"):
                    val = val[1:-1]
                conds.append(('attr_eq', name, val))
        pos = m.end()
    return tag, conds


def select(root: Node, selector: str) -> list:
    tag, conds = parse_selector(selector)
    out = []
    for e in iter_elements(root):
        if tag != '*' and e.tag != tag:
            continue
        ok = True
        for c in conds:
            if c[0] == 'id' and e.attrs.get('id') != c[1]:
                ok = False
                break
            if c[0] == 'class' and c[1] not in classes(e):
                ok = False
                break
            if c[0] == 'attr' and c[1] not in e.attrs:
                ok = False
                break
            if c[0] == 'attr_eq' and e.attrs.get(c[1]) != c[2]:
                ok = False
                break
        if ok:
            out.append(e)
    return out
