"""
Design System and Theme Configuration
Based on comprehensive UI/UX specification for ITC Infotech AI Resume Screener
"""

# ============================================================================
# COLOR PALETTE
# ============================================================================

class Colors:
    """Color palette following enterprise design standards"""

    # Primary Colors
    PRIMARY_BLUE = "#0066CC"
    PRIMARY_DARK = "#003D7A"
    ACCENT_PURPLE = "#7C3AED"
    ACCENT_TEAL = "#0891B2"

    # Neutral Colors
    BACKGROUND_MAIN = "#F8FAFC"
    BACKGROUND_CARD = "#FFFFFF"
    TEXT_PRIMARY = "#0F172A"
    TEXT_SECONDARY = "#64748B"
    TEXT_MUTED = "#94A3B8"

    # Status Colors
    SUCCESS_GREEN = "#10B981"
    WARNING_AMBER = "#F59E0B"
    ERROR_RED = "#EF4444"
    INFO_BLUE = "#3B82F6"

    # Border & Divider
    BORDER_LIGHT = "#E2E8F0"
    BORDER_MEDIUM = "#CBD5E1"

    # Match Score Colors
    SCORE_EXCELLENT = SUCCESS_GREEN  # 90-100%
    SCORE_GOOD = INFO_BLUE           # 75-89%
    SCORE_MODERATE = WARNING_AMBER   # 60-74%
    SCORE_LOW = "#9CA3AF"            # Below 60%


# ============================================================================
# TYPOGRAPHY
# ============================================================================

class Typography:
    """Typography scale and font families"""

    # Font Families
    FONT_PRIMARY = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif"
    FONT_MONO = "'JetBrains Mono', 'Fira Code', monospace"

    # Font Sizes (rem)
    TEXT_XS = "0.75rem"      # 12px
    TEXT_SM = "0.875rem"     # 14px
    TEXT_BASE = "1rem"       # 16px
    TEXT_LG = "1.125rem"     # 18px
    TEXT_XL = "1.25rem"      # 20px
    TEXT_2XL = "1.5rem"      # 24px
    TEXT_3XL = "2rem"        # 32px
    TEXT_4XL = "2.5rem"      # 40px

    # Font Weights
    WEIGHT_NORMAL = "400"
    WEIGHT_MEDIUM = "500"
    WEIGHT_SEMIBOLD = "600"
    WEIGHT_BOLD = "700"
    WEIGHT_EXTRABOLD = "800"


# ============================================================================
# SPACING SYSTEM
# ============================================================================

class Spacing:
    """Consistent spacing scale"""

    XS = "0.25rem"    # 4px
    SM = "0.5rem"     # 8px
    MD = "1rem"       # 16px
    LG = "1.5rem"     # 24px
    XL = "2rem"       # 32px
    XL2 = "3rem"      # 48px
    XL3 = "4rem"      # 64px


# ============================================================================
# BORDER RADIUS
# ============================================================================

class Radius:
    """Border radius scale"""

    SM = "0.375rem"   # 6px
    MD = "0.5rem"     # 8px
    LG = "0.75rem"    # 12px
    XL = "1rem"       # 16px
    FULL = "9999px"   # Circular


# ============================================================================
# SHADOWS
# ============================================================================

class Shadows:
    """Box shadow definitions"""

    SM = "0 1px 2px 0 rgba(0, 0, 0, 0.05)"
    MD = "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)"
    LG = "0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)"
    XL = "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)"
    HOVER = "0 20px 25px -5px rgba(0, 0, 0, 0.12), 0 10px 10px -5px rgba(0, 0, 0, 0.06)"


# ============================================================================
# COMPONENT STYLES
# ============================================================================

