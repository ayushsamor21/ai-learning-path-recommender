THEME_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400;14..32,500;14..32,590;14..32,650&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --ink: #050506;
  --surface-1: #0c0c0e;
  --surface-2: #131316;
  --surface-3: #1a1a1e;
  --glass: rgba(255,255,255,0.035);
  --line: rgba(255,255,255,0.11);
  --line-strong: rgba(255,255,255,0.23);
  --ink-1: #f5f5f7;
  --ink-2: rgba(255,255,255,0.60);
  --ink-3: rgba(255,255,255,0.46);
  --violet: #a78bfa;
  --violet-2: #7565ff;
  --violet-soft: rgba(167,139,250,0.12);
  --violet-line: rgba(167,139,250,0.40);
  --coral: #ff6b6b;
  --coral-soft: rgba(255,107,107,0.10);
}

html, body, [class*="css"], .stApp, .stMarkdown, p, span, label, input, textarea {
  font-family: Inter, "SF Pro Display", "Helvetica Neue", sans-serif;
}

.stApp {
  background:
    radial-gradient(900px 520px at 12% -10%, rgba(117,101,255,0.18), transparent 52%),
    radial-gradient(720px 420px at 100% 0%, rgba(255,107,107,0.08), transparent 46%),
    var(--ink);
  color: var(--ink-1);
}

.block-container {
  padding-top: 1.2rem;
  padding-bottom: 3rem;
  max-width: 1180px;
}

[data-testid="stHeader"] { background: transparent; }

[data-testid="stSidebar"] {
  background: var(--surface-1);
  border-right: 1px solid var(--line);
}

[data-testid="stSidebar"] * {
  color: var(--ink-1) !important;
}

[data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] textarea {
  background: var(--surface-2) !important;
  color: var(--ink-1) !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px;
}

h1, h2, h3 {
  letter-spacing: -0.045em;
  font-weight: 590;
}

.stButton > button {
  border-radius: 999px;
  border: 1px solid var(--line-strong);
  background: rgba(255,255,255,0.06);
  color: var(--ink-1);
  font-weight: 560;
  letter-spacing: -0.01em;
}

.stButton > button:hover {
  border-color: var(--violet-line);
  background: var(--violet-soft);
}

.stButton > button[kind="primary"] {
  background: #f5f5f7;
  color: #090909;
  border: none;
}

.stButton > button[kind="primary"]:hover {
  background: #ffffff;
}

div[data-testid="stTabs"] button {
  color: var(--ink-3);
  font-weight: 560;
}

div[data-testid="stTabs"] button[aria-selected="true"] {
  color: var(--ink-1);
}

.stProgress > div > div {
  background: linear-gradient(90deg, var(--violet-2), var(--violet));
}

.gate {
  display: grid;
  place-items: center;
  padding: 36px 0 8px;
}

.gate-inner {
  width: min(560px, 100%);
  text-align: center;
}

