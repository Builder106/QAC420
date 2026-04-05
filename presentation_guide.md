# Presentation Guide: Capitol Alpha

**Project:** Do Members of Congress Beat the Market?
**Course:** QAC 420: Data for Good
**Presenter:** Yinka Vaughan
**Duration:** 10 Minutes + 3 Minutes Q&A
**Date:** Thursday, April 30, 2026
**Location:** ALLB 311 (12:00 PM)

---

## Slide 1: Title Slide
*   **Title:** Capitol Alpha: Do Members of Congress Beat the Market?
*   **Subtitle:** QAC 420: Data for Good
*   **Visual:** Clean, professional title layout.
*   **Speaker Notes:** Introduce yourself and the core premise of the project.

## Slide 2: The Problem Statement
*   **Title:** The Question of Political Accountability
*   **Key Message:** We often hear news about politicians making suspiciously well-timed stock trades. Do the data back this up?
*   **Speaker Notes:** Explain the objective: to aggregate congressional stock returns and benchmark them against the S&P 500. Highlight the "Why" (transparency, accountability, fairness of democracy).

## Slide 3: Data Acquisition & Technical Hurdles
*   **Title:** Wrangling the Disclosures
*   **Key Message:** Getting this data isn't as simple as downloading a CSV.
*   **Speaker Notes:** 
    *   Explain parsing over 16,000+ trades.
    *   Discuss the challenge with House PDFs: using `pdfplumber` and Regex to pull structured tables from messy scans.
    *   Mention bypassing interface limits: using Playwright to inject JavaScript (`dt.page.len(-1).draw()`) to force all rows to render.

## Slide 4: Ethical Considerations
*   **Title:** The Ethics of Web Scraping
*   **Key Message:** Automating transparency is a form of "Data for Good."
*   **Speaker Notes:** Address the ethics of web scraping. This is public data mandated by law. You aren't bypassing security firewalls or accessing private data; you are merely automating the reading of thousands of pages to make the data accessible to citizens.

## Slide 5: Defining the Financial Metrics
*   **Title:** How Do We Measure an "Edge"?
*   **Key Message:** Explaining Jensen's Alpha and Information Advantage Decay simply.
*   **Speaker Notes:** 
    *   **Jensen's Alpha:** Abnormal returns compared to the broader market (S&P 500) relative to risk.
    *   **Information Advantage Decay:** The idea that the value of non-public "insider" knowledge drops off over time (e.g., looking at returns in 30, 60, or 90-day windows).

## Slide 6: Overall Findings & Statistical Significance
*   **Title:** Congress vs. The Market
*   **Asset to Include:** `returns_kde.png`
*   **Key Message:** The data proves a statistically significant edge ($p < 0.05$).
*   **Speaker Notes:** Point to the KDE graph. Highlight that the 90-day return mean for Congressional trades sits at ~7.6%, compared to the S&P 500's historical ~3.4%. It's not just anecdotal; it's proven across thousands of trades.

## Slide 7: Visualizing Trade Volume Over Time
*   **Title:** Who is Trading the Most?
*   **Asset to Include:** link to your interactive Flourish Racing Bar Chart
*   **Key Message:** High-volume trading is a bipartisan phenomenon.
*   **Speaker Notes:** Show how trading volume shifts over time. Point out when specific legislators suddenly spike in volume during major market shifts.

## Slide 8: The "Anomalies": Timing the COVID Crash
*   **Title:** Timing the Market: The COVID Sell-Off
*   **Asset to Include:** `covid_crash_sales.png`
*   **Key Message:** Major panic selling happened *before* the public crashed the market.
*   **Speaker Notes:** This is the storytelling climax. Focus on the annotations:
    *   Sen. Loeffler and others began dumping stocks in mid-January.
    *   Show the massive $37M+ sell-offs by Loeffler and Perdue weeks before the bottom fell out in mid-March.

## Slide 9: What Are They Trading?
*   **Title:** Top Assets & Tech Profiteers
*   **Assets to Include:** `top_assets.png` (maybe alongside `tech_purchases.png` if space permits)
*   **Key Message:** Congress doesn't just sell to avoid crashes; they buy to catch booms.
*   **Speaker Notes:** Briefly note the top traded assets. Then, point out how heavy tech purchases (NVDA, MSFT, AAPL) clustered during the 2020-2021 bull run.

## Slide 10: Societal Implications & Conclusion
*   **Title:** Data for Good: Policy Implications
*   **Key Message:** What this means for voters and legislation.
*   **Speaker Notes:** When elected officials consistently beat the market by seemingly timing global catastrophes or leveraging non-public briefings, it damages institutional trust. Conclude that robust policies banning active stock trading for sitting Congress members are mathematically justified.

## Slide 11: Q&A
*   **Title:** Questions?
*   **Speaker Notes:** Thank the audience and open the floor for the 3-minute Q&A.