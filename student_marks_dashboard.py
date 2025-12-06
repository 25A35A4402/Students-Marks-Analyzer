import streamlit as st
import pandas as pd

st.set_page_config(page_title="Student Marks + Ranking Dashboard", layout="wide")

st.title("📘 Student Marks Analyzer")

file_path = r"C:\Users\gunasri\Downloads\andhra_student_marks_DMGT_JAVA_IDS_UHV_ADSAA.csv"
df = pd.read_csv(file_path)


subjects = ["DMGT", "JAVA", "IDS", "UHV", "ADSAA"]

# ------- CALCULATIONS ------- #
df["Total"] = df[subjects].sum(axis=1)
df["Average"] = df[subjects].mean(axis=1)

def get_grade(avg):
    if avg >= 90: return "A+"
    elif avg >= 80: return "A"
    elif avg >= 70: return "B"
    elif avg >= 60: return "C"
    else: return "D"

df["Grade"] = df["Average"].apply(get_grade)
df["Rank"] = df["Total"].rank(method="min", ascending=False).astype(int)

df = df.sort_values(by="Rank").reset_index(drop=True)

st.subheader("📋 All Students Details (Before Ranking)")
st.dataframe(df, use_container_width=True)

st.markdown("---")

st.header("🏆 Ranking System")

# Show topper
topper = df[df["Rank"] == 1].iloc[0]

st.subheader("🎉 Class Topper")
st.write(f"**Name:** {topper['Name']}")
st.write(f"**Total Marks:** {topper['Total']}")
st.write(f"**Average:** {topper['Average']:.2f}")
st.write(f"**Grade:** {topper['Grade']}")

st.markdown("---")

# Search for a student's rank
st.subheader("🔍 Search Student Rank")
search = st.text_input("Enter roll number or name")

if st.button("Search"):
    result = pd.DataFrame()

    if search.isdigit():
        result = df[df["Roll_No"] == int(search)]
    else:
        result = df[df["Name"].str.contains(search, case=False, na=False)]

    if result.empty:
        st.error("Student not found!")
    else:
        st.success("Student Found!")
        st.dataframe(result)

        stud = result.iloc[0]
        st.write(f"### 🏅 Rank: **{stud['Rank']}**")
        st.write(f"### 📊 Total Marks: **{stud['Total']}**")
        st.write(f"### 📉 Average: **{stud['Average']:.2f}**")
        st.write(f"### 🎯 Grade: **{stud['Grade']}**")

st.markdown("---")

# Ranking Table
st.subheader("📚 Final Ranking Table (Sorted by Rank)")
st.dataframe(df[["Rank", "Roll_No", "Name", "Total", "Average", "Grade"]], use_container_width=True)
