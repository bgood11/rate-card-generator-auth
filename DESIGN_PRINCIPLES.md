# Stax Staff Portal - Design Principles & Brand Guidelines

**Last Updated**: 11/06/2025  
**Version**: 1.0.0  
**Based on**: Shermin Stax Branding Guidelines Dec 2023

## 🎨 Core Design Principles

### 1. **Professional & Trustworthy**
The Stax brand represents financial expertise and reliability. Every design decision should reinforce trust and professionalism.

### 2. **Clean & Minimalist**
Embrace whitespace and avoid clutter. The interface should feel spacious and easy to navigate, reflecting the clarity we bring to financial solutions.

### 3. **Modern & Forward-Thinking**
While maintaining professionalism, the design should feel contemporary and innovative, positioning Stax as a leader in financial services.

### 4. **Accessible & Inclusive**
Ensure all users can effectively use the platform, regardless of ability. Follow WCAG 2.1 AA standards.

## 🎨 Color Palette

### Primary Colors

```css
/* Core Brand Colors */
--stax-teal: #477085;        /* Primary - Deep blue-gray for headers and primary actions */
--stax-pink: #d884b6;        /* Secondary - Soft pink/purple for accents */
--stax-light-blue: #2ab7e3;  /* Tertiary - Bright cyan for highlights and CTAs */
--stax-gray: #9d9c9c;        /* Neutral - For body text and secondary elements */
```

### Extended Palette

```css
/* Backgrounds */
--bg-primary: #ffffff;       /* White - Main content areas */
--bg-secondary: #f9fafb;     /* Gray-50 - Page backgrounds */
--bg-tertiary: #f3f4f6;      /* Gray-100 - Subtle contrast */

/* Text Colors */
--text-primary: #477085;     /* Stax teal - Headers and important text */
--text-secondary: #9d9c9c;   /* Stax gray - Body text */
--text-muted: #6b7280;       /* Gray-500 - De-emphasized text */
--text-inverse: #ffffff;     /* White - Text on dark backgrounds */

/* Semantic Colors */
--success: #10b981;          /* Green - Success states */
--warning: #f59e0b;          /* Amber - Warning states */
--error: #ef4444;            /* Red - Error states */
--info: #3b82f6;             /* Blue - Informational states */

/* Gradients */
--gradient-primary: linear-gradient(to right, #477085, #2ab7e3);
--gradient-secondary: linear-gradient(to right, #d884b6, #2ab7e3);
--gradient-subtle: linear-gradient(to bottom right, #2ab7e3/10, transparent);
```

### Color Usage Guidelines

