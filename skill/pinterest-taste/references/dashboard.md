# dashboard: UI/UX patterns
> Distilled from 60 Pinterest pins. Updated 2026-11-14. Patterns, not copies: no single pin is reproduced.

Batch note: 60 pins read, 0 skipped. Two pins repeat another image (same shot under different ids), so independent evidence is ~58 shots.

## Directions

### Soft Bento Light
- **Use when:** SaaS, finance, HR, health, education and e-commerce admin for general business users. Friendly, calm, "premium but approachable".
- **Signature:** (1) White rounded cards on a pale tinted canvas, arranged as a bento grid of mixed sizes. (2) One saturated accent (purple, green or orange) carries all emphasis: active nav, primary button, selected chart bar. (3) A "Welcome back, <name>" greeting above a KPI row.
- **Palette (approx.):** bg `#F3F4F8` (or tinted `#EEF6F1`), surface `#FFFFFF`, text `#14161C`, muted text `#7A8190`, accent `#6C5CE7` (alt `#1F9D61` / `#F2652B`), positive chip bg `#DDF7E6` with text `#1E8E4E`, negative chip `#FDE3E1` with text `#D43B32`.
- **Type:** Geometric or neo-grotesque sans: Plus Jakarta Sans, Manrope, DM Sans, Inter. Greeting/page title 28–36px/600; KPI value 24–32px/600–700; card title 14–16px/600; labels 11–12px/400–500 muted; table text 12–13px.
- **Layout:** Left icon rail (56–72px) or text sidebar (220–260px) plus 12-col content. Top bar: search left, bell/avatar right, often a pill tab nav centred. KPI row of 3–4 cards, then a 2:1 chart row, then table or list. Card radius 16–24px, gap 16–20px, padding 16–24px. Soft shadow or none, no heavy borders.
- **Seen in:** https://www.pinterest.com/pin/1093389615817674723/ , https://www.pinterest.com/pin/1096696946788891413/ , https://www.pinterest.com/pin/1101693127632695749/ , https://www.pinterest.com/pin/1114781714047326787/ , https://www.pinterest.com/pin/1126533294325227941/ , https://www.pinterest.com/pin/1086000897680509464/

### Frosted Glass Gradient
- **Use when:** AI tools, CRM, HR, smart-home and showcase or portfolio pieces where mood outweighs density.
- **Signature:** (1) Blurry multi-colour gradient or photo behind translucent panels. (2) Pill-shaped nav and buttons, near-black pill for the active state. (3) Pastel or lime-yellow highlight blocks inside otherwise grey-white glass.
- **Palette (approx.):** bg gradient `#CFE3F5` → `#F7D9E8` → `#FBE9C9`, glass surface `rgba(255,255,255,0.55)` (border `rgba(255,255,255,0.7)`), text `#1B1D22`, active pill `#111111`, accent lime `#D8F35B` (or mint `#B9F0D0`), secondary periwinkle `#B8B4F2`.
- **Type:** Grotesque sans with wide, open forms: Inter, Plus Jakarta Sans, Figtree. Greeting 28–40px/500; stat numerals 28–48px/500; labels 11–13px/400.
- **Layout:** Single rounded device frame (radius 24–32px) on a decorative backdrop. Panels radius 16–24px, 12–16px gaps. Medium density, 4–6 modules, often a photo or illustration card for warmth.
- **Seen in:** https://www.pinterest.com/pin/1040120476466587799/ , https://www.pinterest.com/pin/1036039089283963161/ , https://www.pinterest.com/pin/1050253575617477537/ , https://www.pinterest.com/pin/1094515515720305975/ , https://www.pinterest.com/pin/1116189088932975328/ , https://www.pinterest.com/pin/1083819466612178450/

