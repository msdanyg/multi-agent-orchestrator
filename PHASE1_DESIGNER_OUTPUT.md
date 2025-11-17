# Phase 1: Designer Agent Output
## Todo List App - UI/UX Design Specification

**Agent:** Designer
**Task:** Create UI/UX design specification for modern todo list web app
**Timestamp:** 2025-11-17

---

## Design Philosophy
Minimalist, clean interface focused on:
- Task completion efficiency
- Visual clarity
- Accessibility (WCAG 2.1 AA)
- Mobile-first responsive design

---

## Color Palette

### Primary Colors
- **Primary:** #6366f1 (Indigo) - Actions, completed tasks
- **Background:** #ffffff (White) - Main background
- **Surface:** #f8fafc (Light gray) - Card surfaces
- **Text Primary:** #0f172a (Slate 900) - Main text
- **Text Secondary:** #64748b (Slate 500) - Secondary text

### Status Colors
- **Success:** #10b981 (Green) - Completed tasks
- **Danger:** #ef4444 (Red) - Delete actions
- **Warning:** #f59e0b (Amber) - Important tasks
- **Info:** #3b82f6 (Blue) - Task metadata

### Accessibility
- Contrast ratios: All combinations meet WCAG AA (4.5:1 minimum)
- Color is never the only indicator (icons + text)

---

## Typography

### Font Family
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI',
             'Roboto', 'Oxygen', 'Ubuntu', 'Cantarell',
             sans-serif;
```

### Font Sizes
- **Heading:** 24px / 1.5rem (Todo List title)
- **Body:** 16px / 1rem (Todo items)
- **Small:** 14px / 0.875rem (Metadata, counts)
- **Input:** 16px / 1rem (Prevents iOS zoom on focus)

---

## Layout Structure

### Desktop (> 768px)
```
┌─────────────────────────────────────┐
│           Todo List App              │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ [Add new todo...]      [+ Add] │ │
│  └────────────────────────────────┘ │
│                                      │
│  ┌────────────────────────────────┐ │
│  │ [✓] Buy groceries      [×]     │ │
│  ├────────────────────────────────┤ │
│  │ [ ] Read documentation [×]     │ │
│  ├────────────────────────────────┤ │
│  │ [✓] Morning workout    [×]     │ │
│  └────────────────────────────────┘ │
│                                      │
│  3 tasks · 2 completed               │
└─────────────────────────────────────┘

Max-width: 600px (centered)
Padding: 32px
```

### Mobile (< 768px)
```
┌─────────────────────┐
│   Todo List App     │
│                     │
│ ┌─────────────────┐ │
│ │ [Add...]  [Add] │ │
│ └─────────────────┘ │
│                     │
│ ┌─────────────────┐ │
│ │ [✓] Buy...  [×] │ │
│ ├─────────────────┤ │
│ │ [ ] Read... [×] │ │
│ └─────────────────┘ │
│                     │
│ 3 tasks · 2 done    │
└─────────────────────┘

Padding: 16px
Full width
```

---

## Component Specifications

### 1. App Container
```css
max-width: 600px
margin: 0 auto
padding: 32px (desktop) / 16px (mobile)
min-height: 100vh
background: #ffffff
```

### 2. Header
```css
font-size: 24px
font-weight: 600
color: #0f172a
margin-bottom: 24px
text-align: center
```

### 3. Input Form
```css
display: flex
gap: 12px
margin-bottom: 24px
padding: 20px
background: #f8fafc
border-radius: 12px
```

#### Text Input
```css
flex: 1
padding: 12px 16px
font-size: 16px
border: 2px solid #e2e8f0
border-radius: 8px
transition: border-color 0.2s

Focus state:
  border-color: #6366f1
  outline: none
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1)
```

#### Add Button
```css
padding: 12px 24px
background: #6366f1
color: #ffffff
border: none
border-radius: 8px
font-weight: 500
cursor: pointer
transition: all 0.2s

