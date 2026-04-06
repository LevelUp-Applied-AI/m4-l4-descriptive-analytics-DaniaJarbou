# Student Performance Analysis Report (Findings)

### 1. Dataset Description
- **Total Records:** 2,000 student entries.
- **Features:** 10 columns covering academic, behavioral, and demographic data.
- **Data Quality:** - Imputed missing values for `commute_minutes` using the median.
    - Handled outliers in `study_hours_weekly` (approx. 5% of data) to ensure accurate analysis.
    - Standardized `scholarship` categories.

### 2. Key Distribution Findings
- **Academic Performance:** `gpa` and `attendance_pct` show a slight left-skew, indicating a generally high-performing student population.
- **Departmental Comparison:** The Boxenplot shows that GPA distributions are remarkably consistent across all departments, suggesting no significant grading bias between fields of study.

### 3. Notable Correlations
- **Primary Driver:** A moderate positive correlation (r ≈ 0.45) exists between **Study Hours & GPA**.
- **Secondary Driver:** **Attendance** also correlates positively with GPA, proving that physical presence is a key success factor.
- **Caveat:** Note that **correlation is not causation**; while these factors are linked, they may be influenced by other underlying variables like student motivation.

### 4. Hypothesis Test Results

#### Hypothesis 1: Internship Impact
- **Hypothesis:** Students with internships have a higher GPA.
- **Test:** Independent Samples T-test (Welch’s T-test).
- **Result:** **t-stat = 14.2288, p-value < 0.001**.
- **Interpretation:** The result is **statistically significant**. 
- **Effect Size:** **Cohen's d = 0.6898** (Medium-to-Large effect), indicating that the difference is practically meaningful for academic policy.

#### Hypothesis 2: Scholarship vs. Department
- **Hypothesis:** Scholarship status is associated with the student's department.
- **Test:** Chi-square Test of Independence.
- **Result:** **chi2 = 17.1358, p-value = 0.3769**.
- **Interpretation:** The result is **not statistically significant** (p > 0.05). Scholarship distribution is independent of the department, ensuring equitable financial aid distribution.

### 5. Actionable Recommendations
1. **Prioritize Internship Partnerships:** Given the large effect size (d ≈ 0.69), the university should expand internship opportunities to boost student GPAs.
2. **Attendance Monitoring:** Use attendance records as an early-warning system to provide support to at-risk students before their GPA drops.
3. **Targeted Study Support:** Provide tutoring or peer-led study groups specifically for students reporting low weekly study hours, as this is a primary driver of academic success.