### Deep Green / Dark Contrast
- **Use when:** Health, sustainability, fintech or creator tools that want authority, or dark-mode products.
- **Signature:** (1) A dark sidebar or dark panel against light cards, or a fully dark canvas. (2) A neon lime or bright green accent on charts and CTAs. (3) Bars or lines in graded greens, with one highlighted data point.
- **Palette (approx.):** bg `#F1F3F0` (dark variant `#0E0F11`), dark surface `#12301F` (or `#1A1B1E`), light card `#FFFFFF`, text `#0F1A14`, accent lime `#B6F23B`, accent green `#1F8A4C`, warm secondary `#F4B79A` or `#F2652B`.
- **Type:** Rounded or grotesque sans: Manrope, Inter, Outfit. Page title 24–32px/600; KPI 28–40px/600; nav 13–14px/500; muted 12px.
- **Layout:** Sidebar 72–240px in the dark colour. Content in a light rounded sheet (radius 20–28px). Right column for a calendar, appointments or secondary info. Medium-high density.
- **Seen in:** https://www.pinterest.com/pin/1087408272566703954/ , https://www.pinterest.com/pin/1092052609672174058/ , https://www.pinterest.com/pin/1116189088932975328/ , https://www.pinterest.com/pin/1113515076643761619/ , https://www.pinterest.com/pin/1040120476468426762/ , https://www.pinterest.com/pin/1027454102473727565/

### Dense Data Console
- **Use when:** Analytics, admin and ops tools for expert users who scan many metrics and tables daily.
- **Signature:** (1) Neutral white UI with 1px hairline borders instead of shadows. (2) Compact tables, small KPI strips, sortable columns, filter chips. (3) Specialised charts (treemap, heatmap, dot matrix, multi-donut) and mono or tabular numerals.
- **Palette (approx.):** bg `#F7F7F8`, surface `#FFFFFF`, border `#E6E7EB`, text `#111318`, muted `#6B7280`, accent `#2F6BFF` (or `#E8590C` / `#111111`), status green `#16A34A`, red `#DC2626`, amber `#F59E0B`.
- **Type:** Inter, Geist or similar neutral sans, with a mono (JetBrains Mono, IBM Plex Mono) for IDs and numbers. Page title 20–24px/600; KPI 20–28px/600; table 12–13px/400; header row 11–12px/500 muted.
- **Layout:** 220–260px sidebar with grouped sections, 12-col main, radius 8–12px, 12–16px gaps. Table row height 36–44px. Toolbar above table: search, filter, export, density.
- **Seen in:** https://www.pinterest.com/pin/1084241679077163100/ , https://www.pinterest.com/pin/1125618500638793162/ , https://www.pinterest.com/pin/1086282372631683597/ , https://www.pinterest.com/pin/1101693127631977729/ , https://www.pinterest.com/pin/1105844883527479561/ , https://www.pinterest.com/pin/1107322627162676625/

## Layout & structure
- Shell: left sidebar (icon rail 56–72px, or labelled 220–260px) + top bar + content. Seen in nearly all pins. Rail is used by lighter, consumer-feeling products; labelled sidebars by multi-module admin tools.
- Sidebar groups carry small uppercase section labels (Menu, General, Platform), count badges on items (2, 4, 10) and an upsell or help card pinned at the bottom.
- Page opening: greeting ("Welcome back, <name>") or plain page title, plus a date-range selector and a primary action (Add / Export / New) top right.
- KPI row first: 3–4 cards (label, large value, delta chip, "vs last month"), then one or two hero charts, then table or list. Order matches the reading priority: status, trend, detail.
- Bento grid: cards of 1×, 2× and tall spans; the right column (~25–30%) is a secondary rail with calendar, activity log, chat history, or detail panel.
- Widths seen: 12-col, 1280–1440px canvas. Gaps are consistent at 12, 16 or 20px. Card padding 16–24px.
- Detail pattern: a master list on the left and a selected-record panel on the right (property, patient, invoice, shipment tracking).
- Multi-screen kits (HR, task management) show the same shell repeated across dashboard, calendar, list, form and inbox views.

## Typography
- One sans family per product. Geometric (Plus Jakarta Sans, Manrope, DM Sans, Outfit) for friendly products; Inter or Geist for tool-like ones. Free Google options cover all.
- KPI numerals are the loudest element: 24–40px, weight 600–700, tight tracking (-0.01em). Often the cents or unit are set smaller and lighter (e.g. `$4,250` large, `.25` muted).
- Scale: page title 24–32px, card title 14–16px/600, body and table 12–14px, captions and axis labels 10–12px muted.
- Greeting headlines can go larger (32–48px, weight 500) in the glass and light bento directions.
- Mono used for IDs, timestamps and heatmap labels in data-console style.
- Muted grey (`#7A8190`-ish) for labels, near-black for values; weight carries hierarchy more than size.

