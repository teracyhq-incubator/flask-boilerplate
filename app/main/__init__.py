# -*- coding: utf-8 -*-

"""main blueprint"""

from flask import Blueprint

__all__ = ['main_bp']

main_bp = Blueprint('main', __name__)

from . import views
