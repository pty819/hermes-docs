import os
import sys

# sys.path adjusted for standalone docs repo

project = "Hermes Agent 架构深度解析"
copyright = "2026, NousResearch / Community"
author = "Hermes Architecture Book"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.graphviz",
    "sphinxcontrib.mermaid",
]

templates_path = ["_templates"]
exclude_patterns = []
source_suffix = ".rst"
master_doc = "index"

language = "zh_CN"

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_css_files = ["mermaid-book.css"]

mermaid_version = "10.6.1"
mermaid_d3_zoom = True
mermaid_fullscreen = True
mermaid_fullscreen_button = "⤢"
mermaid_fullscreen_button_opacity = "55"
mermaid_width = "100%"
mermaid_init_js = """
mermaid.initialize({
  startOnLoad: true,
  theme: "base",
  flowchart: {
    htmlLabels: true,
    useMaxWidth: false,
    curve: "basis",
    nodeSpacing: 42,
    rankSpacing: 60,
    padding: 18,
  },
  sequence: {
    useMaxWidth: false,
    wrap: true,
    actorMargin: 72,
    width: 160,
    messageMargin: 24,
    noteMargin: 18,
    diagramMarginX: 24,
    diagramMarginY: 20,
  },
  class: {
    useMaxWidth: false,
  },
  state: {
    useMaxWidth: false,
  },
  themeVariables: {
    fontFamily: 'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    fontSize: "14px",
    primaryColor: "#fff7ed",
    primaryTextColor: "#1f2937",
    primaryBorderColor: "#c2410c",
    lineColor: "#475569",
    secondaryColor: "#eff6ff",
    tertiaryColor: "#f8fafc",
    background: "#ffffff",
    mainBkg: "#ffffff",
    clusterBkg: "#f8fafc",
    clusterBorder: "#94a3b8",
    edgeLabelBackground: "#ffffff",
    noteBkgColor: "#fffbeb",
    noteBorderColor: "#f59e0b",
    actorBkg: "#eff6ff",
    actorBorder: "#3b82f6",
    actorTextColor: "#1e3a8a",
    actorLineColor: "#64748b",
    signalColor: "#475569",
    signalTextColor: "#334155",
    labelBoxBkgColor: "#ffffff",
    labelBoxBorderColor: "#cbd5e1",
    activationBkgColor: "#dbeafe",
    activationBorderColor: "#60a5fa",
    sequenceNumberColor: "#1e3a8a",
  },
});
"""

html_theme_options = {
    "navigation_depth": 4,
    "collapse_navigation": False,
    "sticky_navigation": True,
}
