import streamlit as st

from inference.predict_freight import predict_freight_cost
from inference.predict_invoice_flag import predict_invoice_flag

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------
st.set_page_config(
    page_title="Vendor Invoice Intelligence",
    page_icon="◆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -------------------------------------------------------
# Theme  —  "Modern Dark"
# Calm, composed, aesthetic. Deep dark grays and vibrant indigo.
# Inter (body & display) · JetBrains Mono (figures)
# Clean contrast, subtle glass-like borders.
# -------------------------------------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root{
  --bg:#0f1115;          /* very dark gray/black */
  --panel:#16181d;       /* slightly lighter for panels */
  --panel-2:#1c1e24;     /* even lighter for inputs/hover */
  --card:#1a1c22;        /* cards */
  --line:#2e323a;        /* borders */
  --line-strong:#3d424d; /* stronger borders */
  --ink:#f1f5f9;         /* off-white text */
  --muted:#94a3b8;       /* muted gray text */
  --faint:#475569;       /* very muted */
  --clay:#6366f1;        /* vibrant indigo */
  --clay-soft:rgba(99, 102, 241, 0.15);
  --sage:#10b981;        /* bright emerald */
  --sage-soft:rgba(16, 185, 129, 0.15);
  --brick:#ef4444;       /* bright red */
  --brick-soft:rgba(239, 68, 68, 0.15);
}

