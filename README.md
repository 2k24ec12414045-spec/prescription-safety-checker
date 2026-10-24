# MedGuard — Prescription Safety Checker

**Project ID:** HM-02  
**Project Type:** Educational Software Prototype  
**Status:** Functional prototype with automated tests

## 1. Project Overview

MedGuard is a Python-based prescription review prototype designed to demonstrate medicine-name identification, duplicate active ingredient checks, and drug interaction checks against a locally maintained CSV database.

The application provides a Streamlit web interface where users can enter medicine brand names and review database matches, unknown entries, duplicate ingredient results, and configured drug interaction rules.

MedGuard uses a verification-aware approach: only medicine records and interaction rules marked as `verified` are used for the relevant safety checks. Unknown or unverified records require further review.

**Important:** MedGuard is an educational prototype, not a clinically validated medical application. It cannot determine whether a prescription is safe, and it must not be used to make medication decisions.

## 2. Features

- **Interactive web dashboard:** Enter medicine names through a Streamlit interface.
- **Medicine identification:** Match entered names against a local CSV database.
- **Duplicate ingredient review:** Identify repeated active ingredients across verified medicine records.
- **Configured interaction checks:** Compare ingredients against explicitly verified local interaction rules.
- **Unknown medicine handling:** Flag names that do not match the database.
- **Verification-aware results:** Exclude unverified medicine records and interaction rules from relevant checks.
- **Database validation:** Check CSV structure, required fields, duplicate brand names, review statuses, and database warnings.
- **CSV report export:** Download a report containing medicine identification and interaction review statuses.
- **Automated testing:** Use pytest to test the core functionality and database validation.

## 3. Technology Stack

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Streamlit | Interactive web dashboard |
| Pandas | CSV processing and tabular reports |
| pytest | Automated testing |
| CSV | Local medicine and interaction-rule storage |

## 4. Project Structure

```text
prescription-safety-checker/
├── app.py
├── safety_engine.py
├── medicines.csv
├── interaction_rules.csv
├── database_validation.py
├── test_safety.py
├── test_database_validation.py
├── README.md
└── .venv/
```

- `app.py` — Streamlit dashboard and prescription review workflow.
- `safety_engine.py` — Medicine matching, duplicate ingredient checks, and interaction-rule matching.
- `medicines.csv` — Local medicine records and their verification status.
- `interaction_rules.csv` — Local interaction rules and supporting source information.
- `database_validation.py` — CSV structure and data-quality validation.
- `test_safety.py` — Automated tests for core safety-engine functions.
- `test_database_validation.py` — Automated tests for database validation.
- `.venv/` — Local Python virtual environment; it should not be committed to Git.

## 5. Requirements

- Python 3.13 or a compatible Python version
- pip
- A web browser
- The Python packages listed below

Install the dependencies in an activated virtual environment:

```bash
python -m pip install streamlit pandas pytest
```

## 6. Installation and Setup

### Step 1: Open the project directory

In Windows PowerShell:

```powershell
cd "$HOME\Downloads\prescription-safety-checker"
```

### Step 2: Create a virtual environment

If one does not already exist:

```powershell
python -m venv .venv
```

### Step 3: Activate the environment

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& .\.venv\Scripts\Activate.ps1
```

If the environment is already activated, you can continue to the next step.

### Step 4: Install dependencies

```powershell
python -m pip install streamlit pandas pytest
```

### Step 5: Run the application

```powershell
python -m streamlit run app.py
```

Streamlit will display a local address in the terminal. Open that address in your browser to use the dashboard.

## 7. How to Use MedGuard

1. Start the Streamlit application.
2. Enter one medicine brand name per line in the input area.
3. Select **Review Prescription**.
4. Review the database matches and unknown medicine entries.
5. Review duplicate ingredient results.
6. Review any matches against configured, verified interaction rules.
7. Download the CSV review report if required.
8. Use the database validation option in the sidebar to inspect the CSV database structure and warnings.

A medicine match only indicates a database match. It does not independently establish the medicine's identity, suitability, or safety for a particular person.

## 8. Database Format

### Medicine database — `medicines.csv`

The medicine database uses these columns:

| Column | Description |
|---|---|
| `brand_name` | Brand name stored in the local database |
| `aliases` | Alternative names used for matching |
| `active_ingredients` | Ingredient names separated by `\|` when there are multiple entries |
| `review_status` | `verified` or `unverified` |
| `source` | Source or provenance of the record |

The current database contains fictional demonstration records marked `unverified`. These records are intended for software testing and are not real clinical reference data.

### Interaction rules — `interaction_rules.csv`

The interaction rules file uses these columns:

| Column | Description |
|---|---|
| `ingredient_a` | First ingredient in the rule |
| `ingredient_b` | Second ingredient in the rule |
| `severity` | Severity label supplied by the rule's source |
| `explanation` | Explanation associated with the rule |
| `source` | Reference supporting the rule |
| `review_status` | `verified` or `unverified` |

The current interaction rules file has a header but no data rows. Consequently, the prototype currently has no configured interaction rules available to generate interaction alerts.

Clinical rules should only be added after appropriate verification against reliable medical references and review by qualified professionals. Do not use invented rules or mark records as verified merely to produce demonstration alerts.

## 9. Running the Automated Tests

Run the complete test suite from the project directory:

```powershell
python -m pytest -v
```

The current development milestone has **10 passing tests** across the core functionality and database validation checks.

The tests verify software behavior and database structure. They do not establish clinical accuracy, completeness of medicine data, or the safety of any prescription.

To validate the local CSV database separately:

```powershell
python -c "from database_validation import validate_database; print(validate_database())"
```

A structurally valid database can still contain incomplete, outdated, or clinically unverified information.

## 10. Current Limitations

- The medicine records are fictional demonstration data and are marked unverified.
- No interaction rules are currently configured.
- Unknown or unverified entries cannot be fully assessed by the prototype.
- The application does not establish that a medicine is suitable for an individual patient.
- Missing records or rules may cause relevant issues to go undetected.
- The prototype has not been clinically validated.
- Results must not be interpreted as medical clearance or a recommendation to start, stop, or combine medicines.

## 11. Future Enhancements

Potential future improvements include:

- Integration with an appropriately licensed and maintained medicine reference database.
- Evidence tracking and review dates for medicine records and interaction rules.
- More comprehensive automated tests, including invalid CSV schemas and duplicate data cases.
- Improved handling of aliases and ambiguous medicine names.
- A detailed audit trail for database updates and review decisions.
- User interface improvements and expanded report formatting.
- Security, privacy, and deployment reviews before any broader use.

These are proposed enhancements and are not claims about existing functionality.

## 12. Educational and Safety Disclaimer

MedGuard is developed for educational and software demonstration purposes only. It is not a substitute for a pharmacist, doctor, or other qualified healthcare professional.

An empty result, a database match, or the absence of a configured interaction alert does not mean that a prescription is safe. Always consult a qualified healthcare professional for medication-related decisions.

## 13. License

No open-source license has been specified yet. Add a suitable license file before distributing the project under an open-source license.
