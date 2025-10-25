"""
UI Components Module
Professional, Modern, and Modular UI Components
"""

from .style import get_custom_css
from .header import render_header, render_metrics, render_features, render_section_header
from .sidebar import render_sidebar
from .info_box import (
    render_info_box,
    render_success_box,
    render_warning_box,
    render_danger_box,
    render_instructions,
    render_welcome_message
)

__all__ = [
    'get_custom_css',
    'render_header',
    'render_metrics',
    'render_features',
    'render_section_header',
    'render_sidebar',
    'render_info_box',
    'render_success_box',
    'render_warning_box',
    'render_danger_box',
    'render_instructions',
    'render_welcome_message'
]

__version__ = '1.0.0'
__author__ = 'Kelompok 2 - INF313'