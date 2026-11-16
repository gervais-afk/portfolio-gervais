"""Compatibility entry point. CV content lives exclusively in profile.json."""
from build_cv import build


def generate_exact_user_1page_cv_fr():
    build(('fr',))


if __name__ == '__main__':
    generate_exact_user_1page_cv_fr()