## Color
- Neutral base (white cards, grey-tinted canvas) + one accent used consistently. Purple/indigo (finance, SaaS), green (health, HR, sustainability, commerce), orange (fintech, ops), blue (storage, collaboration).
- Semantic chips: green up, red down, amber pending, on pale tinted fills with darker text; rarely solid.
- Chart colour: highlighted series or bar in full accent, other bars in a pale tint or hatched grey (single-hue emphasis). Multi-series charts use 2–4 hues: accent, a complementary orange or green, grey.
- Pastel KPI cards in a row (lilac, coral, blue, mint, yellow) appear in task and order-status views to colour-code states.
- Lime `#D8F35B`–`#B6F23B` is a recurring highlight in newer shots: active nav, delta chips, selected rows.
- Dark variants use near-black with one warm tint, not pure `#000`.

## Components
- **KPI card:** label + info/arrow icon top, value 24–32px, delta chip, comparison text, optional sparkline. Radius 16–20px.
- **Bar chart:** rounded-top bars, inactive bars pale or hatched, active bar accent with floating tooltip showing value and date. Y-axis in light grey, 4–5 gridlines or none.
- **Line/area chart:** smooth curve, gradient fill fading to transparent, hover marker with crosshair and tooltip; two series for current vs previous period.
- **Donut:** thick ring with centre total and legend list with percentages alongside. Radial gauges and semicircle meters for targets and scores.
- **Table:** avatar or thumbnail + name in first column, status pill column, row action "…" menu, pagination with numbered pages, checkbox select, toolbar of search/filter/sort/export. Zebra rarely; hover or selected row tinted.
- **Navigation:** sidebar active item = tinted pill or filled accent block; top tab nav as a pill group with dark active pill; breadcrumb for deep pages.
- **Segmented controls & chips:** Weekly/Monthly/Yearly toggles above charts; filter chips with counts; category tags in pastel fills.
- **Calendar / schedule:** mini month grid with highlighted today and range, plus a list of timed events or a horizontal timeline with coloured blocks.
- **List with avatars:** team members, patients, activity log, with a status dot or time on the right; avatar stacks to show collaborators.
- **Progress:** thin bars, stacked segmented bars (used/reserved/free), checklists with progress (onboarding, "Getting started").
- **Promo/upsell card:** gradient or illustrated card in sidebar or content ("Upgrade", "Go premium").
- **Assistant/chat card:** input with attach, mic and send button, suggestion cards above; seen in AI-flavoured dashboards.
- **Map:** choropleth or dot map with pinned tooltip, paired with a ranked country bar list.
- **Buttons:** primary = filled accent or near-black pill, 36–44px tall, radius 10px–full; secondary = white with hairline border; icon buttons 32–40px round.
- **Kanban board:** columns with counts, task cards with tags, date, comment and attachment counts, assignee avatars.

## Interaction & motion
- Chart hover tooltips with a crosshair or highlighted bar (shown in many static shots, so a core behaviour).
- Date-range and period toggles re-query the charts; segmented tabs swap datasets *(inferred)*.
- Sidebar collapse chevron present in several shots: expanded labelled → icon rail *(inferred)*.
- Light/dark toggle at the sidebar bottom or top bar *(inferred)*.
- Cards with a top-right arrow icon navigate to a detail report *(inferred)*.
- Row "…" menus and checkboxes imply bulk and per-row actions; expand/collapse nav groups with chevrons.
- Glass shots imply background blur and soft transitions; keep fades 150–250ms *(inferred)*.
- Cursor and pointer artefacts in shots show hover on table rows and chart points.
- Onboarding checklists tick off as steps are completed; progress bar updates *(inferred)*.

## Do / Don't
- Do lead with 3–4 KPIs, each with a delta and its comparison period spelled out ("vs last month").
- Do limit to one accent colour plus semantic green/red/amber; assign each colour one meaning.
- Do give every card a title (14–16px/600) and one clear secondary action (arrow or "View all").
- Do keep radii consistent per direction (e.g. 20px cards, 10px inputs, full pills) and gaps on one 4px multiple.
- Do highlight a single bar or point in charts and let others recede.
- Do pin upsell and help cards at the sidebar bottom, away from primary navigation.
- Do show a detail rail (selected record or calendar) beside lists to avoid navigation.
- Don't fill the canvas with 10+ equal-weight modules; size cards by importance.
- Don't set table or axis text below 11px or in grey lighter than `#8A909C` on white.
- Don't rely on colour alone for status; pair with text label or icon.
- Don't use more than 4 series colours in a chart.
- Don't stack heavy shadow, gradient and border on the same card; pick one separator.

