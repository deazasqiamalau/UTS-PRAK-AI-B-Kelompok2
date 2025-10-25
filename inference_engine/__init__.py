"""
Inference Engine Module
Forward Chaining and Certainty Factor implementations
"""

from .forward_chaining import ForwardChaining
from .certainty_factor import CertaintyFactor, CFCalculator

__version__ = '1.0.0'
__all__ = ['ForwardChaining', 'CertaintyFactor', 'CFCalculator']