# contextscore Roadmap

Phased implementation plan with each phase delivering a working, tested slice of the application.

> **Testing Strategy:** Every step below follows a concurrent testing approach. Core logic (data processing, scoring, aggregation) will be implemented with comprehensive `pytest` suites to ensure accuracy of the composite score calculations. Frontend components will be verified via functional integration tests using `streamlit.testing.v1` to ensure data flows correctly from user input to the ranked results display.

---

## Phase 1: Scoring Engine (Backend)

| Step | Task | Depends On |
| :--- | :--- | :--- |
| 1.1 | Implement exact-match keyword gate logic | — |
| 1.2 | Implement semantic phrase similarity computation | — |
| 1.3 | Implement composite score aggregation (`avg`/`max`) | 1.1, 1.2 |

**Definition of done:**
- All backend tests pass.
- Keyword gate correctly filters/passes items.
- Composite semantic scores (inclusion/exclusion) are accurately calculated using configured aggregation modes.
- Composite match score correctly clamps to zero.

---

## Phase 2: UI & Interaction

| Step | Task | Depends On |
| :--- | :--- | :--- |
| 2.1 | Build data upload area & text column selector | Phase 1 |
| 2.2 | Build criteria configuration form (keywords/phrases) | 2.1 |
| 2.3 | Implement aggregation mode selection UI | 2.2 |
| 2.4 | Implement scoring execution trigger | 2.3 |
| 2.5 | Build ranked results panel (Summary View) | 2.4 |
| 2.6 | Implement detailed view (intermediate scores table) | 2.5 |

**Definition of done:**
- All tests pass.
- User can successfully upload tabular data.
- User can input multiple inclusion/exclusion keywords and phrases.
- Independent aggregation modes (`avg` vs `max`) are selectable for inclusion/exclusion lists.
- Scoring correctly triggers and updates the interface with ranked results.
- Users can toggle between summary view (text + composite score) and the detailed view (table showing intermediate score components — exact-match status, aggregation modes, composite semantic scores, individual phrase similarity scores).

---

## Phase 3: Export & Finalization

| Step | Task | Depends On |
| :--- | :--- | :--- |
| 3.1 | Implement export that matches the currently active view (summary or detailed) | Phase 2 |
| 3.2 | Validate exported file correctness | 3.1 |

**Definition of done:**
- All tests pass.
- Export output matches the currently active view (summary export when summary is active, detailed export when detailed is active).
- UI reliably clears session data upon reset (ensuring no persistent storage).