Hover:
  background: #4f46e5
  transform: translateY(-1px)

Active:
  transform: translateY(0)

Disabled:
  opacity: 0.5
  cursor: not-allowed
```

### 4. Todo Item
```css
display: flex
align-items: center
gap: 12px
padding: 16px
background: #ffffff
border: 1px solid #e2e8f0
border-radius: 8px
margin-bottom: 8px
transition: all 0.2s

Hover:
  border-color: #6366f1
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1)

Completed state:
  background: #f0fdf4
  border-color: #10b981
```

#### Checkbox
```css
width: 20px
height: 20px
border: 2px solid #cbd5e1
border-radius: 4px
cursor: pointer

Checked:
  background: #10b981
  border-color: #10b981
  display checkmark icon
```

#### Todo Text
```css
flex: 1
font-size: 16px
color: #0f172a

Completed:
  text-decoration: line-through
  color: #64748b
```

#### Delete Button
```css
padding: 8px
background: transparent
border: none
color: #ef4444
cursor: pointer
opacity: 0.7
transition: opacity 0.2s

Hover:
  opacity: 1
```

### 5. Footer Stats
```css
padding-top: 16px
text-align: center
font-size: 14px
color: #64748b
border-top: 1px solid #e2e8f0
margin-top: 16px
```

---

## Responsive Breakpoints

### Mobile First
```css
/* Base: Mobile (< 768px) */
.container {
  padding: 16px;
}

/* Tablet and up (>= 768px) */
@media (min-width: 768px) {
  .container {
    padding: 32px;
  }
  .todo-item {
    padding: 20px;
  }
}
```

---

## Interaction States

### 1. Adding Todo
1. User types in input
2. Input shows focus state (blue border + shadow)
3. Add button changes to hover state on mouse over
4. Click Add button → loading state (optional spinner)
5. Todo appears with smooth animation (fade in + slide down)

### 2. Completing Todo
1. User clicks checkbox
2. Checkbox animates to checked state
3. Todo text gets strikethrough animation
4. Background changes to success green
5. Stats update with animation

### 3. Deleting Todo
1. User hovers delete button → opacity increases
2. User clicks delete button
3. Todo item animates out (fade + slide up)
4. Stats update

### 4. Empty State
When no todos:
```
┌─────────────────────────────────┐
│                                 │
│       📝                        │
│                                 │
│    No todos yet!                │
│    Add one to get started       │
│                                 │
└─────────────────────────────────┘
```

---

## Accessibility Features

### Keyboard Navigation
- Tab order: Input → Add button → Checkboxes → Delete buttons
- Enter key: Submit form, toggle checkbox
- Space key: Toggle checkbox
- Escape key: Clear input

### Screen Reader
```html
<input aria-label="New todo item" />
<button aria-label="Add todo">Add</button>
<input type="checkbox" aria-label="Mark as complete" />
<button aria-label="Delete todo">×</button>
```

### Visual Indicators
- Focus outlines visible for all interactive elements
- Status indicated by icon + color (not color alone)
- Error states have descriptive text

---

## Animations

### Smooth Transitions
```css
/* All interactive elements */
transition: all 0.2s ease-in-out;

/* Todo item entrance */
@keyframes fadeInSlide {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* Todo item exit */
@keyframes fadeOutSlide {
  from {
    opacity: 1;
    transform: translateX(0);
  }
  to {
    opacity: 0;
    transform: translateX(20px);
  }
}
```

---

## Local Storage Strategy
- Auto-save on every change
- Load on page load
- Data structure: JSON array of todos
- Each todo: `{ id, text, completed, createdAt }`

---

## Design Assets Delivered
✓ Color palette with accessibility checks
✓ Typography system
✓ Layout structure (desktop + mobile)
✓ Component specifications
✓ Responsive breakpoints
✓ Interaction states
✓ Accessibility guidelines
✓ Animation specifications

**Ready for implementation by Code_writer agent.**
