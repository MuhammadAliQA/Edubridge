from django import template

register = template.Library()


@register.filter
def has_mentor_profile(user) -> bool:
    if not getattr(user, "is_authenticated", False):
        return False
    try:
        getattr(user, "mentor_profile")
        return True
    except Exception:
        return False


@register.filter
def has_student_profile(user) -> bool:
    if not getattr(user, "is_authenticated", False):
        return False
    try:
        getattr(user, "student_profile")
        return True
    except Exception:
        return False


@register.filter
def score_label(mentor) -> str:
    yonalish = getattr(mentor, "yonalish", "")
    return "Band" if yonalish == "ielts" else "Ball"


@register.filter
def score_value(mentor) -> str:
    yonalish = getattr(mentor, "yonalish", "")
    value = getattr(mentor, "ball", None)
    if value is None:
        return ""
    try:
        value_f = float(value)
    except Exception:
        return str(value)

    if yonalish == "ielts":
        if not (0 < value_f <= 9):
            return ""
        return f"{value_f:.1f}".rstrip("0").rstrip(".")

    if yonalish == "sat":
        if not (400 <= value_f <= 1600):
            return ""
        return str(int(round(value_f)))

    return ""
