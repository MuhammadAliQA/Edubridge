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

