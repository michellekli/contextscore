# contextscore Design Document

## 1. Introduction

### 1.1 Purpose
Score and rank textual items by how well they match desired inclusion criteria while suppressing those that match exclusion criteria.

### 1.2 Target Audience
People who need to filter and prioritize large collections of short texts against a flexible combination of keyword and semantic criteria.

### 1.3 Goals
- Keyword and semantic hybrid scoring: Combine hard keyword constraints with soft semantic similarity so users can express both precise and fuzzy criteria.
- Interactivity: Provide a visual interface that lets users upload data, trigger scoring, inspect ranked results, and export the ordered dataset without writing code.
- Transparent ranking: Surface intermediate score components so users understand *why* a given item received its final score.

## 2. Scope

### 2.1 In Scope
- Ingestion of tabular data containing a text column and a set of user-defined keyword and phrase criteria.
- Exact keyword matching (all-of / none-of) against the text.
- Semantic similarity scoring that measures how closely a text matches inclusion vs. exclusion phrases.
- Construction of a composite score that combines the keyword gate with the semantic similarity scores.
- Sorting of all items by composite match score, descending.
- An interactive interface to upload data, trigger scoring, browse ranked results, and download the scored dataset.
- On-demand summary export of the ranked list with basic score columns.
- On-demand detailed export of the full scored dataset with all intermediate score columns.

### 2.2 Out of Scope
- Real-time streaming or incremental scoring of live data.
- Modification or editing of original uploaded text content.
- Persistent server-side storage of uploaded data or scoring results.
- Multi-user collaboration or role-based access control.

## 3. Functional Requirements

### 3.1 Data Input
1. The system shall accept tabular data and allow the user to select the column containing the text to be scored.
2. The system shall allow the user to specify inclusion and exclusion keyword lists (exact-match) and inclusion and exclusion phrase lists (semantic-match).
3. The system shall allow the user to select an aggregation mode (`average` or `maximum`) independently for the inclusion phrase list and the exclusion phrase list.

### 3.2 Scoring
1. The system shall test each item against the exact-match inclusion and exclusion keywords. An item must satisfy all inclusion keywords (if provided) and no exclusion keywords (if provided) to pass this gate. If a keyword list is empty, the corresponding constraint is ignored (i.e., treated as automatically satisfied).
2. The system shall compute individual semantic similarity scores for each phrase in the inclusion phrase list.
3. The system shall compute individual semantic similarity scores for each phrase in the exclusion phrase list.
4. The system shall calculate the composite semantic inclusion score by applying the selected aggregation mode (`average` or `maximum`) to the individual inclusion phrase similarity scores. If the inclusion phrase list is empty, the composite inclusion score defaults to 1 (neutral).
5. The system shall calculate the composite semantic exclusion score by applying the selected aggregation mode (`average` or `maximum`) to the individual exclusion phrase similarity scores. If the exclusion phrase list is empty, the composite exclusion score defaults to 0 (no penalty).
6. The system shall compute a raw semantic score as the difference between the composite semantic inclusion score and the composite semantic exclusion score. This value is an internal intermediate and is not displayed in the output.
7. The exact-match gate acts as a pure boolean filter. If the gate fails, the final composite match score is 0. If the gate passes, the final composite match score is max(0, raw semantic score). The exact-match status does not contribute to the numerical calculation of the raw semantic score.

### 3.3 Ranking & Display
1. The system shall sort all scored items by composite match score in descending order. Items with tied composite scores may appear in any order.
2. The system shall present the ranked list showing at minimum the text and its composite match score.
3. The system shall support a detailed view that additionally displays the exact-match status, the aggregation modes, the composite semantic inclusion score, the composite semantic exclusion score, and the individual similarity score for each semantic-match phrase. The raw semantic score (§3.2.6) is an internal intermediate value and is not included in either view.

### 3.4 Export
1. The export format shall match the currently active view — summary export when the summary view is active, detailed export when the detailed view is active.
2. The summary export shall include only the text and its composite match score, one row per input item.
3. The detailed export shall include the text, composite match score, exact-match status, aggregation modes, composite semantic inclusion score, composite semantic exclusion score, and the individual similarity score for each semantic-match phrase in the inclusion and exclusion sets.