1. **Teal (#477085)** - Primary brand color
   - Main headers and titles
   - Primary buttons (solid fill)
   - Navigation elements
   - Form labels

2. **Pink (#d884b6)** - Secondary accent
   - Special features or premium tools
   - Decorative elements
   - Secondary CTAs
   - Hover states for special actions

3. **Light Blue (#2ab7e3)** - Interactive accent
   - Links and clickable elements
   - Hover states
   - Active states
   - Progress indicators

4. **Gray (#9d9c9c)** - Neutral text
   - Body copy
   - Descriptions
   - Metadata
   - Disabled states

## 📝 Typography

### Font Stack

```css
/* Primary Font Family */
--font-heading: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--font-body: Inter, system-ui, -apple-system, "Segoe UI", Roboto, sans-serif;
--font-mono: "SF Mono", Monaco, Consolas, "Courier New", monospace;
```

### Type Scale

```css
/* Headings */
--text-4xl: 2.25rem;    /* 36px - Page titles */
--text-3xl: 1.875rem;   /* 30px - Major sections */
--text-2xl: 1.5rem;     /* 24px - Section headers */
--text-xl: 1.25rem;     /* 20px - Subsections */
--text-lg: 1.125rem;    /* 18px - Large body text */

/* Body */
--text-base: 1rem;      /* 16px - Default body text */
--text-sm: 0.875rem;    /* 14px - Secondary text */
--text-xs: 0.75rem;     /* 12px - Captions and labels */

/* Line Heights */
--leading-tight: 1.25;
--leading-normal: 1.5;
--leading-relaxed: 1.75;

/* Font Weights */
--font-normal: 400;     /* Body text */
--font-medium: 500;     /* Emphasis */
--font-semibold: 600;   /* Buttons and links */
--font-bold: 700;       /* Headers */
```

### Typography Guidelines

1. **Headers** 
   - Use `system-ui` for optimal native rendering
   - Bold weight (700) for emphasis
   - Stax teal color (#477085)
   - Adequate spacing above and below

2. **Body Text**
   - Inter font for improved readability
   - Regular weight (400)
   - Gray color (#9d9c9c)
   - 1.5 line height for comfort

3. **Interactive Elements**
   - Semibold weight (600)
   - Color change on hover
   - Clear focus states

## 🎯 Component Design Patterns

### Cards

```css
.card {
  background: white;
  border: none;
  border-radius: 1rem;      /* rounded-2xl */
  padding: 2rem;            /* p-8 */
  box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1);  /* shadow-xl */
  transition: all 0.3s ease;
}

.card:hover {
  box-shadow: 0 25px 50px -12px rgb(0 0 0 / 0.25); /* shadow-2xl */
  transform: translateY(-2px);
}
```

### Buttons

#### Primary Button
```css
.btn-primary {
  background: linear-gradient(to right, #477085, #2ab7e3);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.btn-primary:hover {
  background: linear-gradient(to right, #2ab7e3, #477085);
}
```

#### Secondary Button
```css
.btn-secondary {
  background: white;
  color: #477085;
  border: 2px solid #e5e7eb;
  padding: 0.75rem 1.5rem;
  border-radius: 0.75rem;
  font-weight: 600;
}
```

### Form Elements

```css
.input {
  height: 3.5rem;           /* h-14 */
  padding: 0 1rem 0 3rem;   /* Icon space */
  border: 2px solid #f3f4f6;
  border-radius: 0.75rem;   /* rounded-xl */
  font-size: 1rem;
  transition: all 0.2s ease;
}

.input:focus {
  border-color: #2ab7e3;
  outline: none;
  box-shadow: 0 0 0 3px rgb(42 183 227 / 0.1);
}
```

## 📐 Layout Principles

### Spacing System

Use a consistent 8px grid system:
- `4px` - Micro spacing (gap-1)
- `8px` - Small spacing (gap-2)
- `16px` - Default spacing (gap-4)
- `24px` - Medium spacing (gap-6)
- `32px` - Large spacing (gap-8)
- `48px` - Extra large spacing (gap-12)
- `64px` - Section spacing (gap-16)

### Container Widths

```css
--max-w-7xl: 80rem;     /* 1280px - Main content */
--max-w-6xl: 72rem;     /* 1152px - Wide content */
--max-w-4xl: 56rem;     /* 896px - Reading width */
--max-w-2xl: 42rem;     /* 672px - Narrow content */
--max-w-md: 28rem;      /* 448px - Forms and modals */
```

### Grid System

- **Dashboard**: 4-column grid on desktop, 1-column on mobile
- **Tools Grid**: 2-3 columns on desktop, 1-column on mobile
- **Forms**: Single column, max-width constrained

## 🎭 Visual Elements

### Logo Usage

1. **Primary Logo**: Full color Stax logo
   - Minimum size: 32px height
   - Clear space: 0.5x logo height on all sides
   - Always on white or light backgrounds

2. **Logo Placement**
   - Top-left corner in headers
   - Centered on login/auth pages
   - With adequate breathing room

### Icons

- **Icon Library**: Lucide React
- **Size Standards**: 
  - Small: 16px (w-4 h-4)
  - Default: 20px (w-5 h-5)
  - Large: 24px (w-6 h-6)
  - XL: 32px (w-8 h-8)
- **Style**: Outline icons for consistency
- **Color**: Match text color or use accent colors for emphasis

### Decorative Elements

1. **Gradient Corners**
   ```css
   .decorative-corner {
     background: linear-gradient(to bottom right, #2ab7e3/10, transparent);
     border-radius: 0 0 0 1.5rem;
   }
   ```

2. **Status Indicators**
   - Green pulse for "operational"
   - Amber for warnings
   - Red for errors

## 🎬 Animation & Interaction

### Transition Guidelines

```css
/* Standard transition */
transition: all 0.3s ease;

/* Quick transitions (hover states) */
transition: all 0.2s ease;

/* Slow transitions (page changes) */
transition: all 0.5s ease;
```

### Hover Effects

1. **Buttons**: Color/gradient reversal
2. **Cards**: Elevation increase + slight upward movement
3. **Links**: Color change to light blue
4. **Icons**: Scale to 110%

### Loading States

- Use skeleton screens for content loading
- Spinner for actions (with Loader2 icon)
- Progress bars for multi-step processes

## 📱 Responsive Design

### Breakpoints

```css
--sm: 640px;   /* Mobile landscape */
--md: 768px;   /* Tablet */
--lg: 1024px;  /* Desktop */
--xl: 1280px;  /* Wide desktop */
--2xl: 1536px; /* Ultra-wide */
```

### Mobile-First Approach

1. Design for mobile screens first
2. Enhance for larger screens
3. Ensure touch targets are at least 44x44px
4. Simplify navigation for mobile

## ♿ Accessibility Guidelines

1. **Color Contrast**
   - Normal text: 4.5:1 minimum
   - Large text: 3:1 minimum
   - Use tools to verify contrast ratios

2. **Focus States**
   - Clear, visible focus indicators
   - Logical tab order
   - Skip links where appropriate

3. **Screen Readers**
   - Semantic HTML structure
   - Proper ARIA labels
   - Alt text for images
   - Descriptive link text

4. **Keyboard Navigation**
   - All interactive elements keyboard accessible
   - Escape key closes modals
   - Enter/Space activates buttons

## 📋 Implementation Checklist

When building new features, ensure:

- [ ] Colors match brand palette
- [ ] Typography follows scale system
- [ ] Spacing uses 8px grid
- [ ] Components follow established patterns
- [ ] Hover/focus states implemented
- [ ] Mobile responsive
- [ ] Accessibility standards met
- [ ] Animations are smooth and purposeful
- [ ] Design feels cohesive with existing platform

## 🔄 Design Evolution

The design system should evolve based on:
1. User feedback and usability testing
2. New brand guidelines from Stax
3. Technical capabilities and constraints
4. Industry best practices

Regular design reviews should be conducted quarterly to ensure consistency and identify areas for improvement.

---

**Document Version**: 1.0.0  
**Last Review**: 11/06/2025  
**Next Review**: Q2 2025

This document serves as the single source of truth for design decisions in the Stax Staff Portal. All new features should adhere to these principles while allowing for creative solutions within the established framework.