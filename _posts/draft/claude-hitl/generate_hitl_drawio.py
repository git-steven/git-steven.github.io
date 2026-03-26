#!/usr/bin/env python3
"""Generate HITL infographic as draw.io XML per the spec."""

import math
import xml.etree.ElementTree as ET

# ── Canvas ──
W, H = 1920, 1200

# ── Ellipse centers & radii ──
CX, CY = 690, 600  # ~36% x, 50% y
OUTER_RX, OUTER_RY = 570, 480
INNER_RX, INNER_RY = 285, 240
# Governance sits between inner and outer
GOV_RX, GOV_RY = 420, 355

# ── Angle → (x, y) center of box  (0°=top, clockwise) ──
def ellipse_pos(angle_deg, rx, ry, cx=CX, cy=CY):
    rad = math.radians(angle_deg)
    x = cx + rx * math.sin(rad)
    y = cy - ry * math.cos(rad)
    return round(x), round(y)

# ── Color palette  (fill_start, fill_end, stroke) ──
COLORS = {
    "green":   ("#D5E8D4", "#00994D", "#00773B"),
    "red":     ("#FFCCCC", "#C14D4D", "#993B3B"),
    "blue":    ("#CCE5FF", "#5593D5", "#3D6FA8"),
    "yellow":  ("#FFFFDD", "#DFD2B2", "#B0A47D"),
    "purple":  ("#E5CCFF", "#A25DE9", "#7B3DB8"),
    "orange":  ("#FFCC88", "#BB7C4B", "#8D5A32"),
    "neutral": ("#EEEEEE", "#888888", "#666666"),
}

# ── Style helpers ──
SKETCH = "sketch=1;curveFitting=1;jiggle=2;sketchStyle=comic;"

def box_style(color_name, extra=""):
    c = COLORS[color_name]
    return (
        f"rounded=1;whiteSpace=wrap;html=1;shadow=1;{SKETCH}"
        f"fillColor={c[0]};gradientColor={c[1]};strokeColor={c[2]};strokeWidth=2;"
        f"fontFamily=Architects Daughter;fontSize=18;fontColor=#333333;"
        f"align=center;verticalAlign=middle;arcSize=16;{extra}"
    )

def callout_style(color_name):
    c = COLORS[color_name]
    return (
        f"rounded=1;whiteSpace=wrap;html=1;shadow=1;{SKETCH}"
        f"fillColor={c[0]};gradientColor={c[1]};strokeColor={c[2]};strokeWidth=2;"
        f"fontFamily=Tahoma;fontSize=13;fontColor=#333333;"
        f"align=left;verticalAlign=top;arcSize=12;spacing=8;"
    )

def arrow_style(dashed=False, color="#555555", width=4):
    dash = "dashed=1;dashPattern=8 6;" if dashed else ""
    return (
        f"rounded=1;orthogonalLoop=1;jettySize=auto;"
        f"curved=1;strokeColor={color};strokeWidth={width};{SKETCH}{dash}"
        f"endArrow=blockThin;endFill=1;shadow=0;"
    )

def ellipse_ring_style(color, sw=3, dash=False):
    d = "dashed=1;dashPattern=12 8;" if dash else ""
    return (
        f"shape=ellipse;whiteSpace=wrap;html=1;"
        f"fillColor=none;strokeColor={color};strokeWidth={sw};{d}"
        f"{SKETCH}opacity=50;"
    )

# ── Nodes ──
# (id, angle, rx, ry, color, line1, line2, box_w, box_h)
outer_nodes = [
    ("inference",   70,  OUTER_RX, OUTER_RY, "green",  "Inference Service",         "ranking · prediction · scoring",          220, 70),
    ("product_ui", 110,  OUTER_RX, OUTER_RY, "red",    "Product UI",                "surfaces predictions · evaluates session", 220, 70),
    ("expert_user",160,  OUTER_RX, OUTER_RY, "red",    "Expert User",               "session evaluated · rates · tags · corrects", 230, 70),
    ("data_store", 210,  OUTER_RX, OUTER_RY, "blue",   "Data / Outcome Store",      "PostgreSQL · Neo4j · Model Repo",         230, 70),
    ("pipeline",   260,  OUTER_RX, OUTER_RY, "yellow", "Data Pipeline",             "clean · normalize · enrich · transform",  220, 70),
    ("training",   310,  OUTER_RX, OUTER_RY, "yellow", "Training / Tuning + RL",    "batch retraining · RL · evaluation",      230, 70),
]