.orb {
  width: 72px;
  height: 72px;
  margin: 0 auto 22px;
  border-radius: 50%;
  background:
    radial-gradient(circle at 35% 30%, #fff 0 8%, transparent 18%),
    radial-gradient(circle at 50% 50%, #c4b5fd 0%, #7565ff 42%, #1a1038 100%);
  box-shadow:
    0 0 0 1px rgba(167,139,250,0.35),
    0 0 48px rgba(117,101,255,0.45);
  animation: breathe 3.4s ease-in-out infinite;
}

@keyframes breathe {
  0%, 100% { transform: scale(1); filter: brightness(1); }
  50% { transform: scale(1.06); filter: brightness(1.18); }
}

.kicker {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--violet);
  font-weight: 650;
  margin-bottom: 12px;
}

.display {
  font-size: clamp(2.4rem, 6vw, 4.4rem);
  line-height: 0.95;
  letter-spacing: -0.07em;
  font-weight: 590;
  margin: 0 0 14px;
}

.violet {
  background: linear-gradient(120deg, #fff 10%, #c4b5fd 45%, #7565ff 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}

.lead {
  color: var(--ink-2);
  font-size: 17px;
  line-height: 1.6;
  max-width: 42ch;
  margin: 0 auto 22px;
}

.hero {
  position: relative;
  overflow: hidden;
  background: var(--surface-1);
  border: 1px solid var(--line);
  border-radius: 28px;
  padding: 36px 38px 30px;
  margin-bottom: 22px;
  box-shadow: 0 30px 80px rgba(0,0,0,0.35);
}

.hero::after {
  content: "";
  position: absolute;
  right: -80px;
  top: -80px;
  width: 280px;
  height: 280px;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(117,101,255,0.35), transparent 68%);
  pointer-events: none;
}

.hero-kicker {
  font-size: 11px;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: var(--violet);
  font-weight: 650;
}

.hero-title {
  font-size: clamp(2.1rem, 4vw, 3.4rem);
  line-height: 1.02;
  letter-spacing: -0.055em;
  margin: 8px 0 10px;
}

.hero-copy {
  max-width: 640px;
  color: var(--ink-2);
  font-size: 16px;
  line-height: 1.6;
}

.chip-row {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-top: 16px;
}

.chip {
  border: 1px solid var(--line);
  background: var(--glass);
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  color: var(--ink-2);
}

.chip.hot {
  border-color: var(--violet-line);
  background: var(--violet-soft);
  color: #ddd6fe;
}

.stat {
  background: var(--surface-1);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 16px 18px;
}

.stat b {
  display: block;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 18px;
  line-height: 1.2;
  margin-bottom: 6px;
  color: var(--ink-1);
}

.stat span {
  font-size: 12px;
  color: var(--ink-3);
}

.course {
  background: var(--surface-1);
  border: 1px solid var(--line);
  border-radius: 18px;
  padding: 18px 20px 10px;
  margin-bottom: 12px;
}

.course-meta {
  font-size: 11px;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--violet);
  margin-bottom: 6px;
}

.course h3 {
  margin: 0 0 8px;
  font-size: 1.15rem;
}

.course p {
  color: var(--ink-2);
}

.phase {
  display: grid;
  grid-template-columns: 44px 1fr;
  gap: 14px;
  align-items: start;
  margin: 8px 0 4px;
}

.phase-index {
  width: 44px;
  height: 44px;
  display: grid;
  place-items: center;
  font-family: "JetBrains Mono", ui-monospace, monospace;
  font-size: 13px;
  border: 1px solid var(--line-strong);
  border-radius: 12px;
  background: var(--surface-2);
  color: var(--ink-2);
}

.phase-copy small {
  color: var(--ink-3);
  letter-spacing: 0.08em;
  text-transform: uppercase;
  font-size: 11px;
}

.why {
  border-left: 2px solid var(--violet);
  padding: 6px 0 6px 12px;
  color: var(--ink-2);
  font-size: 13px;
  margin: 0 0 16px;
}

.topbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
  margin-bottom: 18px;
}

.brand {
  font-weight: 650;
  letter-spacing: -0.04em;
  font-size: 18px;
}

.user-pill {
  border: 1px solid var(--line);
  background: var(--glass);
  border-radius: 999px;
  padding: 6px 12px;
  font-size: 12px;
  color: var(--ink-2);
}

.gap-row {
  background: var(--surface-1);
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 14px 16px;
  margin-bottom: 10px;
}

.footer-note {
  color: var(--ink-3);
  font-size: 12px;
  margin-top: 18px;
}

.auth-card {
  margin-top: 8px;
  text-align: left;
  background: var(--surface-2);
  border: 1px solid var(--line);
  border-radius: 20px;
  padding: 8px 16px 18px;
}

.signed-out [data-testid="stSidebar"] {
  display: none;
}
</style>
"""
