import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="Decision Intelligence Dashboard",
    layout="wide"
)

st.title("AI Decision Intelligence & Governance Platform")
st.caption("Executive Dashboard — Credit Risk Decisioning")

ARTIFACTS_DIR = "reports/artifacts"

# -----------------------------
# Utilities
# -----------------------------
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

def require_file(path):
    if not os.path.exists(path):
        st.error(f"Missing required artifact: {path}")
        st.stop()

# -----------------------------
# Required artifacts (NO MODELS)
# -----------------------------
require_file(f"{ARTIFACTS_DIR}/decision_df.csv")
require_file(f"{ARTIFACTS_DIR}/fairness_df.csv")

decision_df = load_csv(f"{ARTIFACTS_DIR}/decision_df.csv")
fairness_df = load_csv(f"{ARTIFACTS_DIR}/fairness_df.csv")

st.success(
    "✅ Governed AI Decision System Active\n\n"
    "- Models trained offline\n"
    "- Decisions policy-controlled\n"
    "- Explanations & fairness audited\n"
    "- Dashboard consumes artifacts only"
)
# -----------------------------
# Sidebar controls
# -----------------------------
st.sidebar.header("Decision Policy Controls")

threshold = st.sidebar.slider(
    "Decision Threshold (prob_default)",
    min_value=0.05, max_value=0.95, value=0.35, step=0.01
)

auto_approve_max = st.sidebar.slider(
    "Auto-Approve Threshold",
    min_value=0.05, max_value=0.95, value=0.20, step=0.01
)

auto_reject_min = st.sidebar.slider(
    "Auto-Reject Threshold",
    min_value=0.05, max_value=0.95, value=0.60, step=0.01
)

st.sidebar.caption("Auto-Approve if prob_default ≤ Auto-Approve Threshold")
st.sidebar.caption("Auto-Reject if prob_default ≥ Auto-Reject Threshold")
st.sidebar.caption("Else → Manual Review")

# -----------------------------
# Policy engine
# -----------------------------
def apply_policy(prob):
    if prob <= auto_approve_max:
        return "Auto-Approve"
    elif prob >= auto_reject_min:
        return "Reject"
    return "Manual Review"

# -----------------------------
# SECTION A: Policy Decision Outcomes
# -----------------------------
st.subheader("A) Decision Outcomes Overview")

if "prob_default" not in decision_df.columns:
    st.error("decision_df must contain column: prob_default")
    st.stop()

decision_df_dash = decision_df.copy()
decision_df_dash["policy_decision"] = decision_df_dash["prob_default"].apply(apply_policy)

counts = decision_df_dash["policy_decision"].value_counts()

c1, c2, c3 = st.columns(3)
c1.metric("Auto-Approve", int(counts.get("Auto-Approve", 0)))
c2.metric("Manual Review", int(counts.get("Manual Review", 0)))
c3.metric("Reject", int(counts.get("Reject", 0)))

st.dataframe(
    counts.reset_index()
    .rename(columns={"index": "Decision", "policy_decision": "Count"}),
    use_container_width=True
)

# -----------------------------
# SECTION B: Risk Distribution
# -----------------------------
st.subheader("B) Risk Distribution")

fig, ax = plt.subplots()
ax.hist(decision_df_dash["prob_default"], bins=30)
ax.set_xlabel("Probability of Default")
ax.set_ylabel("Number of Customers")
st.pyplot(fig)

# -----------------------------
# SECTION C: Customer Decision Explanation (SHAP)
# -----------------------------
st.subheader("C) Customer Reason Codes")

reason_cols = [c for c in decision_df_dash.columns if "reason" in c.lower()]

if not reason_cols:
    st.warning(
        "No reason code columns found. "
        "Export reason codes from SHAP step into decision_df."
    )
else:
    idx = st.number_input(
        "Customer row index",
        min_value=0,
        max_value=len(decision_df_dash) - 1,
        value=0
    )

    row = decision_df_dash.iloc[int(idx)]

    st.json({
        "prob_default": float(row["prob_default"]),
        "policy_decision": row["policy_decision"]
    })

    rc_df = pd.DataFrame(
        {c: [row[c]] for c in reason_cols}
    ).T.rename(columns={0: "value"})

    st.dataframe(rc_df, use_container_width=True)

# -----------------------------
# SECTION D: Fairness & Governance
# -----------------------------
st.subheader("D) Fairness & Governance")

if "approved_flag" not in fairness_df.columns:
    st.warning("fairness_df missing approved_flag — regenerate fairness artifact.")
else:
    protected = [c for c in fairness_df.columns if c in ["SEX", "AGE_GROUP", "EDUCATION"]]

    if not protected:
        st.warning("No protected attributes found.")
    else:
        group_col = st.selectbox("Protected Attribute", protected)

        grp = (
            fairness_df
            .groupby(group_col)["approved_flag"]
            .mean()
            .reset_index(name="approval_rate")
        )

        min_rate = grp["approval_rate"].min()
        max_rate = grp["approval_rate"].max()
        di = min_rate / max_rate if max_rate > 0 else 0

        st.dataframe(grp, use_container_width=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Min Approval Rate", f"{min_rate:.3f}")
        c2.metric("Max Approval Rate", f"{max_rate:.3f}")
        c3.metric("Disparate Impact", f"{di:.3f}")

        if di < 0.8:
            st.error("80% Rule: FAIL — mitigation required")
        else:
            st.success("80% Rule: PASS")

        def governance_action(di):
            if di >= 0.8:
                return "No action required"
            elif di >= 0.6:
                return "Increase manual review for affected group"
            return "Disable auto-approval; enforce review"

        st.info(f"Recommended governance action: **{governance_action(di)}**")

# -----------------------------
# Footer
# -----------------------------
st.divider()
st.caption(
    "This dashboard intentionally consumes only governed artifacts — "
    "models remain offline for auditability and stability."
)