## Pinterest-isms to avoid
- **Glass over a busy gradient lowers text contrast (muted grey on translucent pastel).** Fix: keep text at 4.5:1 against the worst-case backdrop; use panels at ≥70% white opacity or a solid fallback.
- **Tiny 9–10px labels and axis text to look "clean".** Fix: floor at 11–12px; hide secondary labels on smaller breakpoints instead of shrinking them.
- **Placeholder numbers and repeated rows ("Name goes here", identical IDs) hide layout failures.** Fix: test with long names, empty states, 0 values and 6-digit amounts.
- **Decorative illustration or photo cards (hero people, buildings, scenery) steal space from data.** Fix: limit to one per screen, or move to empty and onboarding states.
- **Device-frame mockups, tilted perspective and cropped canvases hide the real breakpoints.** Fix: design the flat 1440 and 768 layouts, then present.
- **Floating pill nav and rail icons without labels.** Fix: add labels or tooltips and an accessible name; icon-only rails need 40px+ hit areas.
- **Pastel chart tints that vanish (pale bars on white).** Fix: inactive series at ≥3:1 against the card, add direct value labels on key bars.
- **Dense rainbow KPI cards (5 pastel hues with no meaning).** Fix: tie hue to state or category and keep the same mapping app-wide.
- **Only the happy path shown: no loading, error, empty or permission states.** Fix: specify skeletons and empty cards per module.
- **Neon lime on white used for text or small icons.** Fix: use lime only as a fill with dark text on it; use a deeper green for text.

