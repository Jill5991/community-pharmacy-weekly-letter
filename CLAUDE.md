# CLAUDE.md — Community Pharmacy Weekly Letter

## Project Purpose

This repository generates a **community-pharmacy weekly letter** in Traditional Chinese.
The report is designed for outpatient / community pharmacy use and prioritises updates relevant to:

- 家醫 / 基層照護
- 新陳代謝科
- 腸胃科
- 心臟內科
- 神經內科
- 婦產科
- 牙科

Core source families:

- OpenEvidence MCP (`mcp__openevidence__oe_ask`)
- PubMed MCP (`mcp__claude_ai_PubMed__search_articles`)
- CrossRef journals (`uv run python main.py journals`)
- Web / news feeds (`uv run python main.py scrape`)

This is **not** a disease-specific oncology report anymore.
Every paragraph should answer: "What should a community pharmacist do differently this week?"

---

## Before Writing a New Report

**MANDATORY — do this BEFORE writing a single word of content:**

```bash
# 1. Find the latest report
PREV=$(ls reports/ -t | head -1)
echo "Previous report: $PREV"

# 2. Read it fully — note every approval, warning, shortage, DDI, and workflow change already covered
# 3. Grep recurring topics to avoid repetition
grep -E "GLP-1|SGLT2|NOAC|statin|heart failure|PPI|H\\. pylori|IBD|migraine|epilepsy|dementia|HRT|OCP|DDI|shortage|recall" reports/$PREV
```

Before drafting, answer:

- Which items were already reported with the same recommendation? → **skip**
- Which items are real follow-ups (label expansion, new warning, new monitoring advice)? → keep with `[更新]`
- Which items change counselling / dispensing / monitoring **this week**? → surface first

If a specialty section has no real update this week, write `_本週無新訊號_`.

---

## Report File Naming

```
reports/YYYY-WNN.md
```

Use ISO week number:

```bash
python3 -c "from datetime import date; d=date.today(); print(f'{d.year}-W{d.isocalendar()[1]:02d}')"
```

---

## Weekly Report Structure

### Required 12-section structure (繁體中文)

```md
# 社區藥局每週情報 — YYYY-WNN

> 生成日期：YYYY-MM-DD
> 核心合作科別：家醫 / 內分泌 / 腸胃 / 心臟 / 神經 / 婦產 / 牙科
> 涵蓋期間：...
> 來源：...

## 一、摘要
（本週 5 個最重要變化）

## 二、家醫 / 基層照護
## 三、新陳代謝科
## 四、腸胃科
## 五、心臟內科
## 六、神經內科
## 七、婦產科
## 八、牙科
## 九、藥物安全警訊
## 十、重要交互作用 / DDI
## 十一、本週 Takeaways
## 十二、OpenEvidence 點評
```

For each specialty section, prefer this mini-format:

1. 本週更新
2. 對社區藥局的意義
3. 建議行動 / 轉介 / 監測 / 衛教

Optional appendices after the 12 core sections:

- `## 媒體動態`
- `## 文獻速報`

---

## Writing Rules

- Language: **Traditional Chinese**
- Keep drug names, guideline names, and abbreviations in English
- Prioritise practical outpatient issues: dose, monitoring, contraindications, counselling, adherence, shortage alternatives
- Avoid vague claims like "important" or "significant" without explaining the practice impact
- Cite journal / guideline / regulator / news source whenever possible

### Pregnancy / women’s health format

If a drug update affects pregnancy, fertility, breastfeeding, HRT, or contraception, explicitly include:

- `Pregnancy:` can use / avoid / insufficient evidence / trimester-specific note
- `Lactation:` compatible / caution / avoid
- `Contraception:` whether backup contraception or counselling is needed

Do **not** use outdated pregnancy-letter shorthand alone without explanation.

### DDI format

Every major DDI entry should follow this format:

```md
| 組合 | 嚴重度 | 機轉 | 可能臨床後果 | 社區藥局處置 |
|------|--------|------|--------------|--------------|
```

Prefer concrete actions:

- avoid combination
- stagger administration
- reduce dose
- monitor ECG / potassium / glucose / INR / bleeding
- refer back to prescriber

---

## Data Pipeline

Run before writing:

```bash
uv run python main.py scrape
uv run python main.py journals
```

If Twitter credentials are available:

```bash
uv run python main.py run
```

Cached files:

- `data/webscrape_cache.json`
- `data/journals_cache.json`

Use the Python-collected cache as a **candidate pool**, then filter manually in-session for relevance to community pharmacy.

---

## OpenEvidence Section

Use `mcp__openevidence__oe_ask` with a prompt like:

```text
Based on the following community-pharmacy updates from this week, classify each as:
- practice-changing now
- operationally important for pharmacists
- watchlist only

[list findings]
```

The OpenEvidence section should not repeat the report.
It should synthesise what is truly actionable vs merely interesting.

---

## After Writing

1. Check that the 12 required sections are all present
2. Confirm every specialty section has either a real update or `_本週無新訊號_`
3. Confirm every DDI row includes a pharmacist action
4. Check tables render correctly
5. Run `uv run python main.py report` if needed

---

## Duplicate-Avoidance Checklist

Before finalising:

```bash
PREV=$(ls reports/ -t | head -2 | tail -1)
grep -E "GLP-1|SGLT2|NOAC|statin|heart failure|PPI|H\\. pylori|IBD|migraine|epilepsy|dementia|HRT|OCP|DDI|shortage|recall" reports/$PREV
grep -E "dose|monitor|warning|recall|interaction|contraindication|pregnancy|lactation" reports/$PREV | head -30
```

Rules:

- Same source + same recommendation + same key number → delete
- Same topic + new warning / new label / new workflow implication → keep as `[更新]`
- If nothing changes pharmacist behaviour, leave it out