inner_nodes = [
    ("model_ensemble", 300, INNER_RX, INNER_RY, "purple", "Model Ensemble",           "specialized models · weighted outputs",  200, 65),
    ("deployment",       0, INNER_RX, INNER_RY, "blue",   "Deployment / Promotion",   "publish approved model set",             200, 65),
    ("inference_link",  40, INNER_RX, INNER_RY, "green",  "Runtime Link",             "connects deployed models to inference",  200, 65),
]

gov_nodes = [
    ("curation",   335, GOV_RX, GOV_RY, "orange", "Curation Team",          "reviews session data · selects signal",  200, 65),
    ("governance",  25, GOV_RX, GOV_RY, "orange", "Model Governance Team",  "validates · approves release",           210, 65),
]

# ── Edges  (source_id, target_id, dashed, color) ──
outer_edges = [
    ("inference",   "product_ui",  False, "#555555"),
    ("product_ui",  "expert_user", False, "#555555"),
    ("expert_user", "data_store",  False, "#555555"),
    ("data_store",  "pipeline",    False, "#555555"),
    ("pipeline",    "training",    False, "#555555"),
    ("training",    "model_ensemble", False, "#555555"),  # feeds inner
]

inner_edges = [
    ("model_ensemble", "deployment",     False, "#555555"),
    ("deployment",     "inference_link",  False, "#555555"),
    ("inference_link", "inference",       False, "#555555"),  # back to outer
]

gov_edges = [
    ("data_store", "curation",   True, "#BB7C4B"),
    ("curation",   "pipeline",   True, "#BB7C4B"),
    ("model_ensemble", "governance", True, "#BB7C4B"),
    ("governance", "deployment", True, "#BB7C4B"),
]

# ── Right-side callout panel ──
callouts = [
    ("operational_loop",    "Operational Loop",         "red",     "Real-time interaction where predictions are consumed and evaluated by expert users"),
    ("model_loop",          "Model Evolution Loop",     "yellow",  "Slower learning cycle involving curated data, training, and controlled model updates"),
    ("governance_boundary", "Governance Boundaries",    "orange",  "Human review layers that filter training signal and gate model promotion"),
    ("semi_supervised",     "Semi-Supervised Learning", "purple",  "Automated predictions combined with human feedback and curated learning"),
    ("non_autonomous",      "Not Fully Autonomous",     "neutral", "Human mediation introduces delay, filtering, and control boundaries"),
]

