---
name: TravelMate
colors:
  surface: '#faf9fe'
  surface-dim: '#dad9df'
  surface-bright: '#faf9fe'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f3f8'
  surface-container: '#eeedf3'
  surface-container-high: '#e9e7ed'
  surface-container-highest: '#e3e2e7'
  on-surface: '#1a1b1f'
  on-surface-variant: '#414755'
  inverse-surface: '#2f3034'
  inverse-on-surface: '#f1f0f5'
  outline: '#717786'
  outline-variant: '#c1c6d7'
  surface-tint: '#005bc1'
  primary: '#0058bc'
  on-primary: '#ffffff'
  primary-container: '#0070eb'
  on-primary-container: '#fefcff'
  inverse-primary: '#adc6ff'
  secondary: '#006e28'
  on-secondary: '#ffffff'
  secondary-container: '#6ffb85'
  on-secondary-container: '#00732a'
  tertiary: '#9e3d00'
  on-tertiary: '#ffffff'
  tertiary-container: '#c64f00'
  on-tertiary-container: '#fffbff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a41'
  on-primary-fixed-variant: '#004493'
  secondary-fixed: '#72fe88'
  secondary-fixed-dim: '#53e16f'
  on-secondary-fixed: '#002107'
  on-secondary-fixed-variant: '#00531c'
  tertiary-fixed: '#ffdbcc'
  tertiary-fixed-dim: '#ffb595'
  on-tertiary-fixed: '#351000'
  on-tertiary-fixed-variant: '#7c2e00'
  background: '#faf9fe'
  on-background: '#1a1b1f'
  surface-variant: '#e3e2e7'
  surface-background: '#FFFFFF'
  surface-canvas: '#F2F2F7'
  status-error: '#FF3B30'
  status-warning: '#FF9500'
  border-subtle: '#E5E5EA'
typography:
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  code-sm:
    fontFamily: jetbrainsMono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '700'
    lineHeight: 28px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  margin-mobile: 1rem
  margin-desktop: 2rem
  gutter: 1rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 1.5rem
---

## Brand & Style

The design system embodies a **Modern, Trustworthy, and Tech-savvy** persona, functioning as a high-end digital concierge for the modern traveler. The brand personality is grounded in reliability and precision, using "observable AI" to build user trust. 

The visual style is **Corporate / Modern**, taking cues from Streamlit's functional clarity but refined for a premium mobile experience. It prioritizes information density and readability, ensuring that complex itineraries and multi-step tool executions are digestible. The aesthetic is clean and professional, using high-quality typography and a disciplined color application to feel like a sophisticated travel assistant rather than a generic chatbot.

**Key Brand Pillars:**
- **Transparency:** Showing the "thinking" process through structured tool-execution panels.
- **Efficiency:** A utility-first layout that minimizes friction during travel planning.
- **Reliability:** A robust, grounded visual language that implies technical competence.

## Colors

The color palette is anchored by **Travel Blue** (#007AFF), signifying technology and professional service. **Nature Green** (#34C759) is used as a secondary accent to denote success, health, and positive outcomes (such as successful API connections or finalized bookings).

The system uses a neutral-heavy background strategy to ensure maximum legibility for long-form Markdown itineraries. 
- **Primary:** Used for actionable elements, active states, and primary brand moments.
- **Secondary:** Used for "Success" states and travel-positive highlights (e.g., "Eco-friendly" tags).
- **Surface Strategy:** Use white for primary cards and chat bubbles, with a subtle off-white (`#F2F2F7`) for the application background to create soft depth.
- **Borders:** Use a very light gray (`#E5E5EA`) for tool execution containers and dividers to maintain a clean, structured look without adding visual noise.

## Typography

This design system utilizes **Inter** across all primary UI roles to ensure maximum readability and a clean, systematic feel. **JetBrains Mono** is introduced specifically for "Tool Execution" logs and technical data to reinforce the "Tech-savvy" brand pillar.

**Usage Guidelines:**
- **Headlines:** Use Bold weights for itinerary sections (e.g., 【Daily Plan】).
- **Body:** Use the standard weight for chat interactions. Itinerary content should use a slightly increased line height (1.5x) to aid long-form reading on mobile.
- **Labels:** Use Semibold uppercase for metadata like "TOOL CALLED" or "ARGUMENTS" to distinguish system logs from human conversation.

## Layout & Spacing

The layout employs a **Fluid Grid** model optimized for mobile-first interactions. It relies on a vertical stack rhythm to organize the flow of the travel planning conversation.

- **Mobile:** 16px (1rem) side margins with full-width chat bubbles.
- **Desktop:** The layout centers at a maximum width of 800px for the chat stream, with a 280px fixed sidebar for trip configuration and API status.
- **Spacing Rhythm:** Use 16px (stack-md) as the default vertical gap between chat bubbles. Larger 24px (stack-lg) gaps should separate distinct days in a generated itinerary.
- **Tool Panels:** Indent tool execution cards by 12px from the left and right within the chat flow to signal they are "internal" processes.

## Elevation & Depth

Hierarchy is achieved through **Tonal Layers** and **Low-contrast outlines** rather than heavy shadows, keeping the UI feeling fast and light.

- **Base Layer:** The "Canvas" (`#F2F2F7`) acts as the foundation.
- **Surface Layer:** White surfaces (`#FFFFFF`) are used for chat bubbles and itinerary containers. These use a 1px border of `#E5E5EA` to define boundaries.
- **Interactive Depth:** Subtle, diffused shadows (0px 2px 4px rgba(0,0,0,0.05)) are reserved exclusively for the primary chat input area and floating action buttons to suggest they sit above the content.
- **Sidebar:** Uses a slightly darker gray or a distinct tonal shift from the canvas to separate "Configuration" from "Interaction."

## Shapes

The design system uses a **Rounded** (Level 2) shape language to balance professional structure with an approachable "concierge" feel.

- **Buttons & Inputs:** 0.5rem (8px) radius.
- **Chat Bubbles:** 1rem (16px) radius for the outer corners, with a sharper 4px radius on the corner pointing to the sender.
- **Itinerary Cards:** 1rem (16px) radius for large structured sections to create a soft, contained feeling.

## Components

### Chat Bubbles
- **User:** Primary Blue background with White text. Aligned to the right.
- **Agent:** White background with a subtle Border (`#E5E5EA`). Aligned to the left.
- **Radius:** Asymmetric rounding to indicate directional flow.

### Tool Execution Cards
- **Visuals:** Collapsible "Accordion" style panels. Use a light gray background (`#F8F9FA`).
- **Header:** Includes a mono-spaced label (e.g., `google_maps_api`) and a small status indicator (Green dot for success).
- **Body:** Uses `code-sm` typography for JSON arguments and raw results.

### Sidebar Navigation
- **Structure:** Contains high-level metadata: Trip Name, Travel Dates, and API Status indicators.
- **Status Indicators:** 8px circles. Green (`#34C759`) for connected, Red (`#FF3B30`) for error/disconnected.

### Markdown Containers (Itineraries)
- **Styling:** Vertical dividers (2px thick, Nature Green) to separate "Day 1", "Day 2", etc.
- **Weather Icons:** Use standardized glyphs for weather summaries.
- **Checkboxes:** Styled with a 0.25rem radius for interactive packing lists or "To-do" itinerary items.

### Primary Buttons
- **Style:** Full-width on mobile, 0.5rem radius, Travel Blue background.
- **Text:** Semibold Inter, White.