## Source pins
- https://www.pinterest.com/pin/1013943303629881832/ - Automation dashboard: stat cards, onboarding steps, avatar inbox rail
- https://www.pinterest.com/pin/1025343040190762424/ - Purple rail, greeting hero, bento of tasks and calendar
- https://www.pinterest.com/pin/1027454102473727565/ - Lime delta chips on white cards, dark top bar, tilted showcase
- https://www.pinterest.com/pin/1036039089283963161/ - Glass CRM with flow columns and avatar header row
- https://www.pinterest.com/pin/1040120476466587799/ - Glass HR: big stat trio, onboarding checklist, lime accents
- https://www.pinterest.com/pin/1040120476468426762/ - Black rail, KPI icons, line chart, doctor detail card
- https://www.pinterest.com/pin/1050253575617477537/ - Smart-home glass tiles with sliders and toggles
- https://www.pinterest.com/pin/1056094181380703059/ - Pastel KPI cards over kanban columns with tags
- https://www.pinterest.com/pin/1072419730024552305/ - Lime health metrics, bar chart, gauge, workout widgets
- https://www.pinterest.com/pin/1083326885404847835/ - Glassy sidebar and clean purchase-order table with tabs
- https://www.pinterest.com/pin/1083819466612178450/ - AI chat home: prompt cards, history rail, coral gradient
- https://www.pinterest.com/pin/1084241679077163100/ - Treemap, heatmap and barcode charts in data console
- https://www.pinterest.com/pin/1086000897679429061/ - Property ops: work-order table plus selected-building detail panel
- https://www.pinterest.com/pin/1086000897680509464/ - Beige bento, hatched highlighted bar, donut cost breakdown
- https://www.pinterest.com/pin/1086282372631683597/ - Analytics table with thumbnails, score bars, KPI strip
- https://www.pinterest.com/pin/1087408272565721653/ - Pastel asset tiles, to-do progress, transactions, activity log
- https://www.pinterest.com/pin/1087408272566313251/ - HR kit: green palette across dashboards, calendars, forms
- https://www.pinterest.com/pin/1087408272566703954/ - Dark green sidebar, gradient area chart with tooltip
- https://www.pinterest.com/pin/1090011916101916026/ - Clinical dashboard: KPI strip, risk donut, calendar, legend
- https://www.pinterest.com/pin/1090715603528979232/ - Database console: setup cards, metric strip, status table
- https://www.pinterest.com/pin/1090715603529502427/ - Grouped sidebar with section labels, search shortcut, branch selector
- https://www.pinterest.com/pin/1090715603536693194/ - Sidebar nav with badge, KPI sparkline, product card
- https://www.pinterest.com/pin/1092052609672174058/ - Dark green rail, lime charts, appointment scheduler panel
- https://www.pinterest.com/pin/1093389615817674723/ - Green finance bento: card, rounded bars, payment history table
- https://www.pinterest.com/pin/1094515515720305975/ - AI ops glass: checklist, token/cost sparklines, forecast bar
- https://www.pinterest.com/pin/1096696946786373558/ - Learning dashboard with pastel course cards, progress list
- https://www.pinterest.com/pin/1096696946787432558/ - Warm neutral fleet UI, orange accent, feedback prompt card
- https://www.pinterest.com/pin/1096696946788891413/ - Sales KPIs, highlighted bar, map with tooltips, top products
- https://www.pinterest.com/pin/1098878377861669772/ - Blue-glass education home: activity bars, teacher avatars, course rail
- https://www.pinterest.com/pin/1101693127631977729/ - Long IT admin page: uptime, heatmap, gauges, orange accent
- https://www.pinterest.com/pin/1101693127632256773/ - Same greeting-hero bento: purple rail, calendar, promo card
- https://www.pinterest.com/pin/1101693127632395659/ - Purple upgrade banner, bar and line pair, orders table
- https://www.pinterest.com/pin/1101693127632625332/ - HR employee detail: attendance, leave rings, payroll panels
- https://www.pinterest.com/pin/1101693127632682129/ - Blue file manager: quick-access folders, file table
- https://www.pinterest.com/pin/1101693127632695749/ - Purple finance: money flow bars, budget donut, goal bars
- https://www.pinterest.com/pin/1101693127632991479/ - Project view: task cards, status donut, income vs expense
- https://www.pinterest.com/pin/1101693127633178709/ - Task-management kit: kanban, list, calendar, chat screens
- https://www.pinterest.com/pin/1101693127633661728/ - Pastel order-status cards, blue bars, category donut
- https://www.pinterest.com/pin/1101693127633686721/ - Forest green hatched bars, team status pills
- https://www.pinterest.com/pin/1102256077589825394/ - Social analytics: platform sidebar, tabs, hover crosshair tooltip
- https://www.pinterest.com/pin/1105493039825307003/ - Care dashboard: progress bar, staff list, schedule, AI card
- https://www.pinterest.com/pin/1105493039827270696/ - Grey glass: assistant chat, timeline blocks, big greeting stats
- https://www.pinterest.com/pin/1105844883527479561/ - Dense multilingual stats: KPI progress, donuts, project table
- https://www.pinterest.com/pin/1107322627162676625/ - Orange dot-matrix chart, semicircle donut, KPI row
- https://www.pinterest.com/pin/1107322627163174416/ - Marketplace admin: promo banner, area chart, sortable listings table
- https://www.pinterest.com/pin/1112952126702124222/ - Glass HR again: lime/black onboarding bar and rings
- https://www.pinterest.com/pin/1113515076643761619/ - Black campaign UI: cream highlight bar, pill influencer avatars
- https://www.pinterest.com/pin/1113515076650680260/ - Glass table with row icons and pill pagination
- https://www.pinterest.com/pin/1113515076652004846/ - Logistics: map route, shipments table, green accent on dark
- https://www.pinterest.com/pin/1114781714047326787/ - Indigo finance: quick-send avatars, donut, tinted bars
- https://www.pinterest.com/pin/1116189088932607337/ - Reports: smooth lines, map, donut, row checkbox table
- https://www.pinterest.com/pin/1116189088932975328/ - Green environmental dashboard: dark cards, bars, map
- https://www.pinterest.com/pin/1116189088933107868/ - Invoice detail: big total, segmented progress, colour blocks
- https://www.pinterest.com/pin/1116189088934140552/ - Nested sidebar with count badges and huge earnings value
- https://www.pinterest.com/pin/1121959326097920973/ - Settings page: gradient banner, form rows, sessions list
- https://www.pinterest.com/pin/1121959326103294528/ - Shipping admin: purple pills, map, income sparkline
- https://www.pinterest.com/pin/1122874119628256514/ - AI workspace: red accent, recent chats, storage segments
- https://www.pinterest.com/pin/1125337025667428184/ - Dark-purple invoice list with selected-detail split panel
- https://www.pinterest.com/pin/1125618500638793162/ - Mono-ish ledger: stacked-dot bars, tight tables, light sidebar
- https://www.pinterest.com/pin/1126533294325227941/ - Orange and cream bars, sparkline cards, dark highlight card