# ── Build XML ──
def build_drawio():
    # Collect node positions for edge routing
    positions = {}

    cells = []
    cell_id = 100

    def nid():
        nonlocal cell_id
        cell_id += 1
        return str(cell_id)

    # ── Background ──
    bg_id = nid()
    cells.append(f'''<mxCell id="{bg_id}" value="" style="rounded=0;whiteSpace=wrap;html=1;fillColor=#FCF5E5;gradientColor=#EDE6D6;gradientDirection=radial;strokeColor=#B0A890;strokeWidth=1;opacity=30;{SKETCH}" vertex="1" parent="1"><mxGeometry width="{W}" height="{H}" as="geometry"/></mxCell>''')

    # ── Title ──
    title_id = nid()
    cells.append(f'''<mxCell id="{title_id}" value="&lt;font style=&quot;font-size:36px;&quot;&gt;&lt;b&gt;Autonomous and Non-Autonomous AI Systems&lt;/b&gt;&lt;/font&gt;&lt;br&gt;&lt;font style=&quot;font-size:22px;&quot;&gt;Part 1: Human-in-the-Loop (HITL)&lt;/font&gt;" style="text;html=1;align=center;verticalAlign=middle;whiteSpace=wrap;rounded=1;{SKETCH}shadow=1;fillColor=#f5f5f5;gradientColor=#AFA99A;strokeColor=#666666;opacity=12;arcSize=30;fontFamily=Architects Daughter;fontSize=36;fontColor=#504D47;" vertex="1" parent="1"><mxGeometry x="200" y="15" width="900" height="90" as="geometry"/></mxCell>''')

    # ── Ellipse rings (visual guides) ──
    outer_ring_id = nid()
    cells.append(f'''<mxCell id="{outer_ring_id}" value="" style="{ellipse_ring_style('#888888', 2, False)}" vertex="1" parent="1"><mxGeometry x="{CX - OUTER_RX}" y="{CY - OUTER_RY}" width="{OUTER_RX*2}" height="{OUTER_RY*2}" as="geometry"/></mxCell>''')

    inner_ring_id = nid()
    cells.append(f'''<mxCell id="{inner_ring_id}" value="" style="{ellipse_ring_style('#999999', 2, True)}" vertex="1" parent="1"><mxGeometry x="{CX - INNER_RX}" y="{CY - INNER_RY}" width="{INNER_RX*2}" height="{INNER_RY*2}" as="geometry"/></mxCell>''')

    # ── Ellipse labels ──
    outer_label_id = nid()
    cells.append(f'''<mxCell id="{outer_label_id}" value="&lt;b&gt;Operational Loop&lt;/b&gt;" style="text;html=1;align=left;verticalAlign=middle;fontFamily=Architects Daughter;fontSize=16;fontColor=#88555588;fontStyle=2;strokeColor=none;fillColor=none;" vertex="1" parent="1"><mxGeometry x="{CX - OUTER_RX + 15}" y="{CY - OUTER_RY + 5}" width="200" height="30" as="geometry"/></mxCell>''')

    inner_label_id = nid()
    cells.append(f'''<mxCell id="{inner_label_id}" value="&lt;i&gt;Model Evolution&lt;/i&gt;" style="text;html=1;align=left;verticalAlign=middle;fontFamily=Architects Daughter;fontSize=14;fontColor=#99999988;fontStyle=2;strokeColor=none;fillColor=none;" vertex="1" parent="1"><mxGeometry x="{CX - INNER_RX + 10}" y="{CY - INNER_RY + 5}" width="170" height="25" as="geometry"/></mxCell>''')

    # ── Place nodes ──
    node_ids = {}

    def place_nodes(node_list):
        for (nkey, angle, rx, ry, color, line1, line2, bw, bh) in node_list:
            cx, cy = ellipse_pos(angle, rx, ry)
            x = cx - bw // 2
            y = cy - bh // 2
            positions[nkey] = (cx, cy, bw, bh)
            mid = nid()
            node_ids[nkey] = mid
            label = f"&lt;b&gt;{line1}&lt;/b&gt;&lt;br&gt;&lt;font style=&quot;font-size:12px;font-family:Tahoma;&quot;&gt;{line2}&lt;/font&gt;"
            cells.append(f'''<mxCell id="{mid}" value="{label}" style="{box_style(color)}" vertex="1" parent="1"><mxGeometry x="{x}" y="{y}" width="{bw}" height="{bh}" as="geometry"/></mxCell>''')

    place_nodes(outer_nodes)
    place_nodes(inner_nodes)
    place_nodes(gov_nodes)

    # ── Edges ──
    def place_edges(edge_list):
        for (src, tgt, dashed, color) in edge_list:
            eid = nid()
            w = 5 if dashed else 4
            style = arrow_style(dashed, color, w)
            cells.append(f'''<mxCell id="{eid}" value="" style="{style}" edge="1" source="{node_ids[src]}" target="{node_ids[tgt]}" parent="1"><mxGeometry relative="1" as="geometry"/></mxCell>''')

    place_edges(outer_edges)
    place_edges(inner_edges)
    place_edges(gov_edges)

    # ── Right-side callout panel ──
    panel_x = 1340
    panel_y = 150
    panel_w = 540
    box_h = 100
    gap = 18

    for i, (ckey, caption, color, text) in enumerate(callouts):
        by = panel_y + i * (box_h + gap)
        cid = nid()
        label = f"&lt;b style=&quot;font-size:15px;font-family:Architects Daughter;&quot;&gt;{caption}&lt;/b&gt;&lt;br&gt;&lt;br&gt;&lt;font style=&quot;font-size:13px;&quot;&gt;{text}&lt;/font&gt;"
        cells.append(f'''<mxCell id="{cid}" value="{label}" style="{callout_style(color)}" vertex="1" parent="1"><mxGeometry x="{panel_x}" y="{by}" width="{panel_w}" height="{box_h}" as="geometry"/></mxCell>''')

    # ── Legend (top-right) ──
    leg_x = 1340
    leg_y = 15
    leg_w = 540
    leg_h = 120
    leg_id = nid()
    legend_text = (
        "&lt;b style=&quot;font-size:16px;font-family:Architects Daughter;&quot;&gt;Legend&lt;/b&gt;&lt;br&gt;"
        "&lt;font style=&quot;font-size:12px;font-family:Tahoma;&quot;&gt;"
        "━━ Solid arrow → system flow&lt;br&gt;"
        "┅┅ Orange dashed → governance / review boundary&lt;br&gt;"
        "🟥 Pink / Red nodes → operational human interaction&lt;br&gt;"
        "Inner dashed ring → model evolution loop&lt;br&gt;"
        "Outer ring → runtime operational loop"
        "&lt;/font&gt;"
    )
    cells.append(f'''<mxCell id="{leg_id}" value="{legend_text}" style="rounded=1;whiteSpace=wrap;html=1;{SKETCH}shadow=1;fillColor=#f5f5f5;gradientColor=#DDDDDD;strokeColor=#999999;strokeWidth=1;align=left;verticalAlign=top;spacing=10;arcSize=10;fontFamily=Tahoma;fontSize=13;fontColor=#444444;" vertex="1" parent="1"><mxGeometry x="{leg_x}" y="{leg_y}" width="{leg_w}" height="{leg_h}" as="geometry"/></mxCell>''')

    # ── Bottom insight band ──
    band_y = H - 90
    band_h = 75
    band_id = nid()
    insight = (
        "&lt;i&gt;&quot;Many production AI systems are loop-shaped, but not closed-loop. "
        "Human feedback, curation, and governance introduce delay, filtering, "
        "and control boundaries that prevent true autonomy.&quot;&lt;/i&gt;"
    )
    cells.append(f'''<mxCell id="{band_id}" value="{insight}" style="rounded=1;whiteSpace=wrap;html=1;{SKETCH}shadow=1;fillColor=#E8E4DD;gradientColor=#D0C9BD;strokeColor=#B0A890;strokeWidth=2;fontFamily=Tahoma;fontSize=15;fontColor=#504D47;align=center;verticalAlign=middle;arcSize=8;spacing=12;" vertex="1" parent="1"><mxGeometry x="40" y="{band_y}" width="{W - 80}" height="{band_h}" as="geometry"/></mxCell>''')

    # ── Author line ──
    author_id = nid()
    cells.append(f'''<mxCell id="{author_id}" value="&lt;font style=&quot;font-size:14px;font-family:Architects Daughter;&quot;&gt;by: &lt;i&gt;&lt;b&gt;Steven Miers&lt;/b&gt;&lt;/i&gt;&lt;/font&gt;" style="text;html=1;align=right;verticalAlign=middle;strokeColor=none;fillColor=none;fontFamily=Architects Daughter;fontSize=14;fontColor=#504D47;" vertex="1" parent="1"><mxGeometry x="{W - 300}" y="{H - 35}" width="260" height="30" as="geometry"/></mxCell>''')

    # ── Assemble full XML ──
    xml = f'''<mxfile host="Electron" agent="draw.io" version="29.3.0">
  <diagram name="HITL Infographic" id="hitl-infographic-v1">
    <mxGraphModel dx="1920" dy="1200" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="{W}" pageHeight="{H}" background="#FCF5E5" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
        {"".join(cells)}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''
    return xml


if __name__ == "__main__":
    xml = build_drawio()
    with open("/home/claude/hitl-infographic.drawio", "w") as f:
        f.write(xml)
    print(f"Generated {len(xml)} bytes")
    # Quick sanity: print node positions
    for nodes in [
        [("inference",70,570,480),("product_ui",110,570,480),("expert_user",160,570,480),
         ("data_store",210,570,480),("pipeline",260,570,480),("training",310,570,480)],
        [("model_ensemble",300,285,240),("deployment",0,285,240),("inference_link",40,285,240)],
        [("curation",320,420,355),("governance",20,420,355)],
    ]:
        for name, angle, rx, ry in nodes:
            x, y = ellipse_pos(angle, rx, ry)
            print(f"  {name:20s}  {angle:4d}°  →  ({x:5d}, {y:5d})")
