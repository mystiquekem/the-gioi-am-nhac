"""Helper functions for quiz-related database operations."""
from sqlalchemy.sql.expression import func
import random


def get_random_questions(db, limit=3):
    """Return a list of question dicts with shuffled choices.

    The import of the `question` model is done inside the function to
    avoid circular imports with `app`.
    """
    from app import question

    quest = db.session.execute(
        db.select(question).order_by(func.random()).limit(limit)
    ).scalars().all()

    data = []
    for row in quest:
        choice_pool = [row.CorrectA, row.DecoyB, row.DecoyC, row.DecoyD]
        random.shuffle(choice_pool)
        row_as_dict = {
            'ID': row.ID,
            'QName': row.QName,
            'ChoiceA': choice_pool[0],
            'ChoiceB': choice_pool[1],
            'ChoiceC': choice_pool[2],
            'ChoiceD': choice_pool[3]
        }
        data.append(row_as_dict)

    return data


def get_question_by_id(db, q_id):
    """Return the `question` model instance for the given ID or None."""
    from app import question

    return db.session.execute(
        db.select(question).where(question.ID == q_id)
    ).scalar_one_or_none()
