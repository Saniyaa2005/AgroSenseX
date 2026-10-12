
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "feedback.db"


def initialize_feedback_db():
    """Create the feedback table if it does not already exist."""
    with sqlite3.connect(DB_PATH) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS prediction_feedback (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                crop TEXT NOT NULL,
                predicted_disease TEXT NOT NULL,
                confidence REAL,
                feedback TEXT NOT NULL
                    CHECK (feedback IN ('Correct', 'Incorrect', 'Unsure')),
                comment TEXT,
                language TEXT NOT NULL DEFAULT 'en'
            )
            """
        )
        connection.commit()


def save_feedback(
    crop,
    predicted_disease,
    confidence,
    feedback,
    comment="",
    language="en",
):
    """Save feedback for a prediction and return its database ID."""
    allowed_feedback = {"Correct", "Incorrect", "Unsure"}

    if feedback not in allowed_feedback:
        raise ValueError("Feedback must be Correct, Incorrect, or Unsure.")

    if not crop or not predicted_disease:
        raise ValueError("Crop and predicted disease are required.")

    if confidence is not None:
        confidence = float(confidence)
        if not 0 <= confidence <= 1:
            raise ValueError("Confidence must be between 0 and 1.")

    timestamp = datetime.now(timezone.utc).isoformat()

    with sqlite3.connect(DB_PATH) as connection:
        cursor = connection.execute(
            """
            INSERT INTO prediction_feedback (
                timestamp, crop, predicted_disease, confidence,
                feedback, comment, language
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                timestamp,
                str(crop),
                str(predicted_disease),
                confidence,
                feedback,
                str(comment).strip(),
                str(language),
            ),
        )
        connection.commit()
        return cursor.lastrowid


if __name__ == "__main__":
    initialize_feedback_db()
    print("Feedback database initialized successfully.")
    print(f"Database location: {DB_PATH}")