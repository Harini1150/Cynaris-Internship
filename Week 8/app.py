
import pandas as pd
import streamlit as st

from executive_summary import generate_executive_summary
from powerpoint_export import create_powerpoint

st.set_page_config(
    page_title="CIA Executive Insights",
    page_icon="📊",
    layout="wide",
)

st.title("CIA Executive Insights Generator")
st.write(
    "Upload a business CSV, explore its data, generate five EDA insights, "
    "and create an AI-powered executive report."
)

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the CSV: {type(exc).__name__}: {exc}")
        st.stop()

    if df.empty:
        st.error("The uploaded CSV contains no data.")
        st.stop()

    st.subheader("1. Dataset overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{len(df):,}")
    col2.metric("Columns", f"{len(df.columns):,}")
    col3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

    with st.expander("Preview data"):
        st.dataframe(df.head(20), width="stretch")

    with st.expander("Descriptive statistics"):
        st.dataframe(df.describe(include="all").T, width="stretch")

    st.subheader("2. Generate five EDA insights")

    insights = []

    missing = df.isna().sum()
    missing_pct = missing / len(df) * 100

    insights.append(
        f"The dataset contains {len(df):,} rows and {len(df.columns)} columns."
    )

    if missing_pct.max() == 0:
        insights.append("No missing values were found in any column.")
    else:
        missing_col = missing_pct.idxmax()
        insights.append(
            f"The column with the highest missing-data percentage is "
            f"'{missing_col}' ({missing_pct[missing_col]:.1f}%)."
        )

    duplicate_count = int(df.duplicated().sum())
    insights.append(
        f"The dataset contains {duplicate_count:,} fully duplicated rows."
    )

    numeric_cols = df.select_dtypes(include="number").columns.tolist()

    if numeric_cols:
        numeric_col = numeric_cols[0]
        series = df[numeric_col].dropna()

        if not series.empty:
            insights.append(
                f"Numeric column '{numeric_col}' has mean "
                f"{series.mean():.2f} and median {series.median():.2f}."
            )
        else:
            insights.append(
                f"Numeric column '{numeric_col}' has no non-missing values."
            )
    else:
        insights.append(
            "The dataset has no numeric columns for numerical analysis."
        )

    categorical_cols = df.select_dtypes(
        include=["object", "category", "bool", "str"]
    ).columns.tolist()

    if categorical_cols:
        cat_col = categorical_cols[0]
        top_values = df[cat_col].value_counts(dropna=True)

        if not top_values.empty:
            top_value = top_values.index[0]
            share = top_values.iloc[0] / len(df) * 100

            insights.append(
                f"In '{cat_col}', the most frequent value is "
                f"'{top_value}' ({share:.1f}% of all rows)."
            )
        else:
            insights.append(
                f"Categorical column '{cat_col}' has no non-missing values."
            )
    else:
        insights.append("The dataset has no categorical columns.")

    for i, insight in enumerate(insights, start=1):
        st.write(f"**Insight {i}:** {insight}")

    st.subheader("3. Generate executive summary")

    if st.button("Generate AI Summary", type="primary"):
        st.session_state.pop("executive_summary", None)
        st.session_state.pop("insights", None)

        with st.spinner("Generating the executive summary with Groq..."):
            try:
                summary_text = generate_executive_summary(insights)

                st.session_state["executive_summary"] = summary_text
                st.session_state["insights"] = insights

            except Exception as exc:
                st.error(
                    f"Summary generation failed: {type(exc).__name__}"
                )

                st.write("Detailed error information:")
                st.code(str(exc) or repr(exc))

                error_body = getattr(exc, "body", None)
                st.write("API error body:")
                st.code(repr(error_body))

                response = getattr(exc, "response", None)

                if response is not None:
                    st.write(
                        "HTTP status: "
                        f"{getattr(response, 'status_code', 'Unknown')}"
                    )

                    try:
                        st.json(response.json())
                    except Exception:
                        st.code(response.text)

    summary = st.session_state.get("executive_summary")
    saved_insights = st.session_state.get("insights")

    if summary and saved_insights:
        st.subheader("Executive Summary")
        st.write(summary)

        st.subheader("4. Recommendations")

        recommendations = [
            "Investigate missing values and define an appropriate data-quality strategy.",
            "Review duplicate records before using the data for business reporting.",
            "Validate the observed numerical and categorical patterns with domain experts.",
        ]

        for item in recommendations:
            st.write(f"- {item}")

        try:
            ppt_bytes = create_powerpoint(
                saved_insights,
                summary,
                recommendations,
            )

            st.download_button(
                label="Download Executive PowerPoint",
                data=ppt_bytes,
                file_name="cia_executive_insights.pptx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "presentationml.presentation"
                ),
            )

        except Exception as exc:
            st.error(
                f"PowerPoint generation failed: "
                f"{type(exc).__name__}: {exc}"
            )

else:
    st.info("Upload a CSV file to begin the analysis.")
