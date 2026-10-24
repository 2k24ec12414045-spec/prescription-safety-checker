
import streamlit as st
import pandas as pd

from database_validation import validate_database
from safety_engine import (
    check_duplicate_ingredients,
    check_drug_interactions,
)


# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="MedGuard | Prescription Review",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------- CUSTOM CSS ----------------

st.markdown(
    """
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&display=swap'
    );

    .stApp {
        background: linear-gradient(
            135deg, #f4f7fc 0%, #eef4fb 55%, #f8faff 100%
        );
        font-family: 'DM Sans', sans-serif;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #101c35;
    }

    [data-testid="stSidebar"] * {
        color: #f3f6ff;
    }

    .brand {
        font-size: 1.85rem;
        font-weight: 700;
        color: #152b4a;
        letter-spacing: -0.8px;
    }

    .brand span {
        color: #2878e5;
    }

    .subtitle {
        color: #65748b;
        font-size: 0.98rem;
        margin-top: 0.25rem;
        margin-bottom: 1.3rem;
    }

    .hero {
        background: linear-gradient(120deg, #132644, #245c9d);
        padding: 30px;
        border-radius: 20px;
        color: white;
        margin: 12px 0 25px 0;
        box-shadow: 0 12px 30px rgba(24, 54, 96, 0.13);
    }

    .hero h2 {
        color: white;
        font-size: 1.8rem;
        margin: 0 0 10px 0;
    }

    .hero p {
        color: #e1ebfa;
        margin-bottom: 0;
        line-height: 1.7;
    }

    .section-title {
        font-size: 1.25rem;
        font-weight: 700;
        color: #172d4c;
        margin: 20px 0 10px 0;
    }

    .small-muted {
        color: #6d7b91;
        font-size: 0.9rem;
    }

    div[data-testid="stMetric"] {
        background: white;
        border: 1px solid #e2eaf5;
        padding: 17px;
        border-radius: 15px;
        box-shadow: 0 4px 14px rgba(26, 48, 79, 0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #60728b;
    }

    div[data-testid="stMetricValue"] {
        color: #18385e;
        font-weight: 700;
    }

    div.stButton > button,
    div.stDownloadButton > button {
        border-radius: 10px;
        min-height: 45px;
        font-weight: 600;
        border: 1px solid #d5e1f1;
        transition: all 0.2s ease;
    }

    div.stButton > button[kind="primary"] {
        background: #246fe5;
        border-color: #246fe5;
        color: white;
    }

    div.stButton > button:hover,
    div.stDownloadButton > button:hover {
        border-color: #246fe5;
        transform: translateY(-1px);
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: white;
        border-radius: 15px;
        border-color: #e2eaf5;
    }

    textarea {
        border-radius: 12px !important;
    }

    hr {
        border-color: #dfe7f2;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------- SIDEBAR ----------------

with st.sidebar:
    st.markdown(
        """
        <div style="padding: 12px 0 24px 0;">
            <div style="font-size: 2rem;">💊</div>
            <div style="font-size: 1.4rem; font-weight: 700;">
                MedGuard
            </div>
            <div style="font-size: 0.8rem; color: #b8c8e2;">
                HM-02 · Prescription Review
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    st.markdown("### Navigation")
    st.markdown("🏠  Prescription Review")
    st.markdown("🧪  Safety Checks")
    st.markdown("📄  Review Report")

    # Database validation
    st.divider()
    st.markdown("### Database Health")

    if st.button("🔄 Validate Database", use_container_width=True):
        validation = validate_database()

        if validation["valid"]:
            st.success("Database structure is valid.")
        else:
            st.error("Database validation failed.")

        st.caption(
            f"Medicine records: {validation['medicine_count']}"
        )
        st.caption(
            f"Interaction rules: {validation['rule_count']}"
        )

        for error in validation["errors"]:
            st.error(error)

        for warning in validation["warnings"]:
            st.warning(warning)

    st.divider()

    st.markdown("### About this project")
    st.caption(
        "An evidence-aware educational prototype for medicine "
        "identification, duplicate ingredient review and configured "
        "drug interaction rules."
    )

    st.divider()

    st.markdown("### Data status")
    st.caption("Local CSV database")
    st.caption("Only verified records and rules are used for checks.")

    st.warning(
        "This prototype does not confirm prescription safety."
    )


# ---------------- HEADER ----------------

st.markdown(
    """
    <div class="brand">Med<span>Guard</span></div>
    <div class="subtitle">
        Evidence-aware prescription review · HM-02
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero">
        <h2>Prescription Safety Review</h2>
        <p>
            Review medicine identification, look for duplicate active
            ingredients, and check configured verified interaction rules.
            Uncertain or unverified records require manual review.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.info(
    "Educational prototype only. This application cannot determine "
    "whether a prescription is safe and does not replace review by "
    "a qualified healthcare professional."
)


# ---------------- INPUT SECTION ----------------

st.markdown(
    '<div class="section-title">01 · Enter medicines</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="small-muted">'
    'Enter one brand name per line. Unknown or unverified entries '
    'will require manual verification.'
    '</div>',
    unsafe_allow_html=True,
)

with st.container(border=True):
    medicine_text = st.text_area(
        "Medicine brand names",
        placeholder="DemoBrandA\nDemoBrandB\nunknown_brand",
        height=150,
        label_visibility="visible",
    )

    review_clicked = st.button(
        "🔎  Review Prescription",
        type="primary",
        use_container_width=True,
    )


# ---------------- REVIEW LOGIC ----------------

if review_clicked:
    medicine_names = [
        name.strip()
        for name in medicine_text.splitlines()
        if name.strip()
    ]

    if not medicine_names:
        st.error("Please enter at least one medicine name.")

    else:
        try:
            result = check_duplicate_ingredients(medicine_names)

            interaction_result = check_drug_interactions(
                medicine_names
            )

            st.markdown(
                '<div class="section-title">'
                '02 · Review overview</div>',
                unsafe_allow_html=True,
            )

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Medicines submitted",
                    len(medicine_names),
                )

            with col2:
                st.metric(
                    "Database matches",
                    len(result["matched_medicines"]),
                )

            with col3:
                st.metric(
                    "Unknown entries",
                    len(result["unknown_medicines"]),
                )

            # Medicine identification
            st.markdown(
                '<div class="section-title">'
                '03 · Medicine identification</div>',
                unsafe_allow_html=True,
            )

            with st.container(border=True):
                if result["matched_medicines"]:
                    st.success(
                        f'{len(result["matched_medicines"])} '
                        "database match(es) found."
                    )

                    for name in result["matched_medicines"]:
                        st.write(f"✓ {name}")

                else:
                    st.info("No medicine names matched the database.")

                if result["unknown_medicines"]:
                    st.warning(
                        "Manual verification required for these entries:"
                    )

                    for name in result["unknown_medicines"]:
                        st.write(f"• {name}")

            # Duplicate ingredient review
            st.markdown(
                '<div class="section-title">'
                '04 · Duplicate ingredient review</div>',
                unsafe_allow_html=True,
            )

            with st.container(border=True):
                if result["duplicates"]:
                    st.warning(
                        "Potential duplicate active ingredients detected. "
                        "Professional review is required."
                    )

                    st.json(result["duplicates"])

                else:
                    st.info(
                        "No duplicate ingredient was detected among "
                        "the verified records available to this prototype. "
                        "This is not proof of safety."
                    )

            # Drug interaction review
            st.markdown(
                '<div class="section-title">'
                '05 · Drug interaction review</div>',
                unsafe_allow_html=True,
            )

            with st.container(border=True):
                if interaction_result["interactions"]:
                    st.warning(
                        "One or more configured, verified interaction "
                        "rules matched. Professional review is required."
                    )

                    interaction_df = pd.DataFrame(
                        interaction_result["interactions"]
                    )

                    st.dataframe(
                        interaction_df,
                        use_container_width=True,
                        hide_index=True,
                    )

                else:
                    st.info(
                        "No configured, verified interaction rule matched. "
                        "This does not mean the medicines are safe to "
                        "take together."
                    )

                if interaction_result["unknown_medicines"]:
                    st.warning(
                        "Unknown medicines excluded from interaction "
                        "checking: "
                        + ", ".join(
                            interaction_result["unknown_medicines"]
                        )
                    )

                if interaction_result["unverified_medicines"]:
                    st.warning(
                        "Unverified entries excluded from interaction "
                        "checking: "
                        + ", ".join(
                            interaction_result["unverified_medicines"]
                        )
                    )

            # CSV report
            st.markdown(
                '<div class="section-title">'
                '06 · Download review report</div>',
                unsafe_allow_html=True,
            )

            report_rows = []

            for name in medicine_names:
                if name in result["unknown_medicines"]:
                    identification_status = (
                        "Unknown - Manual Verification Required"
                    )

                elif name in result["matched_medicines"]:
                    identification_status = (
                        "Matched - Verify Evidence and Record Status"
                    )

                else:
                    identification_status = "Not Confirmed"

                if name in interaction_result["unknown_medicines"]:
                    interaction_status = (
                        "Not Checked - Medicine Unknown"
                    )

                elif name in interaction_result["unverified_medicines"]:
                    interaction_status = (
                        "Not Checked - Medicine Unverified"
                    )

                else:
                    interaction_status = (
                        "Checked Against Configured Verified Rules"
                    )

                report_rows.append({
                    "Medicine Entered": name,
                    "Identification Status": identification_status,
                    "Interaction Review Status": interaction_status,
                })

            report_df = pd.DataFrame(report_rows)

            with st.container(border=True):
                st.caption(
                    "The report records identification and review status. "
                    "It is not a clinical clearance certificate."
                )

                st.download_button(
                    label="📥  Download CSV Report",
                    data=report_df.to_csv(
                        index=False
                    ).encode("utf-8"),
                    file_name="prescription_review_report.csv",
                    mime="text/csv",
                    use_container_width=True,
                )

            # Limitations
            with st.expander("Important limitations and review notes"):
                st.write(result["note"])
                st.write(interaction_result["note"])

                st.write(
                    "The quality of results depends on the completeness "
                    "and verification of the local medicine database and "
                    "interaction rules. Missing rules or records can cause "
                    "relevant issues to go undetected."
                )

        except Exception as error:
            st.error(
                "The review could not be completed. Check the CSV "
                "database files and application configuration."
            )
            print(f"Review error: {error}")


# ---------------- FOOTER ----------------

st.divider()

st.markdown(
    """
    <div style="text-align: center; padding: 10px 0 20px 0;">
        <div style="font-weight: 600; color: #34506f;">
            MedGuard · HM-02
        </div>
        <div style="font-size: 0.8rem; color: #718096; margin-top: 5px;">
            Local educational prototype · Fictional demo records are
            unverified · Not for clinical decision-making
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)
