
import pandas as pd
import streamlit as st

from executive_summary import (
    generate_executive_summary,
    generate_business_recommendations,
)
from powerpoint_export import create_powerpoint


st.set_page_config(
    page_title="CIA Executive Insights",
    page_icon="📊",
    layout="wide",
)

st.title("📊 CIA Executive Insights Generator")
st.write(
    "Analyze a business dataset, generate an AI-powered executive "
    "summary, and export business recommendations to PowerPoint."
)

uploaded_file = st.file_uploader(
    "Upload a business CSV file",
    type=["csv"],
)

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as exc:
        st.error(f"Could not read the CSV file: {exc}")
        st.stop()

    if df.empty:
        st.warning("The uploaded CSV contains no data rows.")
        st.stop()

    st.subheader("1. Dataset overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", f"{df.shape[0]:,}")
    col2.metric("Columns", f"{df.shape[1]:,}")
    col3.metric("Missing cells", f"{int(df.isna().sum().sum()):,}")

    with st.expander("Preview dataset"):
        st.dataframe(df.head(20), use_container_width=True)

    with st.expander("Descriptive statistics"):
        st.dataframe(
            df.describe(include="all").transpose(),
            use_container_width=True,
        )

    st.subheader("2. Automated EDA insights")

    insights = []

    insights.append(
        f"The dataset contains {df.shape[0]} rows and "
        f"{df.shape[1]} columns."
    )

    missing_total = int(df.isna().sum().sum())
    missing_percent = (
        missing_total / (df.shape[0] * df.shape[1]) * 100
        if df.size else 0
    )

    if missing_total:
        insights.append(
            f"The dataset contains {missing_total} missing cells "
            f"({missing_percent:.2f}% of all cells)."
        )
    else:
        insights.append("No missing cells were detected in the dataset.")

    duplicate_count = int(df.duplicated().sum())
    insights.append(
        f"The dataset contains {duplicate_count} fully duplicated rows."
    )

    # Exclude likely identifier columns from numeric business statistics.
    numeric_columns = df.select_dtypes(include="number").columns.tolist()
    business_numeric_columns = [
        column for column in numeric_columns
        if not any(
            token in str(column).lower()
            for token in ("id", "identifier", "code")
        )
    ]

    if business_numeric_columns:
        numeric_column = business_numeric_columns[0]
        mean_value = df[numeric_column].mean()
        median_value = df[numeric_column].median()

        insights.append(
            f"For {numeric_column}, the mean is {mean_value:.2f} "
            f"and the median is {median_value:.2f}."
        )
    elif numeric_columns:
        insights.append(
            "Numeric columns appear to contain identifiers or codes; "
            "review their meanings before interpreting their statistics."
        )
    else:
        insights.append(
            "No numeric columns were detected for numerical analysis."
        )

    categorical_columns = df.select_dtypes(
        include=["object", "category", "bool", "string"]
    ).columns.tolist()

    if categorical_columns:
        category_column = categorical_columns[0]
        counts = df[category_column].dropna().value_counts()

        if not counts.empty:
            most_common = counts.index[0]
            frequency = int(counts.iloc[0])
            percentage = frequency / len(df) * 100

            insights.append(
                f"The most frequent value in {category_column} is "
                f"'{most_common}', appearing {frequency} times "
                f"({percentage:.1f}% of all rows)."
            )
        else:
            insights.append(
                f"The column {category_column} has no non-missing "
                "categorical values to summarize."
            )
    else:
        insights.append(
            "No categorical columns were detected for category analysis."
        )

    # Keep exactly five insights for the AI functions and PowerPoint.
    insights = insights[:5]

    for number, insight in enumerate(insights, start=1):
        st.write(f"**Insight {number}:** {insight}")

    st.subheader("3. Generate AI executive summary")

    if st.button("Generate AI Summary and Recommendations", type="primary"):
        st.session_state.pop("executive_summary", None)
        st.session_state.pop("recommendations", None)
        st.session_state.pop("insights", None)

        with st.spinner("Generating the executive summary with Groq..."):
            try:
                summary_text = generate_executive_summary(insights)
                st.session_state["executive_summary"] = summary_text
                st.session_state["insights"] = insights
            except Exception as exc:
                st.error(
                    f"Executive summary generation failed: "
                    f"{type(exc).__name__}"
                )
                st.write(str(exc) or repr(exc))

        if st.session_state.get("executive_summary"):
            with st.spinner("Generating business recommendations with Groq..."):
                try:
                    recommendations = generate_business_recommendations(
                        insights
                    )
                    st.session_state["recommendations"] = recommendations
                except Exception as exc:
                    st.error(
                        f"Recommendation generation failed: "
                        f"{type(exc).__name__}"
                    )
                    st.write(str(exc) or repr(exc))

    summary = st.session_state.get("executive_summary")
    saved_insights = st.session_state.get("insights")
    recommendations = st.session_state.get("recommendations")

    if summary and saved_insights:
        st.subheader("Executive Summary")
        st.write(summary)

    if recommendations:
        st.subheader("4. AI-Generated Business Recommendations")

        for number, recommendation in enumerate(recommendations, start=1):
            st.write(f"**{number}.** {recommendation}")

        st.caption(
            "Review AI-generated recommendations against the original "
            "data before using them for business decisions."
        )

    if summary and saved_insights and recommendations:
        st.subheader("5. Download Executive Report")

        try:
            ppt_bytes = create_powerpoint(
                saved_insights,
                summary,
                recommendations,
            )

            st.download_button(
                label="Download Executive PowerPoint",
                data=ppt_bytes,
                file_name="CIA_Executive_Insights_W8D2.pptx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "presentationml.presentation"
                ),
            )
        except Exception as exc:
            st.error(
                f"PowerPoint generation failed: {type(exc).__name__}"
            )
            st.write(str(exc) or repr(exc))

else:
    st.info("Upload a CSV file to begin your analysis.")