## 4. User Interface Layout & Flow

### 4.1 Primary Layout
The application shall present a data upload area, a scoring trigger, and a results panel that can toggle between summary and detailed views.

### 4.2 Workflow Steps

**Step 1: Upload**
User provides a data file and selects the column containing the text to be scored.

**Step 2: Configure**
User provides keyword and phrase lists for inclusion and exclusion criteria, and selects the aggregation mode (`average` or `maximum`) independently for the inclusion phrase list and the exclusion phrase list.

**Step 3: Score & Review**
User triggers the scoring process. The system displays the ranked results. User may toggle between the summary view (text + composite score) and the detailed view (all intermediate scores).

**Step 4: Export**
User requests a download of the scored dataset. The export format matches the active view (summary or detailed) selected during the Score & Review step.

## 5. Data Structures & Definitions

### 5.1 Input Schema (User Perspective)
- **Data file:** Tabular data, with the user specifying the text column.
- **Criteria:** Two categories of criteria — exact-match keywords and semantic-match phrases — each split into inclusion and exclusion lists.

### 5.2 Output Schema (System Perspective)
- **Scored Item:**
  - `text`: The original textual content.
  - `exact-match status`: Pass/fail indicator for the deterministic keyword gate.
  - `aggregation mode (inclusion)`: The aggregation method selected for the inclusion phrase list (`average` or `maximum`).
  - `aggregation mode (exclusion)`: The aggregation method selected for the exclusion phrase list (`average` or `maximum`).
  - `semantic inclusion scores`: Individual similarity scores for each inclusion phrase.
  - `composite semantic inclusion score`: Semantic similarity score aggregated from individual inclusion phrase scores using the selected inclusion aggregation mode.
  - `semantic exclusion scores`: Individual similarity scores for each exclusion phrase.
  - `composite semantic exclusion score`: Semantic similarity score aggregated from individual exclusion phrase scores using the selected exclusion aggregation mode.
  - `composite match score`: The final numeric score, derived from composite semantic inclusion and exclusion scores, clamped to a minimum of zero (and set to zero if exact-match gate fails).
- **Ranked Dataset:** An ordered collection of scored items sorted by composite match score descending.

### 5.3 File Output Definitions
- **Summary export:** Tabular file containing only the text and its composite match score. One row per input item.
- **Detailed export:** Tabular file containing text, composite match score, exact-match status, aggregation modes, composite semantic inclusion score, composite semantic exclusion score, and the individual similarity score for each semantic-match phrase. One row per input item.

## 6. Non-Functional Requirements

### 6.1 Performance
- Repeated invocations of the semantic model within a session should not incur redundant loading overhead.

### 6.2 Usability
- The user interface shall clearly distinguish between the summary and detailed views.

### 6.3 Reliability
- The system shall provide clear error messages for malformed or missing data input.
- The exported dataset must contain exactly the scored results produced by the most recent scoring run.

### 6.4 Security
- User-uploaded data shall not be persisted on the server after the session ends.
- Uploaded content shall be handled only in memory for the duration of the session.

## 7. Glossary

- **Exact-match keyword:** A string (single word or phrase) that must be literally present (or literally absent) in the text.
- **Semantic-match phrase:** A phrase whose meaning is compared against the text using similarity measurement, without requiring literal presence.
- **Inclusion criteria:** Conditions that a text should satisfy to be considered a match.
- **Exclusion criteria:** Conditions that a text should avoid to be considered a match.
- **Aggregation mode:** A user-selected method (`average` or `maximum`) for combining individual phrase similarity scores into a single composite score, configurable independently for inclusion and exclusion phrase lists.
- **Composite match score:** The final numeric score. It is calculated by taking the difference between composite semantic inclusion and composite semantic exclusion scores, clamping it to a minimum of zero, and setting it to zero if the item fails the exact-match gate.
- **Intermediate scores:** The similarity scores of each semantic-match phrase and the aggregate score components (composite semantic inclusion, composite semantic exclusion, aggregation modes) that contribute to the calculation of the composite match score. The raw semantic score (composite inclusion − composite exclusion) is computed as an internal intermediate but is not included in the detailed view or export.