class ComponentStyles:
    """Reusable component style definitions"""

    @staticmethod
    def primary_button():
        """Primary button styling"""
        return f"""
            background: linear-gradient(135deg, {Colors.PRIMARY_BLUE} 0%, {Colors.PRIMARY_DARK} 100%);
            color: white;
            padding: 12px 24px;
            border-radius: {Radius.MD};
            border: none;
            font-weight: {Typography.WEIGHT_SEMIBOLD};
            font-size: {Typography.TEXT_SM};
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 6px rgba(0, 102, 204, 0.2);
        """

    @staticmethod
    def secondary_button():
        """Secondary button styling"""
        return f"""
            background: white;
            color: {Colors.PRIMARY_BLUE};
            border: 2px solid {Colors.PRIMARY_BLUE};
            padding: 12px 24px;
            border-radius: {Radius.MD};
            font-weight: {Typography.WEIGHT_SEMIBOLD};
            font-size: {Typography.TEXT_SM};
            cursor: pointer;
            transition: all 0.3s ease;
        """

    @staticmethod
    def card():
        """Card styling"""
        return f"""
            background: {Colors.BACKGROUND_CARD};
            border-radius: {Radius.LG};
            padding: {Spacing.XL};
            box-shadow: {Shadows.MD};
            border: 1px solid {Colors.BORDER_LIGHT};
            transition: all 0.3s ease;
        """

    @staticmethod
    def input_field():
        """Input field styling"""
        return f"""
            width: 100%;
            padding: 12px 16px;
            border: 1px solid {Colors.BORDER_LIGHT};
            border-radius: {Radius.MD};
            font-size: {Typography.TEXT_SM};
            transition: all 0.2s ease;
            background: {Colors.BACKGROUND_CARD};
        """

    @staticmethod
    def badge(color=Colors.PRIMARY_BLUE, bg_color="#EFF6FF"):
        """Badge/tag styling"""
        return f"""
            display: inline-block;
            padding: 4px 12px;
            border-radius: {Radius.FULL};
            font-size: {Typography.TEXT_XS};
            font-weight: {Typography.WEIGHT_SEMIBOLD};
            background: {bg_color};
            color: {color};
        """


# ============================================================================
# LAYOUT CONSTANTS
# ============================================================================

class Layout:
    """Layout dimensions and constants"""

    TOPBAR_HEIGHT = "64px"
    SIDEBAR_WIDTH = "240px"
    SIDEBAR_COLLAPSED_WIDTH = "80px"
    MAX_CONTENT_WIDTH = "1400px"

    # Breakpoints
    MOBILE_MAX = "640px"
    TABLET_MIN = "641px"
    TABLET_MAX = "1024px"
    DESKTOP_MIN = "1025px"


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def get_match_score_color(score: float) -> str:
    """Get color based on match score percentage"""
    if score >= 90:
        return Colors.SCORE_EXCELLENT
    elif score >= 75:
        return Colors.SCORE_GOOD
    elif score >= 60:
        return Colors.SCORE_MODERATE
    else:
        return Colors.SCORE_LOW


def get_match_score_label(score: float) -> str:
    """Get label based on match score percentage"""
    if score >= 90:
        return "Excellent Match"
    elif score >= 75:
        return "Good Match"
    elif score >= 60:
        return "Moderate Match"
    else:
        return "Low Match"


def format_percentage(value: float) -> str:
    """Format float as percentage"""
    return f"{int(value)}%"


# ============================================================================
# ANIMATIONS
# ============================================================================

class Animations:
    """CSS animation definitions"""

    TRANSITION_FAST = "all 0.2s ease"
    TRANSITION_MEDIUM = "all 0.3s ease"
    TRANSITION_SLOW = "all 0.5s ease"

    HOVER_LIFT = "transform: translateY(-4px);"
    HOVER_SCALE = "transform: scale(1.02);"

    @staticmethod
    def keyframes():
        """CSS keyframes for animations"""
        return """
        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        @keyframes shimmer {
            0% { background-position: -1000px 0; }
            100% { background-position: 1000px 0; }
        }

        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        """