/* ---- Canvas ---- */
.stApp{
  background: var(--bg);
  color:var(--ink);
  font-family:'Inter',system-ui,sans-serif;
  cursor: default;
  caret-color: transparent;
}
::-webkit-scrollbar {
  display: none;
}
* {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
.block-container{padding-top:2.6rem;padding-bottom:4rem;max-width:1140px;}

h1,h2,h3,h4{font-family:'Inter',system-ui,sans-serif;letter-spacing:-.02em;color:var(--ink);font-weight:600;}
p,li,label,span,div{color:var(--ink);}

/* ---- Hero ---- */
.hero{
  border:1px solid var(--line);
  border-radius:16px;
  padding:40px 48px;
  background:var(--panel);
  box-shadow:0 4px 6px -1px rgba(0,0,0,0.3), 0 2px 4px -1px rgba(0,0,0,0.2);
}
.hero .kicker{
  font-family:'JetBrains Mono',monospace;font-size:.75rem;letter-spacing:.2em;
  text-transform:uppercase;color:var(--clay);margin-bottom:16px;font-weight:600;
}
.hero h1{font-size:2.8rem;line-height:1.1;margin:0 0 14px;font-weight:600;letter-spacing:-0.03em;}
.hero h1 em{font-style:normal;color:var(--clay);}
.hero p{color:var(--muted);font-size:1.05rem;max-width:62ch;margin:0;line-height:1.6;font-weight:400;}

/* ---- Section label ---- */
.eyebrow{
  font-family:'JetBrains Mono',monospace;font-size:.75rem;letter-spacing:.2em;
  text-transform:uppercase;color:var(--faint);margin:12px 0 4px;font-weight:600;
}
.lede{color:var(--muted);font-size:1.05rem;line-height:1.6;max-width:66ch;font-weight:400;}
.hint{color:var(--muted);font-size:.9rem;line-height:1.55;max-width:78ch;font-weight:400;
  background:var(--clay-soft);border:1px solid rgba(99,102,241,.2);border-left:3px solid var(--clay);
  border-radius:10px;padding:12px 16px;margin:4px 0 14px;}
.hint b{color:var(--ink);font-weight:600;}

/* ---- Sidebar ---- */
[data-testid="stSidebar"]{
  background:var(--panel);
  border-right:1px solid var(--line);
}
[data-testid="stSidebar"] .block-container{padding-top:2.2rem;}
.brand{font-family:'Inter',sans-serif;font-size:1.4rem;font-weight:600;line-height:1.1;}
.brand b{color:var(--clay);font-weight:600;}
.brand-sub{font-family:'JetBrains Mono',monospace;font-size:.65rem;letter-spacing:.15em;
  text-transform:uppercase;color:var(--faint);margin-top:8px;}
.s-card{
  border:1px solid var(--line);border-radius:12px;padding:16px 18px;margin:12px 0;
  background:var(--bg);
}
.s-card .t{font-weight:600;font-size:.95rem;margin-bottom:6px;font-family:'Inter',sans-serif;color:var(--ink);}
.s-card .d{color:var(--muted);font-size:.85rem;line-height:1.5;font-weight:400;}
.s-foot{color:var(--faint);font-size:.75rem;line-height:1.6;margin-top:24px;
  border-top:1px solid var(--line);padding-top:16px;font-family:'JetBrains Mono',monospace;}

/* ---- Segmented control ---- */
div[data-testid="stSegmentedControl"] {
  margin: 8px 0 12px;
}
div[data-testid="stSegmentedControl"] > div {
  background-color: var(--panel-2) !important;
  border-radius: 10px !important;
  padding: 4px !important;
}
div[data-testid="stSegmentedControl"] div[data-baseweb="tab_highlight"],
div[data-testid="stSegmentedControl"] div[style*="position: absolute"] {
  display: none !important;
}
div[data-testid="stSegmentedControl"] label,
div[data-testid="stSegmentedControl"] button {
  background-color: transparent !important;
  border-radius: 8px !important;
  border: none !important;
  box-shadow: none !important;
  cursor: pointer !important;
}
div[data-testid="stSegmentedControl"] label p,
div[data-testid="stSegmentedControl"] label span,
div[data-testid="stSegmentedControl"] label div,
div[data-testid="stSegmentedControl"] button p,
div[data-testid="stSegmentedControl"] button span,
div[data-testid="stSegmentedControl"] button div {
  color: var(--muted) !important;
  font-family: 'Inter', sans-serif !important;
  font-weight: 500 !important;
}
div[data-testid="stSegmentedControl"] label:hover,
div[data-testid="stSegmentedControl"] button:hover {
  background-color: rgba(255, 255, 255, 0.05) !important;
}
div[data-testid="stSegmentedControl"] label:hover p,
div[data-testid="stSegmentedControl"] label:hover span,
div[data-testid="stSegmentedControl"] label:hover div,
div[data-testid="stSegmentedControl"] button:hover p,
div[data-testid="stSegmentedControl"] button:hover span,
div[data-testid="stSegmentedControl"] button:hover div {
  color: var(--ink) !important;
}
div[data-testid="stSegmentedControl"] label[data-checked="true"],
div[data-testid="stSegmentedControl"] label[aria-checked="true"],
div[data-testid="stSegmentedControl"] label:has(input:checked),
div[data-testid="stSegmentedControl"] button[aria-selected="true"],
div[data-testid="stSegmentedControl"] button[aria-checked="true"],
div[data-testid="stSegmentedControl"] button[data-checked="true"] {
  background-color: var(--panel) !important;
  box-shadow: 0 2px 4px rgba(0,0,0,0.3) !important;
}
div[data-testid="stSegmentedControl"] label[data-checked="true"] p,
div[data-testid="stSegmentedControl"] label[data-checked="true"] span,
div[data-testid="stSegmentedControl"] label[data-checked="true"] div,
div[data-testid="stSegmentedControl"] label:has(input:checked) p,
div[data-testid="stSegmentedControl"] label:has(input:checked) span,
div[data-testid="stSegmentedControl"] label:has(input:checked) div,
div[data-testid="stSegmentedControl"] button[aria-selected="true"] p,
div[data-testid="stSegmentedControl"] button[aria-selected="true"] span,
div[data-testid="stSegmentedControl"] button[aria-selected="true"] div {
  color: var(--ink) !important;
}

/* ---- Segmented control: kill all white borders/outlines ---- */
div[data-testid="stSegmentedControl"] *{outline:none!important;box-shadow:none!important;}
div[data-testid="stSegmentedControl"] [role="radiogroup"],
div[data-testid="stSegmentedControl"] > div{
  background:var(--panel-2)!important;border:1px solid var(--line)!important;border-radius:10px!important;}
div[data-testid="stSegmentedControl"] label,
div[data-testid="stSegmentedControl"] button{border:none!important;background:transparent!important;}
div[data-testid="stSegmentedControl"] label:has(input:checked),
div[data-testid="stSegmentedControl"] button[aria-checked="true"],
div[data-testid="stSegmentedControl"] button[aria-selected="true"]{
  background:var(--clay)!important;border-radius:8px!important;}
div[data-testid="stSegmentedControl"] label:has(input:checked) p,
div[data-testid="stSegmentedControl"] button[aria-checked="true"] p,
div[data-testid="stSegmentedControl"] button[aria-selected="true"] p{color:#ffffff!important;}

/* ---- Inputs ---- */
[data-testid="stNumberInput"] label p,
[data-testid="stSelectbox"] label p {
  color:var(--muted)!important;font-size:.75rem!important;
  font-family:'JetBrains Mono',monospace;letter-spacing:.05em;text-transform:uppercase;font-weight:600;
}
/* the visible box is the BaseWeb wrapper — style it and kill its white border */
[data-testid="stNumberInput"] div[data-baseweb="input"],
[data-testid="stNumberInput"] div[data-baseweb="base-input"],
[data-testid="stSelectbox"] div[data-baseweb="select"] {
  background:var(--panel-2)!important;
  border:1px solid var(--line-strong)!important;border-radius:10px!important;
  box-shadow:none!important;
}
[data-testid="stNumberInput"] div[data-baseweb="input"]:focus-within,
[data-testid="stSelectbox"] div[data-baseweb="select"]:focus-within {
  border-color:var(--clay)!important;box-shadow:0 0 0 3px var(--clay-soft)!important;
}
[data-testid="stNumberInput"] input,
[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
  background:transparent!important;color:var(--ink)!important;
  border:none!important;outline:none!important;box-shadow:none!important;
  font-family:'JetBrains Mono',monospace!important;font-size:1rem!important;
}
[data-testid="stSelectbox"] div[data-baseweb="select"] span {
  color:var(--ink)!important;
}
[data-testid="stNumberInput"] button{
  background:var(--bg)!important;color:var(--muted)!important;
  border:none!important;box-shadow:none!important;
}
[data-testid="stNumberInput"] button:hover{color:var(--ink)!important;background:var(--panel-2)!important;}
/* caption hints under each field */
[data-testid="stNumberInput"] + div [data-testid="stCaptionContainer"],
.stCaption p, [data-testid="stCaptionContainer"] p{
  color:var(--faint)!important;font-family:'JetBrains Mono',monospace!important;
  font-size:.68rem!important;letter-spacing:.02em!important;}
[data-testid="stForm"]{border:1px solid var(--line)!important;border-radius:16px!important;
  background:var(--panel)!important;padding:32px 36px!important;box-shadow:0 4px 6px -1px rgba(0,0,0,0.2)!important;}

/* ---- Buttons ---- */
.stButton button,.stFormSubmitButton button{
  background:var(--clay)!important;color:#ffffff!important;border:none!important;
  border-radius:10px!important;font-family:'Inter',sans-serif!important;
  font-weight:500!important;letter-spacing:0!important;padding:.65rem 1.6rem!important;
  transition:all .2s ease!important;
  box-shadow:0 4px 6px -1px rgba(99,102,241,0.2)!important;
}
.stButton button:hover,.stFormSubmitButton button:hover{
  background:#4f46e5!important;transform:translateY(-1px)!important;
  box-shadow:0 6px 8px -1px rgba(99,102,241,0.3)!important;
}

/* ---- Result cards ---- */
.result{
  border:1px solid var(--line-strong);border-radius:16px;padding:32px 36px;margin-top:24px;
  background:var(--card);box-shadow:0 4px 6px -1px rgba(0,0,0,0.2);
  animation:rise .4s cubic-bezier(0.16, 1, 0.3, 1) both;
}
@keyframes rise{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:none}}
.result.flag{background:rgba(239, 68, 68, 0.03);border-color:rgba(239, 68, 68, 0.2);}
.result.safe{background:rgba(16, 185, 129, 0.03);border-color:rgba(16, 185, 129, 0.2);}
.result.cost{background:rgba(99, 102, 241, 0.03);border-color:rgba(99, 102, 241, 0.2);}

.pill{display:inline-flex;align-items:center;gap:6px;font-family:'JetBrains Mono',monospace;
  font-size:.7rem;letter-spacing:.15em;text-transform:uppercase;padding:6px 14px;border-radius:999px;font-weight:600;}
.pill.flag{color:#f87171;background:rgba(239, 68, 68, 0.15);border:1px solid rgba(239, 68, 68, 0.3);}
.pill.safe{color:#34d399;background:rgba(16, 185, 129, 0.15);border:1px solid rgba(16, 185, 129, 0.3);}
.pill.cost{color:#818cf8;background:rgba(99, 102, 241, 0.15);border:1px solid rgba(99, 102, 241, 0.3);}

.result h2{font-size:1.6rem;margin:18px 0 8px;font-weight:600;letter-spacing:-0.02em;}
.bignum{font-family:'JetBrains Mono',monospace;font-size:3.2rem;font-weight:600;
  letter-spacing:-.03em;line-height:1;margin:12px 0 4px;}
.bignum.cost{color:var(--clay);}
.subnum{color:var(--muted);font-size:.95rem;font-family:'JetBrains Mono',monospace;}
.narr{color:var(--ink);font-size:1.05rem;line-height:1.6;margin:18px 0 8px;max-width:72ch;font-weight:400;}
.narr b{color:var(--ink);font-weight:600;}

/* confidence meter */
.conf{margin:24px 0 8px;}
.conf .lab{display:flex;justify-content:space-between;font-family:'JetBrains Mono',monospace;
  font-size:.75rem;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-bottom:10px;font-weight:600;}
.track{height:8px;border-radius:999px;background:var(--line);overflow:hidden;}
.fill{height:100%;border-radius:999px;}
.fill.flag{background:var(--brick);}
.fill.safe{background:var(--sage);}

/* factor list */
.factors{list-style:none;padding:0;margin:24px 0 0;border-top:1px solid var(--line);padding-top:20px;}
.factors li{display:flex;gap:14px;align-items:flex-start;color:var(--muted);font-size:.95rem;
  line-height:1.6;padding:8px 0;font-weight:400;}
.factors li .mk{color:var(--clay);font-family:'JetBrains Mono',monospace;flex:none;margin-top:2px;font-weight:600;}
.factors li b{color:var(--ink);font-weight:600;}

.action{margin-top:24px;border-top:1px solid var(--line);padding-top:20px;
  color:var(--muted);font-size:1rem;line-height:1.6;font-weight:400;}
.action .hd{font-family:'JetBrains Mono',monospace;font-size:.75rem;letter-spacing:.15em;
  text-transform:uppercase;color:var(--faint);margin-bottom:10px;font-weight:600;}
.action b{color:var(--ink);font-weight:600;}

hr{border:none;border-top:1px solid var(--line);margin:2rem 0;}
#MainMenu, footer {visibility: hidden !important; display: none !important;}
[data-testid="stHeader"] {background-color: transparent !important;}
[data-testid="stHeader"] .stAppDeployButton, [data-testid="stHeader"] .stActionButton {display: none !important;}
</style>
""",
    unsafe_allow_html=True,
)

# -------------------------------------------------------
# Sidebar
# -------------------------------------------------------
with st.sidebar:
    st.markdown(
        '<div class="brand">Ledger<b>·</b>IQ</div>'
        '<div class="brand-sub">Vendor Invoice Intelligence</div>',
        unsafe_allow_html=True,
    )
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        '<div class="s-card"><div class="t">Forecast freight</div>'
        '<div class="d">Estimate landed freight cost before the carrier bills you.</div></div>'
        '<div class="s-card"><div class="t">Catch risky invoices</div>'
        '<div class="d">Surface invoices that drift from their purchase order for human review.</div></div>'
        '<div class="s-card"><div class="t">Move money faster</div>'
        '<div class="d">Auto-clear the routine, escalate only the exceptions.</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="s-foot">Models: Linear Regression · Random Forest<br>'
        'Trained on vendor_invoice ledger</div>',
        unsafe_allow_html=True,
    )

# -------------------------------------------------------
# Hero
# -------------------------------------------------------
st.markdown(
    """
<div class="hero">
  <div class="kicker">Finance Operations · ML</div>
  <h1>Read every invoice <em>before</em> it costs you.</h1>
  <p>A quiet working desk for procurement finance — forecast freight on incoming
  vendor invoices and flag the ones that deserve a human's eyes, with a
  plain-language rationale behind every call.</p>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")
module = st.segmented_control(
    "Module",
    options=["Freight Cost Forecast", "Invoice Risk Review"],
    default="Freight Cost Forecast",
    label_visibility="collapsed",
)

# -------------------------------------------------------
# Freight Cost Forecast
# -------------------------------------------------------
if module == "Freight Cost Forecast":
    st.markdown('<div class="eyebrow">Module 01 — Regression</div>', unsafe_allow_html=True)
    st.markdown("### Freight Cost Forecast")
    st.markdown(
        '<p class="lede">Enter the invoice value and the model projects the freight you '
        "should expect to pay — useful for budgeting, margin analysis, and sanity-checking "
        "a carrier quote before approval.</p>",
        unsafe_allow_html=True,
    )

    with st.form("freight_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            distance_km = st.number_input("Distance (km)", min_value=1.0, value=150.0, step=10.0, format="%.1f")
            package_weight_kg = st.number_input("Package Weight (kg)", min_value=0.1, value=50.0, step=1.0, format="%.1f")
            delivery_mode = st.selectbox("Delivery Mode", ["standard", "express", "two day", "same day"])
        with c2:
            vehicle_type = st.selectbox("Vehicle Type", ["truck", "van", "ev van", "bike", "ev bike", "scooter"])
            package_type = st.selectbox("Package Type", ["electronics", "documents", "fragile items", "groceries", "cosmetics", "clothing", "pharmacy", "furniture", "automobile parts"])
        with c3:
            region = st.selectbox("Region", ["north", "south", "east", "west", "central"])
            weather_condition = st.selectbox("Weather", ["clear", "rainy", "foggy", "hot", "cold", "stormy"])
        
        submit_freight = st.form_submit_button("Forecast freight")

    if submit_freight:
        input_data = {
            "distance_km": [distance_km],
            "package_weight_kg": [package_weight_kg],
            "delivery_mode": [delivery_mode],
            "vehicle_type": [vehicle_type],
            "package_type": [package_type],
            "region": [region],
            "weather_condition": [weather_condition]
        }
        prediction = predict_freight_cost(input_data)["Predicted_Freight_INR"]
        freight = float(prediction[0])
        
        # Determine cost band
        cost_per_kg = freight / package_weight_kg if package_weight_kg else 0.0
        
        if cost_per_kg < 50:
            band = "highly economical for the route and weight profile"
        elif cost_per_kg < 200:
            band = "a typical freight burden you can budget against with confidence"
        else:
            band = "an elevated freight rate — worth confirming against the carrier's quote"

        st.markdown(
            '<div class="result cost">'
            '<span class="pill cost">◆ Freight Forecast</span>'
            f'<div class="bignum cost">₹{freight:,.0f}</div>'
            f'<div class="subnum">≈ ₹{cost_per_kg:,.1f} per kg</div>'
            f'<p class="narr">For shipping <b>{package_weight_kg}kg</b> over <b>{distance_km}km</b> '
            f'via <b>{delivery_mode}</b>, the model projects a freight cost of <b>₹{freight:,.0f}</b>. '
            f"This is {band}. Use it to pre-load freight into your landed-cost estimate "
            "and to challenge any carrier invoice that comes in materially higher.</p>"
            '<div class="action"><div class="hd">Suggested next step</div>'
            "Lock this figure into the purchase-order accrual. If the billed freight lands "
            "more than ~15% above this estimate, route the invoice to the risk review below "
            "before releasing payment.</div>"
            "</div>",
            unsafe_allow_html=True,
        )

# -------------------------------------------------------
# Invoice Risk Review
# -------------------------------------------------------
else:
    st.markdown('<div class="eyebrow">Module 02 — Classification</div>', unsafe_allow_html=True)
    st.markdown("### Invoice Risk Review")
    st.markdown(
        '<p class="lede">Compare what the vendor invoiced against what the purchase order '
        "says was ordered and received. The model returns a confidence-scored verdict on "
        "whether the invoice can auto-clear or needs a human signature.</p>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<p class="hint">An invoice <b>auto-clears</b> when its value and quantity line up with '
        "the purchase order. A large gap between the invoiced amount and the PO item total — or "
        "between invoiced and received quantities — is what drives the manual-approval flag. "
        "The defaults below show a clean, matching invoice; widen the gaps to see it flag.</p>",
        unsafe_allow_html=True,
    )

    with st.form("invoice_flag_form"):
        c1, c2, c3 = st.columns(3)
        with c1:
            invoice_quantity = st.number_input(
                "Invoice quantity", min_value=1, value=80, step=1, format="%d",
                help="Units billed on this invoice. Recommended: 10 – 5,000.",
            )
            st.caption("Range · 10 – 5,000 units")
            freight = st.number_input(
                "Freight cost (INR)", min_value=0, value=850, step=10, format="%d",
                help="Freight charged. Normally 0 – 5% of invoice value (often ₹0 – ₹10,000).",
            )
            st.caption("Range · ₹0 – ₹10,000")
        with c2:
            invoice_dollars = st.number_input(
                "Invoice value (INR)", min_value=1, value=250000, step=1000, format="%d",
                help="Total billed by the vendor. Recommended: ₹10,000 – ₹2,500,000.",
            )
            st.caption("Range · ₹10,000 – ₹2,500,000")
            total_item_quantity = st.number_input(
                "PO / received quantity", min_value=1, value=80, step=1, format="%d",
                help="Units on the purchase order / goods receipt. Match invoice quantity to auto-clear.",
            )
            st.caption("Tip · match the invoice quantity")
        with c3:
            total_item_dollars = st.number_input(
                "PO item total (INR)", min_value=1, value=250000, step=1000, format="%d",
                help="Expected total from the purchase order. Keep within ~₹500 of invoice value to auto-clear.",
            )
            st.caption("Tip · keep within ~₹500 of invoice value")
        submit_flag = st.form_submit_button("Review invoice")

    if submit_flag:
        result = predict_invoice_flag(
            {
                "invoice_quantity": [invoice_quantity],
                "invoice_dollars": [invoice_dollars],
                "Freight": [freight],
                "total_item_quantity": [total_item_quantity],
                "total_item_dollars": [total_item_dollars],
            }
        )
        is_flagged = bool(result["Predicted_Flag"][0])
        prob_flag = float(result["Flag_Probability"][0])
        confidence = (prob_flag if is_flagged else 1 - prob_flag) * 100

        # --- evidence the user can read ---
        dollar_gap = abs(invoice_dollars - total_item_dollars)
        qty_gap = abs(invoice_quantity - total_item_quantity)
        freight_ratio = (freight / invoice_dollars * 100) if invoice_dollars else 0.0

        factors = []
        if dollar_gap > 500:
            factors.append(
                f"The invoiced amount (<b>₹{invoice_dollars:,.0f}</b>) diverges from the "
                f"purchase-order item total (<b>₹{total_item_dollars:,.0f}</b>) by "
                f"<b>₹{dollar_gap:,.0f}</b> — the single strongest risk signal here."
            )
        else:
            factors.append(
                f"The invoiced amount matches the purchase-order item total closely "
                f"(within <b>₹{dollar_gap:,.0f}</b>), which is reassuring."
            )
        if qty_gap > 0:
            factors.append(
                f"Invoiced quantity (<b>{invoice_quantity:,}</b>) differs from PO/received "
                f"quantity (<b>{total_item_quantity:,}</b>) by <b>{qty_gap:,}</b> units."
            )
        else:
            factors.append("Invoiced and received quantities agree exactly.")
        factors.append(
            f"Freight is <b>{freight_ratio:.1f}%</b> of invoice value "
            f"(<b>₹{freight:,.0f}</b> on <b>₹{invoice_dollars:,.0f}</b>)."
        )

        factor_html = "".join(
            f'<li><span class="mk">›</span><span>{f}</span></li>' for f in factors
        )

        if is_flagged:
            verdict = (
                f"This invoice should be <b>held for manual approval</b>. The model is "
                f"<b>{confidence:.0f}% confident</b> it falls outside normal vendor-billing "
                "behaviour, primarily because its cost and quantity profile doesn't reconcile "
                "cleanly with the underlying purchase order."
            )
            action = (
                "Route to a finance analyst before payment. <b>Reconcile the invoice against "
                "the PO and goods-receipt note</b>, confirm freight terms with the carrier, "
                "and obtain sign-off before releasing funds."
            )
            st.markdown(
                '<div class="result flag">'
                '<span class="pill flag">⚑ Hold for review</span>'
                "<h2>Manual approval required</h2>"
                f'<p class="narr">{verdict}</p>'
                '<div class="conf"><div class="lab"><span>Model confidence</span>'
                f"<span>{confidence:.0f}%</span></div>"
                f'<div class="track"><div class="fill flag" style="width:{confidence:.0f}%"></div></div></div>'
                f'<ul class="factors">{factor_html}</ul>'
                f'<div class="action"><div class="hd">Recommended action</div>{action}</div>'
                "</div>",
                unsafe_allow_html=True,
            )
        else:
            verdict = (
                f"This invoice is <b>cleared for straight-through auto-approval</b>. The model "
                f"is <b>{confidence:.0f}% confident</b> it matches expected cost, quantity, and "
                "freight patterns for this vendor, so no manual reconciliation is needed."
            )
            action = (
                "Release for <b>automatic payment</b> on the normal schedule. No analyst "
                "intervention is required — keep it in the straight-through queue."
            )
            st.markdown(
                '<div class="result safe">'
                '<span class="pill safe">✓ Cleared</span>'
                "<h2>Safe for auto-approval</h2>"
                f'<p class="narr">{verdict}</p>'
                '<div class="conf"><div class="lab"><span>Model confidence</span>'
                f"<span>{confidence:.0f}%</span></div>"
                f'<div class="track"><div class="fill safe" style="width:{confidence:.0f}%"></div></div></div>'
                f'<ul class="factors">{factor_html}</ul>'
                f'<div class="action"><div class="hd">Recommended action</div>{action}</div>'
                "</div>",
                unsafe_allow_html=True,
            )
