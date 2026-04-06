"""Lab 4 — Descriptive Analytics: Student Performance EDA

Conduct exploratory data analysis on the student performance dataset.
Produce distribution plots, correlation analysis, hypothesis tests,
and a written findings report.

Usage:
    python eda_analysis.py
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats


def load_and_profile(filepath):
    """Load the dataset and generate a data profile report.

    Args:
        filepath: path to the CSV file (e.g., 'data/student_performance.csv')

    Returns:
        DataFrame: the loaded dataset

    Side effects:
        Saves a text profile to output/data_profile.txt containing:
        - Shape (rows, columns)
        - Data types for each column
        - Missing value counts per column
        - Descriptive statistics for numeric columns
    """
    #  Load the dataset and report its shape, data types, missing values,
    #       and descriptive statistics to output/data_profile.txt
    df = pd.read_csv(filepath)
    with open("output/data_profile.txt" , 'w') as f:
        f.write ("--- Data Profile Report ---\n")
        #shape
        f.write(f"Shape: {df.shape[0]} rows, {df.shape[1]} columns\n\n")
        #Data Type
        f.write("Data Types:\n")
        f.write(df.dtypes.to_string()+"\n\n")
        
        #missing values
        f.write("Missing values per column \n")
        missing = df.isnull().sum()
        f.write(missing.to_string()+"\n\n")
        f.write(" percentage of missng values : \n")
        f.write((missing / len(df) * 100).to_string()+"\n\n")
        #Handling Decisions & Reasoning
        f.write("Handling Decisions:\n")
        f.write("- commute_minutes: Impute with median (MCAR, ~10% missing).\n")
        f.write("- study_hours_weekly: Drop rows (MCAR, ~5% missing).\n\n")
         #Descriptive Statistics
        f.write("Descriptive Statistics:\n")
        f.write(df.describe().to_string())
        #Data Cleaning
        #Impute missing commute_minutes with the median value
        df['commute_minutes'] = df['commute_minutes'].fillna(df['commute_minutes'].median())
        #fill none value  in scholarship
        df['scholarship'] = df['scholarship'].fillna("None")
        #Drop rows where study_hours_weekly is missing
        df = df.dropna(subset=['study_hours_weekly'])

    return df    





def plot_distributions(df):
    """Create distribution plots for key numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least 3 distribution plots (histograms with KDE or box plots)
        as PNG files in the output/ directory. Each plot should have a
        descriptive title that states what the distribution reveals.
    """
    #  Create distribution plots for numeric columns like GPA,
    #       study hours, attendance, and commute minutes
    # Use histograms with KDE overlay (sns.histplot) or box plots
    # Save each plot to the output/ directory
    numeric_cols = ["gpa", "study_hours_weekly", "attendance_pct", "commute_minutes"]
    for col in numeric_cols:
        fig , ax = plt.subplots(figsize = (10,6))
        sns.histplot(df[col], bins=40, kde=True,ax=ax,color="blue") 

        mean_val = df[col].mean()
        median_val = df[col].median()

        ax.axvline(mean_val  ,color = "red", linestyle = "--",label =f"Mean = {mean_val:.2f}")
        ax.axvline(median_val ,color = "orange", linestyle = "--",label =f"Median = {median_val:.2f}")
        ax.set_title(f"Distribution of {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Frequency")
        ax.legend()
        fig.tight_layout()
        fig.savefig(f"output/{col}_distribution.png")
        plt.close(fig)
    # GPA by Department
    fig , ax = plt.subplots(figsize = (12,6))

    sns.boxenplot(data=df, x="department", y="gpa", ax=ax, palette="Set2")
    ax.set_title("GPA Distribution Across Department")
    ax.set_xlabel("Department")
    ax.set_ylabel("GPA")
    fig.tight_layout()
    fig.savefig("output/gpa_by_department.png")
    plt.close(fig)

    #Bar chart for scholarship 
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Using countplot to calculate frequencies for each category
    sns.countplot(data=df, x="scholarship", ax=ax, palette="viridis")
    
    # Adding descriptive titles and labels as per requirements
    ax.set_title("Distribution of Scholarships: Most students hold Partial or No Scholarship")
    ax.set_xlabel("Scholarship Type")
    ax.set_ylabel("Number of Students")
    
    fig.tight_layout()
    fig.savefig("output/scholarship_distribution.png")
    plt.close(fig)



def plot_correlations(df):
    """Analyze and visualize relationships between numeric variables.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        None

    Side effects:
        Saves at least one correlation visualization to the output/ directory
        (e.g., a heatmap, scatter plot, or pair plot).
    """
    #  Compute the correlation matrix for numeric columns
    #  Create a heatmap or scatter plots showing key relationships
    #  Save the visualization(s) to the output/ directory
    numeric_cols = ["gpa", "study_hours_weekly", "attendance_pct"]
    corr = df[numeric_cols].corr().round(3)
   
    fig ,ax = plt.subplots(figsize=(8,6))
    mask = np.triu(np.ones_like(corr,dtype=bool))
    sns.heatmap(corr,annot=True, fmt=".2f", mask=mask,linewidths=0.5,
                cmap="coolwarm", center=0 , ax=ax,
                 linecolor ="white", square=True )
    ax.set_title("Correlations Heatmap")
    fig.tight_layout()
    fig.savefig("output/correlation_heatmap.png", dpi=120)
    plt.close(fig)

    #scatter : gpa by  study_hours_weekly
    r_study = corr.loc["gpa", "study_hours_weekly"]
    fig , ax = plt.subplots(figsize = (8,6))
    sns.scatterplot(data=df, x="study_hours_weekly", y="gpa", alpha=0.5, ax=ax)
    ax.set_title(f"Relationship: Study Hours vs GPA (r = {r_study:.2f})")
    ax.set_xlabel("Weekly Study Hours")
    ax.set_ylabel("GPA")
    fig.savefig("output/scatter_study_gpa.png")
    plt.close(fig)


    #scatter : gpa by attendance_pct
    r_attendance = corr.loc["gpa", "attendance_pct"]
    fig , ax = plt.subplots(figsize = (8,6))
    sns.scatterplot(data=df, x="attendance_pct", y="gpa", alpha=0.5, ax=ax)
    ax.set_title(f"Relationship: Attendance vs GPA (r = {r_attendance:.2f})")
    ax.set_xlabel("Attendance Percentage (%)")
    ax.set_ylabel("GPA")
    fig.savefig("output/attendance_gpa.png")
    plt.close(fig)

def run_hypothesis_tests(df):
    """Run statistical tests to validate observed patterns.

    Args:
        df: pandas DataFrame with the student performance data

    Returns:
        dict: test results with keys like 'internship_ttest', 'dept_anova',
              each containing the test statistic and p-value

    Side effects:
        Prints test results to stdout with interpretation.

    Tests to consider:
        - t-test: Does GPA differ between students with and without internships?
        - ANOVA: Does GPA differ across departments?
        - Correlation test: Is the correlation between study hours and GPA significant?
    """
    # TODO: Run at least two hypothesis tests on patterns you observe in the data
    # TODO: Report the test statistic, p-value, and your interpretation
    pass


def main():
    """Orchestrate the full EDA pipeline."""
    os.makedirs("output", exist_ok=True)
    file_path = "data/student_performance.csv"
    
    #  Load and profile the dataset
    df=load_and_profile(file_path)
    print ("Data loaded, profiled, and cleaned successfully")
    #  Generate distribution plots
    plot_distributions(df)
    #  Analyze correlations
    plot_correlations(df)
    # TODO: Run hypothesis tests
    # TODO: Write a FINDINGS.md summarizing your analysis


if __name__ == "__main__":
    main()
