`# SmartScraper - Complete Project Documentation

*Een intelligent web scraping platform dat Python, BeautifulSoup, Selenium en LLM API's combineert*

---

## TABLE OF CONTENTS

### PART 1: PROJECT FOUNDATION

1. [Quick Start Guide](#quick-start-guide)
2. [Project Overview](#project-overview)
   - [2.1 Vision & Goals](#21-vision--goals)
   - [2.2 Target Hardware](#22-target-hardware)
   - [2.3 Core Capabilities](#23-core-capabilities)
   - [2.4 Success Metrics](#24-success-metrics)
3. [Technology Stack](#technology-stack)
   - [3.1 Frontend Technologies](#31-frontend-technologies)
   - [3.2 Backend - Scraping](#32-backend---scraping)
   - [3.3 Backend - LLM](#33-backend---llm)
   - [3.4 Storage Solutions](#34-storage-solutions)
   - [3.5 Data Export](#35-data-export)
4. [Architecture](#architecture)
   - [4.1 High-Level Architecture](#41-high-level-architecture)
   - [4.2 The 4-Phase Pipeline](#42-the-4-phase-pipeline)
   - [4.3 Data Flow Sequence](#43-data-flow-sequence)
   - [4.4 Threading Model](#44-threading-model)
5. [Project Structure](#project-structure)
   - [5.1 Complete Directory Tree](#51-complete-directory-tree)
   - [5.2 File Responsibilities](#52-file-responsibilities)
6. [Installation & Setup](#installation--setup)
   - [6.1 Prerequisites](#61-prerequisites)
   - [6.2 Step-by-Step Installation](#62-step-by-step-installation)
   - [6.3 Getting Claude API Key](#63-getting-claude-api-key)
   - [6.4 First Run](#64-first-run)
   - [6.5 Troubleshooting Installation](#65-troubleshooting-installation)
7. [Configuration](#configuration)
   - [7.1 Settings Class](#71-settings-class)
   - [7.2 Environment Variables (.env)](#72-environment-variables-env)
   - [7.3 Configuration Hierarchy](#73-configuration-hierarchy)
   - [7.4 Advanced Configuration](#74-advanced-configuration)

### PART 2: CODE IMPLEMENTATIONS

8. [Core Code - Entry Point](#core-code---entry-point)
   - [8.1 main.py](#81-mainpy)
9. [Core Code - Configuration](#core-code---configuration)
   - [9.1 config/settings.py](#91-configsettingspy)
   - [9.2 .env.example](#92-envexample)
10. [Core Code - Frontend](#core-code---frontend)
    - [10.1 frontend/main_window.py](#101-frontendmain_windowpy)
    - [10.2 frontend/workers/scraper_worker.py](#102-frontendworkersscraper_workerpy)
    - [10.3 frontend/widgets/url_input.py](#103-frontendwidgetsurl_inputpy)
    - [10.4 frontend/widgets/query_input.py](#104-frontendwidgetsquery_inputpy)
    - [10.5 frontend/widgets/method_selector.py](#105-frontendwidgetsmethod_selectorpy)
    - [10.6 frontend/widgets/progress_widget.py](#106-frontendwidgetsprogress_widgetpy)
    - [10.7 frontend/widgets/results_table.py](#107-frontendwidgetsresults_tablepy)
    - [10.8 frontend/widgets/stealth_settings.py](#108-frontendwidgetsstealth_settingspy)
    - [10.9 frontend/widgets/captcha_settings.py](#109-frontendwidgetscaptcha_settingspy)
    - [10.10 frontend/dialogs/captcha_dialog.py](#1010-frontenddialogscaptcha_dialogpy)
11. [Core Code - Backend Engine](#core-code---backend-engine)
    - [11.1 backend/scraper_engine.py](#111-backendscraper_enginepy)
12. [Core Code - Scrapers](#core-code---scrapers)
    - [12.1 backend/scrapers/base_scraper.py](#121-backendscrapersbase_scraperpy)
    - [12.2 backend/scrapers/requests_scraper.py](#122-backendscrapersrequests_scraperpy)
    - [12.3 backend/scrapers/selenium_scraper.py](#123-backendscrapersselenium_scraperpy)
    - [12.4 backend/scrapers/playwright_scraper.py](#124-backendscrapersplaywright_scraperpy)
    - [12.5 backend/scrapers/stealth_playwright_scraper.py](#125-backendscrapersstealth_playwright_scraperpy)
    - [12.6 backend/scrapers/adaptive_scraper.py](#126-backendscrapersadaptive_scraperpy)
13. [Core Code - LLM Integration](#core-code---llm-integration)
    - [13.1 backend/llm/claude_client.py](#131-backendllmclaude_clientpy)
    - [13.2 backend/llm/prompt_builder.py](#132-backendllmprompt_builderpy)
    - [13.3 backend/llm/response_parser.py](#133-backendllmresponse_parserpy)
14. [Core Code - Extractors](#core-code---extractors)
    - [14.1 backend/extractors/smart_extractor.py](#141-backendextractorssmart_extractorpy)
    - [14.2 backend/extractors/regex_extractor.py](#142-backendextractorsregex_extractorpy)
    - [14.3 backend/extractors/bs4_extractor.py](#143-backendextractorsbs4_extractorpy)
15. [Core Code - Storage](#core-code---storage)
    - [15.1 backend/storage/cache_manager.py](#151-backendstoragecache_managerpy)
    - [15.2 backend/storage/learned_selectors.py](#152-backendstoragelearned_selectorspy)
    - [15.3 backend/storage/cookie_manager.py](#153-backendstoragecsookie_managerpy)
    - [15.4 backend/storage/session_manager.py](#154-backendstoragesesion_managerpy)
16. [Core Code - Stealth](#core-code---stealth)
    - [16.1 backend/stealth/rate_limiter.py](#161-backendstealthrate_limiterpy)
    - [16.2 backend/stealth/behavior_simulator.py](#162-backendstealthbehavior_simulatorpy)
17. [Core Code - CAPTCHA](#core-code---captcha)
    - [17.1 backend/captcha/captcha_detector.py](#171-backendcaptchacaptcha_detectorpy)
    - [17.2 backend/captcha/cloudflare_handler.py](#172-backendcaptchacloudflare_handlerpy)
    - [17.3 backend/captcha/manual_solver.py](#173-backendcaptchamanual_solverpy)
    - [17.4 backend/captcha/api_solvers.py](#174-backendcaptchaapi_solverspy)
18. [Core Code - Exporters](#core-code---exporters)
    - [18.1 backend/exporters/data_exporter.py](#181-backendexportersdata_exporterpy)
19. [Core Code - Utilities](#core-code---utilities)
    - [19.1 utils/logger.py](#191-utilsloggerpy)
    - [19.2 utils/budget_manager.py](#192-utilsbudget_managerpy)
    - [19.3 utils/validators.py](#193-utilsvalidatorspy)
20. [Core Code - Styles](#core-code---styles)
    - [20.1 frontend/styles/dark_theme.qss](#201-frontendstylesdarkt_hemeqss)
    - [20.2 frontend/styles/light_theme.qss](#202-frontendstyleslight_themeqss)

### PART 3: FEATURES & OPTIMIZATION

21. [Cost Optimization Strategy](#cost-optimization-strategy)
    - [21.1 The 4-Phase Pipeline Details](#211-the-4-phase-pipeline-details)
    - [21.2 Caching Strategy](#212-caching-strategy)
    - [21.3 Learned Selectors Strategy](#213-learned-selectors-strategy)
    - [21.4 HTML Minimization](#214-html-minimization)
    - [21.5 Budget Management](#215-budget-management)
    - [21.6 Cost Examples & Savings](#216-cost-examples--savings)
22. [Anti-Bot & Stealth Features](#anti-bot--stealth-features)
    - [22.1 Stealth Levels Explained](#221-stealth-levels-explained)
    - [22.2 Rate Limiting Implementation](#222-rate-limiting-implementation)
    - [22.3 Human Behavior Simulation](#223-human-behavior-simulation)
    - [22.4 Browser Fingerprinting](#224-browser-fingerprinting)
    - [22.5 Session Management](#225-session-management)
    - [22.6 User Agent Rotation](#226-user-agent-rotation)
23. [CAPTCHA Handling](#captcha-handling)
    - [23.1 CAPTCHA Detection](#231-captcha-detection)
    - [23.2 Manual Solving Workflow](#232-manual-solving-workflow)
    - [23.3 Cookie Reuse Strategy](#233-cookie-reuse-strategy)
    - [23.4 API Solvers Integration](#234-api-solvers-integration)
    - [23.5 Cloudflare Bypass](#235-cloudflare-bypass)
    - [23.6 CAPTCHA Cost Analysis](#236-captcha-cost-analysis)
24. [Testing Strategy](#testing-strategy)
    - [24.1 Unit Tests](#241-unit-tests)
    - [24.2 Integration Tests](#242-integration-tests)
    - [24.3 Test Sites](#243-test-sites)
    - [24.4 Running Tests](#244-running-tests)

### PART 4: DEPLOYMENT & OPERATIONS

25. [Performance Benchmarks](#performance-benchmarks)
    - [25.1 Expected Performance (HP EliteBook 840 G6)](#251-expected-performance-hp-elitebook-840-g6)
    - [25.2 Scraping Speed by Method](#252-scraping-speed-by-method)
    - [25.3 Memory Usage](#253-memory-usage)
    - [25.4 CPU Usage](#254-cpu-usage)
    - [25.5 Real-World Scenarios](#255-real-world-scenarios)
26. [Troubleshooting Guide](#troubleshooting-guide)
    - [26.1 Common Installation Issues](#261-common-installation-issues)
    - [26.2 Common Runtime Issues](#262-common-runtime-issues)
    - [26.3 Performance Issues](#263-performance-issues)
    - [26.4 API Issues](#264-api-issues)
    - [26.5 CAPTCHA Issues](#265-captcha-issues)
27. [Deployment](#deployment)
    - [27.1 Packaging with PyInstaller](#271-packaging-with-pyinstaller)
    - [27.2 Docker Deployment](#272-docker-deployment)
    - [27.3 Distribution](#273-distribution)
28. [Legal & Ethics](#legal--ethics)
    - [28.1 Legal Considerations](#281-legal-considerations)
    - [28.2 Ethical Guidelines](#282-ethical-guidelines)
    - [28.3 Terms of Service](#283-terms-of-service)
    - [28.4 robots.txt Compliance](#284-robotstxt-compliance)
    - [28.5 Privacy & GDPR](#285-privacy--gdpr)

### PART 5: REFERENCE & APPENDICES

29. [Development Roadmap](#development-roadmap)
    - [29.1 Phase 1: MVP (Completed)](#291-phase-1-mvp-completed)
    - [29.2 Phase 2: Core Features (Completed)](#292-phase-2-core-features-completed)
    - [29.3 Phase 3: Anti-Bot (Completed)](#293-phase-3-anti-bot-completed)
    - [29.4 Phase 4: CAPTCHA (Completed)](#294-phase-4-captcha-completed)
    - [29.5 Future Enhancements](#295-future-enhancements)
30. [API Reference](#api-reference)
    - [30.1 Claude API Pricing](#301-claude-api-pricing)
    - [30.2 CAPTCHA Services Pricing](#302-captcha-services-pricing)
    - [30.3 Cost Calculations](#303-cost-calculations)
31. [Code Style Guide](#code-style-guide)
    - [31.1 Python Conventions](#311-python-conventions)
    - [31.2 Naming Conventions](#312-naming-conventions)
    - [31.3 Documentation Standards](#313-documentation-standards)
    - [31.4 Error Handling Patterns](#314-error-handling-patterns)
32. [Contributing Guidelines](#contributing-guidelines)
    - [32.1 How to Contribute](#321-how-to-contribute)
    - [32.2 Code Review Process](#322-code-review-process)
    - [32.3 Testing Requirements](#323-testing-requirements)
33. [FAQ](#faq)
    - [33.1 General Questions](#331-general-questions)
    - [33.2 Technical Questions](#332-technical-questions)
    - [33.3 Cost Questions](#333-cost-questions)
    - [33.4 Legal Questions](#334-legal-questions)
34. [Glossary](#glossary)
35. [Resources](#resources)
    - [35.1 Official Documentation Links](#351-official-documentation-links)
    - [35.2 Useful Tools](#352-useful-tools)
    - [35.3 Community Resources](#353-community-resources)
36. [Complete Example Session](#complete-example-session)
    - [36.1 Realistic Usage Scenario](#361-realistic-usage-scenario)
    - [36.2 Console Output Example](#362-console-output-example)
    - [36.3 Results Analysis](#363-results-analysis)

### APPENDICES
- [A. Requirements.txt](#a-requirementstxt)
- [B. .gitignore](#b-gitignore)
- [C. README.md Template](#c-readmemd-template)
- [D. Example Prompts for Claude Code](#d-example-prompts-for-claude-code)
- [E. Keyboard Shortcuts](#e-keyboard-shortcuts)
- [F. Environment Variables Reference](#f-environment-variables-reference)

---

## PART 1: PROJECT FOUNDATION

## Quick Start Guide

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/smartscraper.git
cd smartscraper

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env and add your Claude API key

# 5. Run the application
python main.py
```

Voor een snelle start:
1. Voer een URL in
2. Beschrijf wat je wilt extracteren (bijv. "product namen en prijzen")
3. Klik op "Start Scraping"
4. Resultaten worden getoond en kunnen worden geëxporteerd als CSV, JSON, of Excel

## Project Overview

### 2.1 Vision & Goals

SmartScraper is een desktopapplicatie die traditioneel web scraping combineert met LLM-intelligentie om gestructureerde data uit websites te extraheren met behulp van natuurlijke taal queries. Het project streeft naar de volgende doelen:

1. **Democratisering van web scraping**: Maak data extractie toegankelijk voor niet-programmeurs
2. **Flexibiliteit**: Werken met elke website structuur zonder aanpassingen
3. **Kostenefficiëntie**: Minimaliseer API-kosten door intelligente caching en optimalisatie
4. **Ethische operatie**: Respecteer robots.txt, gebruiksvoorwaarden en rate limits
5. **Gebruiksvriendelijkheid**: Intuïtieve GUI voor alle niveaus van technische expertise

### 2.2 Target Hardware

De applicatie is ontworpen om te draaien op standaard consumenten hardware:

- **Laptop:** HP EliteBook 840 G6 (of vergelijkbaar)
- **CPU:** Intel Core i5/i7 (8e/9e generatie)
- **RAM:** 8-16GB
- **GPU:** Geïntegreerd (Intel UHD Graphics 620) - Geen dedicated GPU vereist
- **OS:** Windows/Mac/Linux
- **Schijfruimte:** 100MB voor app, 1GB+ voor cache en sessies

### 2.3 Core Capabilities

1. **Natuurlijke Taal Queries**:
   - "Extraheer alle product namen en prijzen"
   - "Vind contactgegevens op deze pagina"
   - "Verzamel nieuwskoppen en publicatiedatums"

2. **Multi-methode Scraping**:
   - Requests (eenvoudig, snel, voor statische sites)
   - Selenium (compatibiliteit, JavaScript rendering)
   - Playwright (modern, stealth, anti-bot)
   - Adaptieve selectie op basis van site complexiteit

3. **Intelligente Extractie**:
   - LLM-gestuurde HTML analyse
   - CSS selector en XPath generatie
   - Adaptieve parser selectie (regex, BS4, LLM)

4. **Anti-Bot Mitigatie**:
   - Browser vingerafdruk vermomming
   - Menselijk gedrag simulatie
   - Cloudflare en CAPTCHA omzeiling
   - Cookie en sessie beheer

5. **Kostenbeheersing**:
   - 4-fasen pipeline voor optimale LLM-inzet
   - Intelligente caching met domeinspecifieke selectors
   - HTML minimalisatie voor token reductie
   - Budget monitoring en limieten

### 2.4 Success Metrics

1. **Kostenefficiëntie**:
   - Doel: <€0.05 per 1000 items (met optimalisatie)
   - Baseline: €3.00 per 1000 items (zonder optimalisatie)
   - Reductie: 99.9% kostenvermindering

2. **Snelheid**:
   - Met LLM: 3-5 seconden per pagina
   - Met gecachte selectors: 0.5-1 seconde
   - Batch verwerking: 30-60 pagina's per minuut

3. **Slagingspercentage**:
   - Standaard sites: 95%+
   - Beveiligde sites: 80%+
   - Met CAPTCHA: 60%+ (afhankelijk van service)

4. **Gebruikerservaring**:
   - First-time setup: <5 minuten
   - Leercurve: <30 minuten voor basisfunctionaliteit
   - Foutmeldingen: Duidelijk en met suggesties

## Technology Stack

### 3.1 Frontend Technologies

De frontend is gebouwd met PyQt6, een moderne Python binding voor Qt6:

```yaml
GUI Framework: PyQt6 (6.6.1)
Styling: QSS (Qt Style Sheets)
Threading: QThread voor achtergrondoperaties
Dialog Systeem: QDialog voor CAPTCHA, exports
Widgets: Aangepaste componenten (URL input, query input, etc.)
```

**Waarom PyQt6?**
- Moderne en cross-platform UI
- Betere high-DPI ondersteuning dan Tkinter
- Robuust threading model voor niet-blokkerende UI
- Rijk ecosysteem van widgets en componenten

### 3.2 Backend - Scraping

```yaml
HTTP Library: requests (2.31.0)
HTML Parser: BeautifulSoup4 (4.12.3)
Browser Automation:
  - Selenium (4.16.0) - compatibiliteit
  - Playwright (1.40.0) - modern, aanbevolen
```

**Scraping Strategieën**:
1. **Requests + BS4**: Voor eenvoudige, statische sites
   - Voordeel: Zeer snel, weinig bronnen
   - Nadeel: Geen JavaScript ondersteuning

2. **Selenium + BS4**: Voor sites met JavaScript
   - Voordeel: Brede browser ondersteuning
   - Nadeel: Traag, meer bronintensief

3. **Playwright**: Voor complexe, beveiligde sites
   - Voordeel: Stealth mogelijkheden, moderne engine
   - Nadeel: Nieuwere dependency, complexer

4. **Adaptive**: Automatisch kiest beste methode
   - Analyseert site en selecteert optimale scraper
   - Fallback mechanisme bij fouten

### 3.3 Backend - LLM

```yaml
Provider: Anthropic Claude
Model: claude-sonnet-4-20250514 (primair)
API Integratie: Directe REST API calls
Prijzen:
  - Input: $3 per miljoen tokens
  - Output: $15 per miljoen tokens
  - Typische kosten: €0.003 per extractie
Alternatief: claude-haiku-4 (12x goedkoper voor eenvoudige taken)
```

**LLM Functies**:
1. **HTML Analyse**: Identificeert relevante secties
2. **Selector Generatie**: CSS selectors en XPath
3. **Gegevensstructurering**: JSON schema voor resultaten
4. **Extractie Validatie**: Controleert resultaten

### 3.4 Storage Solutions

```yaml
Cache: JSON bestanden (LLM responses)
Selectors: JSON bestanden (geleerde CSS selectors)
Cookies: JSON bestanden (per domein)
Sessions: Persistente browser contexten
Config: .env bestanden (python-dotenv)
```

**Bestandsstructuur**:
```
/storage
  /cache
    /domain1.com
      query1_hash.json
      query2_hash.json
  /selectors
    domain1.com.json
  /cookies
    domain1.com.json
  /sessions
    domain1.com/
```

### 3.5 Data Export

```yaml
CSV: pandas + UTF-8-BOM encoding
JSON: Native Python met pretty-print
Excel: openpyxl met auto-sizing
```

**Export Opties**:
1. **CSV**: Universele compatibiliteit
   - UTF-8 met BOM voor Excel compatibiliteit
   - Aanpasbare scheidingstekens (komma, tab)

2. **JSON**: Structured data
   - Compact of prettified
   - Nested object ondersteuning

3. **Excel**: Rijk formaat
   - Auto-sized kolommen
   - Auto-filtered headers
   - Basische styling

## Architecture

### 4.1 High-Level Architecture

```
┌───────────────────┐         ┌──────────────────┐
│     Frontend      │         │    Backend       │
│  ┌─────────────┐  │         │  ┌────────────┐  │
│  │ MainWindow  │  │         │  │ Scraper    │  │
│  └─────────────┘  │         │  │ Engine     │  │
│         │         │         │  └────────────┘  │
│  ┌─────────────┐  │ Events  │         │        │
│  │ Widgets     │◄─┼─────────┼─────────┘        │
│  └─────────────┘  │         │         │        │
│         │         │         │  ┌────────────┐  │
│  ┌─────────────┐  │         │  │ Scrapers   │  │
│  │ Workers     │◄─┼─────────┼──┤ Extractors │  │
│  └─────────────┘  │         │  │ LLM        │  │
└───────────────────┘         │  └────────────┘  │
                              │         │        │
┌───────────────────┐         │  ┌────────────┐  │
│     Storage       │◄────────┼──┤ Storage    │  │
│  ┌─────────────┐  │         │  │ Managers   │  │
│  │ Cache       │  │         │  └────────────┘  │
│  │ Selectors   │  │         │         │        │
│  │ Cookies     │  │         │  ┌────────────┐  │
│  │ Sessions    │  │         │  │ Exporters  │  │
│  └─────────────┘  │         │  └────────────┘  │
└───────────────────┘         └──────────────────┘
```

De architectuur is ontworpen als een modulair, event-driven systeem met duidelijke scheiding van verantwoordelijkheden:

1. **Frontend Layer**: Gebruikersinteractie, events, threads
   - MainWindow: Primair venster en layout beheer
   - Widgets: Gespecialiseerde UI componenten
   - Workers: Achtergrond threads voor niet-blokkerende operaties

2. **Backend Layer**: Core functionaliteit
   - Scraper Engine: Coördineert het scraping proces
   - Scrapers: Specifieke implementaties voor data ophalen
   - Extractors: Data extractie uit HTML
   - LLM Integratie: AI-gestuurde extractie

3. **Storage Layer**: Persistentie en caching
   - Cache Manager: LLM response caching
   - Selector Manager: Domein-specifieke selectors
   - Cookie/Session Manager: Auth en anti-bot

### 4.2 The 4-Phase Pipeline

Het kernconcept achter de kostenefficiëntie is de 4-fase pipeline voor data extractie:

```
┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────┐
│ Fase 1:  │     │ Fase 2:  │     │ Fase 3:     │     │ Fase 4:  │
│ Selector │     │ Direct   │     │ Template    │     │ Full LLM │
│ Lookup   │────▶│ Extract  │────▶│ Based       │────▶│ Extract  │
│          │     │          │     │ Extract     │     │          │
│ (0 API)  │     │ (0 API)  │     │ (1 API)     │     │ (2 API)  │
└──────────┘     └──────────┘     └─────────────┘     └──────────┘
```

1. **Fase 1: Selector Lookup** (0 API calls)
   - Zoek in cache naar CSS selectors voor dit domein/query
   - Als gevonden, gebruik direct voor extractie
   - Geen API kosten

2. **Fase 2: Direct Extract** (0 API calls)
   - Probeer extractie met generieke selectors/heuristieken
   - Werkt voor standaard formaten (product lijsten, etc.)
   - Geen API kosten

3. **Fase 3: Template-Based Extract** (1 API call)
   - Minimaliseer HTML om tokens te verminderen
   - Stuur naar LLM met specifiek extractie template
   - Gebruik selectors uit response voor extractie
   - Sla selectors op voor toekomstig gebruik
   - 1 API call

4. **Fase 4: Full LLM Extract** (2 API calls)
   - Als eerdere fasen mislukken, gebruik volledige LLM analyse
   - 1 API call om selectors te genereren
   - 1 API call voor directe extractie uit HTML
   - Sla resultaten op in cache

### 4.3 Data Flow Sequence

Het typische dataflow pad door het systeem:

```
1. User Input (URL + Query)
   │
2. URL Validation
   │
3. Scraper Selection
   │
4. HTML Retrieval
   │
5. ┌──────────────────────┐
   │ 4-Phase Extraction   │
   │ 1. Cached Selectors  │
   │ 2. Generic Extractors │
   │ 3. Template Extract   │
   │ 4. Full LLM Extract   │
   └──────────────────────┘
   │
6. Results Processing
   │
7. Display & Export
```

1. **User Input**: URL en natuurlijke taalquery
2. **Validatie**: Controleer URL, robots.txt, bereikbaarheid
3. **Scraper Selectie**: Kies requests/selenium/playwright
4. **HTML Ophalen**: Haal pagina op, handel JS/CAPTCHA af
5. **4-Fase Extractie**: Doorloop pipeline voor optimale kosten
6. **Resultaten Verwerken**: Structureer data, valideer
7. **Weergeven & Exporteren**: Toon resultaten, exporteer

### 4.4 Threading Model

```
Main Thread (UI)                  Worker Threads
┌─────────────────┐               ┌─────────────────┐
│ PyQt6 Event Loop│◄──────────────┤ ScraperWorker   │
└─────────────────┘ signals       └─────────────────┘
        │                                  │
        │                         ┌─────────────────┐
┌─────────────────┐               │ BrowserContext  │
│ UI Updates      │◄──────────────┤ (Selenium/PW)   │
└─────────────────┘ signals       └─────────────────┘
        │                                  │
        │                         ┌─────────────────┐
│ Progress Updates │◄──────────────┤ LLM Client     │
└─────────────────┘ signals       └─────────────────┘
```

SmartScraper gebruikt een event-driven threading model om een responsieve UI te garanderen:

1. **Main Thread (UI Thread)**
   - Verantwoordelijk voor de PyQt event loop
   - Handelt gebruikersinteractie af
   - Ontvangt signalen van worker threads
   - Updatet UI componenten

2. **Worker Threads**
   - **ScraperWorker**: Primaire thread voor scraping
   - **BrowserContext**: Selenium/Playwright browser instances
   - **LLMClient**: API requests naar Claude

3. **Signalen & Slots**
   - Voorkomt race conditions en UI freezes
   - Standaard PyQt signaling mechanisme
   - Voortgang updates voor lange operaties

## Project Structure

### 5.1 Complete Directory Tree

```
smartscraper/
├── main.py                     # Entry point
├── requirements.txt            # Dependencies
├── .env.example                # Environment variables template
├── README.md                   # Project documentation
├── config/
│   └── settings.py             # Configuration class
├── backend/
│   ├── scraper_engine.py       # Core engine
│   ├── scrapers/
│   │   ├── base_scraper.py     # Abstract base class
│   │   ├── requests_scraper.py # Simple HTTP requests
│   │   ├── selenium_scraper.py # Selenium implementation
│   │   ├── playwright_scraper.py # Playwright implementation
│   │   ├── stealth_playwright_scraper.py # Anti-bot features
│   │   └── adaptive_scraper.py # Auto-selects best method
│   ├── llm/
│   │   ├── claude_client.py    # API client
│   │   ├── prompt_builder.py   # Prompts construction
│   │   └── response_parser.py  # Parse JSON responses
│   ├── extractors/
│   │   ├── smart_extractor.py  # Orchestrates extraction
│   │   ├── regex_extractor.py  # Simple patterns
│   │   └── bs4_extractor.py    # BeautifulSoup parser
│   ├── storage/
│   │   ├── cache_manager.py    # LLM response caching
│   │   ├── learned_selectors.py # Store CSS selectors
│   │   ├── cookie_manager.py   # Store/retrieve cookies
│   │   └── session_manager.py  # Browser session mgmt
│   ├── stealth/
│   │   ├── rate_limiter.py     # Prevent overloading sites
│   │   └── behavior_simulator.py # Human-like behavior
│   ├── captcha/
│   │   ├── captcha_detector.py # Detect CAPTCHA challenges
│   │   ├── cloudflare_handler.py # CF-specific logic
│   │   ├── manual_solver.py    # UI for manual solving
│   │   └── api_solvers.py      # 2captcha, etc.
│   └── exporters/
│       └── data_exporter.py    # CSV, JSON, Excel export
├── frontend/
│   ├── main_window.py          # Main application window
│   ├── workers/
│   │   └── scraper_worker.py   # Background thread
│   ├── widgets/
│   │   ├── url_input.py        # URL input field
│   │   ├── query_input.py      # Natural lang query field
│   │   ├── method_selector.py  # Scraping method selector
│   │   ├── progress_widget.py  # Progress bar & status
│   │   ├── results_table.py    # Results display grid
│   │   ├── stealth_settings.py # Anti-bot settings UI
│   │   └── captcha_settings.py # CAPTCHA settings UI
│   ├── dialogs/
│   │   └── captcha_dialog.py   # Manual CAPTCHA solving
│   └── styles/
│       ├── dark_theme.qss      # Dark mode styling
│       └── light_theme.qss     # Light mode styling
├── utils/
│   ├── logger.py               # Logging utilities
│   ├── budget_manager.py       # Track API usage/costs
│   └── validators.py           # URL/input validation
└── storage/                    # Runtime storage
    ├── cache/                  # LLM response cache
    ├── selectors/              # Learned CSS selectors
    ├── cookies/                # Stored cookies
    └── sessions/               # Browser sessions
```

### 5.2 File Responsibilities

#### Core Files

**main.py**
- Entry point voor de applicatie
- Initialiseert de configuratie
- Start de PyQt main window
- Handelt command line argumenten af

**config/settings.py**
- Centrale configuratieclass
- Laadt settings uit .env en defaults
- Biedt validatie voor instellingen

**backend/scraper_engine.py**
- Coördineert het scraping proces
- Orkestreert andere componenten
- Implementeert 4-fase pipeline
- Afhandeling van fouten en retries

**frontend/main_window.py**
- Primaire UI container
- Verbindt widgets en handlers
- Beheert signalen en slots
- Handelt menu acties af

#### Key Components

**Scraper Classes**
- **base_scraper.py**: Abstracte basis interface
- **requests_scraper.py**: Simpele HTTP
- **selenium_scraper.py**: Volledige browser
- **playwright_scraper.py**: Moderne browser
- **adaptive_scraper.py**: Auto-selectie

**LLM Integration**
- **claude_client.py**: Anthropic API client
- **prompt_builder.py**: Genereert prompts
- **response_parser.py**: Verwerkt antwoorden

**Extractors**
- **smart_extractor.py**: Pipeline coördinator
- **regex_extractor.py**: Eenvoudige patronen
- **bs4_extractor.py**: DOM parsing

**Storage**
- **cache_manager.py**: LLM response caching
- **learned_selectors.py**: Selectoren opslaan
- **cookie_manager.py**: Cookie persistentie
- **session_manager.py**: Browser sessies

## Installation & Setup

### 6.1 Prerequisites

**Software vereisten:**
- Python 3.10 of hoger
- pip (Python package manager)
- git (optional, voor clonen repository)
- Een webbrowser (Chrome of Firefox aanbevolen)

**API vereisten:**
- Anthropic Claude API key
- (Optioneel) 2captcha of vergelijkbare CAPTCHA service API key

**OS-specifieke vereisten:**

Voor Windows:
```bash
# Microsoft C++ Build Tools
winget install Microsoft.VisualStudio.2022.BuildTools
# or
choco install visualstudio2022buildtools
```

Voor macOS:
```bash
# Xcode command line tools
xcode-select --install

# Homebrew (optional maar aanbevolen)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Voor Linux:
```bash
# Debian/Ubuntu
sudo apt-get update
sudo apt-get install -y python3-dev python3-pip build-essential

# Fedora
sudo dnf install python3-devel gcc
```

### 6.2 Step-by-Step Installation

Volg deze stappen om SmartScraper te installeren:

```bash
# 1. Clone the repository (of download zip)
git clone https://github.com/yourusername/smartscraper.git
cd smartscraper

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Setup environment variables
cp .env.example .env
# Edit .env and add your Claude API key
```

**Installatie verificatie:**

Test de installatie door te controleren of de vereiste drivers beschikbaar zijn:

```bash
# Test browsers
python -c "from playwright.sync_api import sync_playwright; playwright = sync_playwright().start(); browser = playwright.chromium.launch(); page = browser.new_page(); page.goto('https://example.com'); print('Playwright OK'); browser.close(); playwright.stop()"

# Test BeautifulSoup
python -c "from bs4 import BeautifulSoup; soup = BeautifulSoup('<html><body>Test</body></html>', 'html.parser'); print('BeautifulSoup OK')"

# Test PyQt6
python -c "from PyQt6.QtWidgets import QApplication; app = QApplication([]); print('PyQt6 OK')"
```

### 6.3 Getting Claude API Key

Om SmartScraper te gebruiken, heb je een Claude API key nodig:

1. **Registreer voor Anthropic API toegang**
   - Ga naar [https://console.anthropic.com/](https://console.anthropic.com/)
   - Maak een account of log in
   - Navigeer naar API Keys sectie

2. **Genereer een nieuwe API key**
   - Klik op "Create API Key"
   - Geef een naam (bijv. "SmartScraper")
   - Stel gebruikslimiet in (aanbevolen)

3. **Configureer SmartScraper**
   - Kopieer de API key
   - Plak in je .env bestand: `CLAUDE_API_KEY=your-api-key`

4. **Verificatie testen**
   - Run: `python -m backend.llm.claude_client --test`
   - Bevestigt dat je key correct werkt

**API kosten management:**

- Standaard limiet: €5 per maand
- Wijzig in .env: `API_COST_LIMIT=5.00`
- Logbestand: `storage/api_usage.log`
- Reset met: `python -m utils.budget_manager --reset`

### 6.4 First Run

Start de applicatie voor de eerste keer:

```bash
# Activate virtual environment if not already active
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run SmartScraper
python main.py
```

**Eerste gebruik checklist:**

1. Accepteer de drivers installatie (indien gevraagd)
2. Controleer API connectie status (groen/rood indicator)
3. Bekijk de Quick Start Guide via Help menu
4. Run een eenvoudige test scrape (bijv. example.com)

**Voorbeeld eerste scrape:**

1. URL: `https://books.toscrape.com/`
2. Query: `Extract all book titles and prices`
3. Method: Auto-select
4. Klik op "Start Scraping"
5. Bekijk resultaten in de tabel
6. Exporteer als CSV/JSON/Excel

### 6.5 Troubleshooting Installation

**Common Issues & Solutions**

1. **ModuleNotFoundError**
   ```
   ModuleNotFoundError: No module named 'PyQt6'
   ```
   Oplossing: Controleer of virtual env geactiveerd is en installeer opnieuw:
   ```bash
   pip install -r requirements.txt
   ```

2. **Playwright Browser Errors**
   ```
   Error: Executable doesn't exist at /path/to/browser
   ```
   Oplossing: Installeer browsers handmatig:
   ```bash
   playwright install
   ```

3. **API Key Issues**
   ```
   AuthenticationError: Invalid API key
   ```
   Oplossing: Controleer of .env correct is ingesteld en herstart app

4. **PyQt Display Issues**
   ```
   Qt: Could not initialize GLX
   ```
   Oplossing voor Linux:
   ```bash
   sudo apt install libxcb-xinerama0 libgl1-mesa-glx
   ```

5. **Permission Denied for storage/**
   ```
   PermissionError: [Errno 13] Permission denied: 'storage/cache'
   ```
   Oplossing:
   ```bash
   chmod -R 755 storage/
   ```

6. **WebDriverException (Selenium)**
   ```
   WebDriverException: Message: unknown error: cannot find Chrome binary
   ```
   Oplossing: Installeer Chrome/Firefox, of specificeer pad:
   ```python
   # In .env
   SELENIUM_BROWSER_PATH=/path/to/browser
   ```

## Configuration

### 7.1 Settings Class

De centrale configuratielogica in `config/settings.py` beheert alle instellingen:

```python
# config/settings.py
import os
from dotenv import load_dotenv

class Settings:
    """Central configuration for SmartScraper."""
    
    def __init__(self):
        """Initialize settings from .env and defaults."""
        # Load from .env file if it exists
        load_dotenv()
        
        # API Keys
        self.claude_api_key = os.getenv("CLAUDE_API_KEY", "")
        self.captcha_api_key = os.getenv("CAPTCHA_API_KEY", "")
        
        # LLM Settings
        self.llm_model = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")
        self.llm_temp = float(os.getenv("LLM_TEMPERATURE", "0.0"))
        self.llm_timeout = int(os.getenv("LLM_TIMEOUT", "30"))
        self.enable_caching = os.getenv("ENABLE_CACHING", "True").lower() == "true"
        
        # Scraping Settings
        self.default_method = os.getenv("DEFAULT_METHOD", "auto")
        self.max_pages = int(os.getenv("MAX_PAGES", "5"))
        self.requests_timeout = int(os.getenv("REQUESTS_TIMEOUT", "10"))
        
        # Anti-Bot
        self.stealth_mode = int(os.getenv("STEALTH_MODE", "1"))  # 0=Off, 1=Basic, 2=Advanced
        self.rate_limit = float(os.getenv("RATE_LIMIT", "1.0"))  # Seconds between requests
        
        # CAPTCHA
        self.captcha_service = os.getenv("CAPTCHA_SERVICE", "manual")  # manual, 2captcha, etc.
        self.captcha_autosolve = os.getenv("CAPTCHA_AUTOSOLVE", "False").lower() == "true"
        
        # Budget Control
        self.api_cost_limit = float(os.getenv("API_COST_LIMIT", "5.00"))  # EUR
        self.track_usage = os.getenv("TRACK_USAGE", "True").lower() == "true"
        
        # UI Settings
        self.theme = os.getenv("THEME", "light")  # light or dark
        self.results_limit = int(os.getenv("RESULTS_LIMIT", "1000"))
        self.window_size = os.getenv("WINDOW_SIZE", "1024x768")
        
        # Storage Paths
        self.storage_dir = os.getenv("STORAGE_DIR", "storage")
        self.cache_dir = os.path.join(self.storage_dir, "cache")
        self.selector_dir = os.path.join(self.storage_dir, "selectors")
        self.cookie_dir = os.path.join(self.storage_dir, "cookies")
        self.session_dir = os.path.join(self.storage_dir, "sessions")
        
        # Create directories if they don't exist
        for directory in [self.cache_dir, self.selector_dir, self.cookie_dir, self.session_dir]:
            os.makedirs(directory, exist_ok=True)
    
    def validate(self):
        """Validate settings and return errors if any."""
        errors = []
        
        if not self.claude_api_key:
            errors.append("CLAUDE_API_KEY is not set")
            
        if self.captcha_service != "manual" and not self.captcha_api_key:
            errors.append(f"CAPTCHA_API_KEY is required for {self.captcha_service}")
            
        if self.default_method not in ["auto", "requests", "selenium", "playwright"]:
            errors.append(f"Invalid DEFAULT_METHOD: {self.default_method}")
            
        return errors
    
    def to_dict(self):
        """Return settings as dictionary (for UI display)."""
        # Filter out sensitive info like API keys
        safe_dict = {k: v for k, v in self.__dict__.items() 
                    if not k.endswith('_api_key')}
        return safe_dict
```

### 7.2 Environment Variables (.env)

The `.env.example` file provides a template for configuration:

```ini
# API Keys
CLAUDE_API_KEY=your-claude-api-key-here
CAPTCHA_API_KEY=your-captcha-api-key-here

# LLM Settings
LLM_MODEL=claude-sonnet-4-20250514
LLM_TEMPERATURE=0.0
LLM_TIMEOUT=30
ENABLE_CACHING=True

# Scraping Settings
DEFAULT_METHOD=auto
MAX_PAGES=5
REQUESTS_TIMEOUT=10

# Anti-Bot
STEALTH_MODE=1
RATE_LIMIT=1.0

# CAPTCHA
CAPTCHA_SERVICE=manual
CAPTCHA_AUTOSOLVE=False

# Budget Control
API_COST_LIMIT=5.00
TRACK_USAGE=True

# UI Settings
THEME=light
RESULTS_LIMIT=1000
WINDOW_SIZE=1024x768

# Storage Paths
STORAGE_DIR=storage
```

### 7.3 Configuration Hierarchy

SmartScraper volgt een gelaagde configuratiehiërarchie:

1. **Defaults**: Hardcoded in Settings class
2. **.env bestand**: Overschrijft defaults
3. **Command line arguments**: Overschrijven .env
4. **UI instellingen**: Tijdelijke overschrijvingen

Voorbeeld om config vanuit command line in te stellen:

```bash
python main.py --model=claude-haiku-4 --stealth=2 --theme=dark
```

### 7.4 Advanced Configuration

Voor gevorderde aanpassingen zijn er extra configuratie-opties:

**Aangepaste Browser Profielen (Stealth)**:

In `stealth_config.json`:
```json
{
  "profiles": [
    {
      "name": "Chrome Windows",
      "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
      "viewport": {"width": 1920, "height": 1080},
      "platform": "Windows",
      "locales": ["en-US", "en"],
      "colorScheme": "light"
    },
    {
      "name": "Firefox Mac",
      "user_agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:95.0) Gecko/20100101 Firefox/95.0",
      "viewport": {"width": 1440, "height": 900},
      "platform": "MacOS",
      "locales": ["en-US", "en"],
      "colorScheme": "dark"
    }
  ]
}
```

**Aangepaste Prompts**:

Aanpasbare extractie prompt templates in `prompt_templates.json`:
```json
{
  "extract_products": "Analyse deze HTML pagina en identificeer alle producten met hun prijzen en beschrijvingen. Geef de resultaten terug als JSON array met objecten die de volgende velden bevatten: 'name', 'price', 'description'.",
  
  "extract_contact": "Vind alle contactinformatie op deze pagina, inclusief telefoonnummers, e-mail adressen, fysieke adressen en contactformulieren. Geef de resultaten terug als JSON.",
  
  "extract_articles": "Identificeer alle nieuwsartikelen of blogposts op deze pagina. Extract voor elk artikel de titel, datum, auteur en een korte samenvatting. Geef terug als JSON array."
}
```

**Logging configuratie**:

Aangepaste logging in `logging.ini`:
```ini
[loggers]
keys=root,scraper,llm,ui

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=INFO
handlers=consoleHandler

[logger_scraper]
level=INFO
handlers=fileHandler
qualname=backend.scrapers
propagate=0

[logger_llm]
level=DEBUG
handlers=fileHandler
qualname=backend.llm
propagate=0

[logger_ui]
level=INFO
handlers=consoleHandler
qualname=frontend
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=INFO
formatter=simpleFormatter
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=simpleFormatter
args=('smartscraper.log', 'a')

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

## PART 2: CODE IMPLEMENTATIONS

## Core Code - Entry Point

### 8.1 main.py

```python
#!/usr/bin/env python3
"""
SmartScraper - Intelligent web scraping tool with LLM integration
"""
import sys
import argparse
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication

from config.settings import Settings
from frontend.main_window import MainWindow
from utils.logger import setup_logging


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="SmartScraper - Intelligent web scraping")
    
    # Basic options
    parser.add_argument('--url', help='URL to scrape')
    parser.add_argument('--query', help='Natural language query for extraction')
    parser.add_argument('--method', choices=['auto', 'requests', 'selenium', 'playwright'],
                       help='Scraping method to use')
    
    # Output options
    parser.add_argument('--output', help='Output file path')
    parser.add_argument('--format', choices=['csv', 'json', 'excel'], 
                       help='Output format')
    
    # Config options
    parser.add_argument('--config', help='Path to config file')
    parser.add_argument('--model', help='LLM model to use')
    parser.add_argument('--theme', choices=['light', 'dark'],
                       help='UI theme')
    parser.add_argument('--stealth', type=int, choices=[0, 1, 2],
                       help='Stealth mode level')
    
    # Headless mode
    parser.add_argument('--headless', action='store_true',
                       help='Run in headless mode (no GUI)')
    
    return parser.parse_args()


def main():
    """Main entry point."""
    # Parse command line arguments
    args = parse_arguments()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting SmartScraper")
    
    # Load settings
    settings = Settings()
    errors = settings.validate()
    
    # Override settings from command line if provided
    if args.model:
        settings.llm_model = args.model
    if args.stealth is not None:
        settings.stealth_mode = args.stealth
    if args.theme:
        settings.theme = args.theme
    
    # Ensure directories exist
    Path(settings.storage_dir).mkdir(exist_ok=True)
    Path(settings.cache_dir).mkdir(exist_ok=True)
    Path(settings.selector_dir).mkdir(exist_ok=True)
    Path(settings.cookie_dir).mkdir(exist_ok=True)
    Path(settings.session_dir).mkdir(exist_ok=True)
    
    # Headless mode
    if args.headless:
        if not args.url or not args.query:
            logger.error("Headless mode requires --url and --query")
            sys.exit(1)
        
        from backend.scraper_engine import ScraperEngine
        
        engine = ScraperEngine(settings)
        results = engine.scrape(args.url, args.query, args.method or settings.default_method)
        
        if args.output:
            from backend.exporters.data_exporter import DataExporter
            
            exporter = DataExporter()
            format_type = args.format or 'json'
            exporter.export(results, args.output, format_type)
            logger.info(f"Results exported to {args.output}")
        else:
            import json
            print(json.dumps(results, indent=2))
    else:
        # GUI mode
        app = QApplication(sys.argv)
        
        # Check for configuration errors
        if errors:
            from PyQt6.QtWidgets import QMessageBox
            error_msg = QMessageBox()
            error_msg.setIcon(QMessageBox.Icon.Critical)
            error_msg.setWindowTitle("Configuration Error")
            error_msg.setText("There are configuration errors:")
            error_msg.setDetailedText("\n".join(errors))
            error_msg.exec()
        
        # Start main window
        window = MainWindow(settings)
        
        # Pre-populate fields if provided
        if args.url:
            window.url_input.setText(args.url)
        if args.query:
            window.query_input.setText(args.query)
        
        window.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

## Core Code - Configuration

### 9.1 config/settings.py

```python
"""
Configuration management for SmartScraper.
"""
import os
import json
from pathlib import Path
from dotenv import load_dotenv


class Settings:
    """Central configuration for SmartScraper."""
    
    def __init__(self):
        """Initialize settings from .env and defaults."""
        # Load from .env file if it exists
        load_dotenv()
        
        # API Keys
        self.claude_api_key = os.getenv("CLAUDE_API_KEY", "")
        self.captcha_api_key = os.getenv("CAPTCHA_API_KEY", "")
        
        # LLM Settings
        self.llm_model = os.getenv("LLM_MODEL", "claude-sonnet-4-20250514")
        self.llm_temp = float(os.getenv("LLM_TEMPERATURE", "0.0"))
        self.llm_timeout = int(os.getenv("LLM_TIMEOUT", "30"))
        self.enable_caching = os.getenv("ENABLE_CACHING", "True").lower() == "true"
        
        # Scraping Settings
        self.default_method = os.getenv("DEFAULT_METHOD", "auto")
        self.max_pages = int(os.getenv("MAX_PAGES", "5"))
        self.requests_timeout = int(os.getenv("REQUESTS_TIMEOUT", "10"))
        self.respect_robots = os.getenv("RESPECT_ROBOTS", "True").lower() == "true"
        
        # Anti-Bot
        self.stealth_mode = int(os.getenv("STEALTH_MODE", "1"))  # 0=Off, 1=Basic, 2=Advanced
        self.rate_limit = float(os.getenv("RATE_LIMIT", "1.0"))  # Seconds between requests
        
        # CAPTCHA
        self.captcha_service = os.getenv("CAPTCHA_SERVICE", "manual")  # manual, 2captcha, etc.
        self.captcha_autosolve = os.getenv("CAPTCHA_AUTOSOLVE", "False").lower() == "true"
        
        # Budget Control
        self.api_cost_limit = float(os.getenv("API_COST_LIMIT", "5.00"))  # EUR
        self.track_usage = os.getenv("TRACK_USAGE", "True").lower() == "true"
        
        # UI Settings
        self.theme = os.getenv("THEME", "light")  # light or dark
        self.results_limit = int(os.getenv("RESULTS_LIMIT", "1000"))
        self.window_size = os.getenv("WINDOW_SIZE", "1024x768")
        
        # Storage Paths
        self.storage_dir = os.getenv("STORAGE_DIR", "storage")
        self.cache_dir = os.path.join(self.storage_dir, "cache")
        self.selector_dir = os.path.join(self.storage_dir, "selectors")
        self.cookie_dir = os.path.join(self.storage_dir, "cookies")
        self.session_dir = os.path.join(self.storage_dir, "sessions")
        
        # Create directories if they don't exist
        for directory in [self.cache_dir, self.selector_dir, self.cookie_dir, self.session_dir]:
            os.makedirs(directory, exist_ok=True)
            
        # Load stealth profiles if they exist
        self.stealth_profiles = []
        stealth_config_path = Path(__file__).parent / 'stealth_config.json'
        if stealth_config_path.exists():
            with open(stealth_config_path, 'r') as f:
                stealth_config = json.load(f)
                self.stealth_profiles = stealth_config.get('profiles', [])
    
    def validate(self):
        """Validate settings and return errors if any."""
        errors = []
        
        if not self.claude_api_key:
            errors.append("CLAUDE_API_KEY is not set")
            
        if self.captcha_service != "manual" and not self.captcha_api_key:
            errors.append(f"CAPTCHA_API_KEY is required for {self.captcha_service}")
            
        if self.default_method not in ["auto", "requests", "selenium", "playwright"]:
            errors.append(f"Invalid DEFAULT_METHOD: {self.default_method}")
            
        return errors
    
    def to_dict(self):
        """Return settings as dictionary (for UI display)."""
        # Filter out sensitive info like API keys
        safe_dict = {k: v for k, v in self.__dict__.items() 
                    if not k.endswith('_api_key') and not isinstance(v, (list, dict))}
        return safe_dict
    
    def get_stealth_profile(self, profile_name=None):
        """Get a stealth profile by name or a random one if name is None."""
        import random
        
        if not self.stealth_profiles:
            # Default profile
            return {
                "name": "Default",
                "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/96.0.4664.110 Safari/537.36",
                "viewport": {"width": 1920, "height": 1080},
                "platform": "Windows",
                "locales": ["en-US", "en"],
                "colorScheme": "light"
            }
        return random.choice(self.stealth_profiles) if profile_name is None else \
               next((p for p in self.stealth_profiles if p["name"] == profile_name), 
                   self.stealth_profiles[0] if self.stealth_profiles else None)
```

### 9.2 .env.example

```ini
# API Keys
CLAUDE_API_KEY=your-claude-api-key-here
CAPTCHA_API_KEY=your-captcha-api-key-here

# LLM Settings
LLM_MODEL=claude-sonnet-4-20250514
LLM_TEMPERATURE=0.0
LLM_TIMEOUT=30
ENABLE_CACHING=True

# Scraping Settings
DEFAULT_METHOD=auto
MAX_PAGES=5
REQUESTS_TIMEOUT=10
RESPECT_ROBOTS=True

# Anti-Bot
STEALTH_MODE=1
RATE_LIMIT=1.0

# CAPTCHA
CAPTCHA_SERVICE=manual
CAPTCHA_AUTOSOLVE=False

# Budget Control
API_COST_LIMIT=5.00
TRACK_USAGE=True

# UI Settings
THEME=light
RESULTS_LIMIT=1000
WINDOW_SIZE=1024x768

# Storage Paths
STORAGE_DIR=storage
```

## Core Code - Frontend

### 10.1 frontend/main_window.py

# frontend/main_window.py

"""
Main Application Window
Coordinates all UI components and worker threads
"""

import logging
from datetime import datetime

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QTabWidget,
    QGroupBox, QSplitter, QTextEdit
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from .widgets.url_input import URLInputWidget
from .widgets.query_input import QueryInputWidget
from .widgets.method_selector import MethodSelectorWidget
from .widgets.stealth_settings import StealthSettingsWidget
from .widgets.captcha_settings import CaptchaSettingsWidget
from .widgets.progress_widget import ProgressWidget
from .widgets.status_widget import StatusWidget
from .widgets.results_table import ResultsTableWidget
from .workers.scraper_worker import ScraperWorker
from .dialogs.captcha_dialog import CaptchaSolverDialog

from backend.exporters.data_exporter import DataExporter


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # State
        self.worker = None
        self.total_scraped = 0
        self.total_cost = 0.0
        self.results = []
        
        self.setup_ui()
        self.setup_connections()
        
        self.logger.info("Main window initialized")
    
    def setup_ui(self):
        """Setup user interface"""
        
        self.setWindowTitle("SmartScraper - AI-Powered Web Scraping")
        self.setGeometry(100, 100, 1400, 900)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Header
        header = self.create_header()
        main_layout.addWidget(header)
        
        # Main content - split view
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: Input & Settings
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right side: Results & Console
        right_panel = self.create_right_panel()
        splitter.addWidget(right_panel)
        
        splitter.setStretchFactor(0, 1)  # Left: 30%
        splitter.setStretchFactor(1, 2)  # Right: 70%
        
        main_layout.addWidget(splitter)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def create_header(self):
        """Create application header"""
        header = QWidget()
        layout = QVBoxLayout(header)
        
        # Title
        title = QLabel("🕷️ SmartScraper")
        title_font = QFont()
        title_font.setPointSize(24)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("AI-Powered Web Scraping with Natural Language")
        subtitle.setStyleSheet("color: #888888; font-size: 14px;")
        layout.addWidget(subtitle)
        
        return header
    
    def create_left_panel(self):
        """Create left panel with inputs and settings"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Input Section
        input_group = QGroupBox("📝 Scraping Configuration")
        input_layout = QVBoxLayout()
        
        self.url_input = URLInputWidget()
        input_layout.addWidget(self.url_input)
        
        self.query_input = QueryInputWidget()
        input_layout.addWidget(self.query_input)
        
        self.method_selector = MethodSelectorWidget()
        input_layout.addWidget(self.method_selector)
        
        input_group.setLayout(input_layout)
        layout.addWidget(input_group)
        
        # Settings Tabs
        settings_tabs = QTabWidget()
        
        self.stealth_settings = StealthSettingsWidget()
        settings_tabs.addTab(self.stealth_settings, "🕵️ Stealth")
        
        self.captcha_settings = CaptchaSettingsWidget()
        settings_tabs.addTab(self.captcha_settings, "🧩 CAPTCHA")
        
        layout.addWidget(settings_tabs)
        
        # Control Buttons
        control_layout = QHBoxLayout()
        
        self.start_btn = QPushButton("🚀 Start Scraping")
        self.start_btn.setMinimumHeight(40)
        self.start_btn.setStyleSheet("""
            QPushButton {
                background-color: #0d7377;
                color: white;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #14a0a6;
            }
        """)
        control_layout.addWidget(self.start_btn)
        
        self.stop_btn = QPushButton("⏹ Stop")
        self.stop_btn.setMinimumHeight(40)
        self.stop_btn.setEnabled(False)
        control_layout.addWidget(self.stop_btn)
        
        layout.addLayout(control_layout)
        
        # Progress & Status
        self.progress_widget = ProgressWidget()
        layout.addWidget(self.progress_widget)
        
        self.status_widget = StatusWidget()
        layout.addWidget(self.status_widget)
        
        layout.addStretch()
        
        return panel
    
    def create_right_panel(self):
        """Create right panel with results and console"""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        # Results Section
        results_group = QGroupBox("📊 Results")
        results_layout = QVBoxLayout()
        
        # Stats bar
        stats_layout = QHBoxLayout()
        
        self.stats_label = QLabel("Total: 0 | Cost: €0.00")
        self.stats_label.setStyleSheet("font-weight: bold; font-size: 14px;")
        stats_layout.addWidget(self.stats_label)
        
        stats_layout.addStretch()
        
        results_layout.addLayout(stats_layout)
        
        # Results table
        self.results_table = ResultsTableWidget()
        results_layout.addWidget(self.results_table)
        
        # Export buttons
        export_layout = QHBoxLayout()
        
        self.export_csv_btn = QPushButton("📊 Export CSV")
        self.export_csv_btn.setEnabled(False)
        export_layout.addWidget(self.export_csv_btn)
        
        self.export_json_btn = QPushButton("📄 Export JSON")
        self.export_json_btn.setEnabled(False)
        export_layout.addWidget(self.export_json_btn)
        
        self.export_excel_btn = QPushButton("📗 Export Excel")
        self.export_excel_btn.setEnabled(False)
        export_layout.addWidget(self.export_excel_btn)
        
        results_layout.addLayout(export_layout)
        
        results_group.setLayout(results_layout)
        layout.addWidget(results_group, stretch=2)
        
        # Console Section
        console_group = QGroupBox("💻 Console Log")
        console_layout = QVBoxLayout()
        
        self.console = QTextEdit()
        self.console.setReadOnly(True)
        self.console.setMaximumHeight(200)
        console_layout.addWidget(self.console)
        
        console_group.setLayout(console_layout)
        layout.addWidget(console_group, stretch=1)
        
        return panel
    
    def setup_connections(self):
        """Connect signals and slots"""
        
        # Control buttons
        self.start_btn.clicked.connect(self.start_scraping)
        self.stop_btn.clicked.connect(self.stop_scraping)
        
        # Export buttons
        self.export_csv_btn.clicked.connect(self.export_csv)
        self.export_json_btn.clicked.connect(self.export_json)
        self.export_excel_btn.clicked.connect(self.export_excel)
    
    def start_scraping(self):
        """Start scraping process"""
        
        # Validate input
        urls = self.url_input.get_urls()
        query = self.query_input.get_query()
        
        if not urls:
            QMessageBox.warning(self, "No URLs", "Please enter at least one URL.")
            return
        
        if not query:
            QMessageBox.warning(self, "No Query", "Please enter a query.")
            return

            # Get configuration
        method = self.method_selector.get_selected_method()
        stealth_config = self.stealth_settings.get_settings()
        captcha_config = self.captcha_settings.get_settings()
        
        # Combine configs
        config = {
            **self.config.to_dict(),
            **stealth_config,
            **captcha_config,
            'method': method
        }
        
        # Log start
        self.log_console(f"Starting scraping of {len(urls)} URL(s)")
        self.log_console(f"Query: {query}")
        self.log_console(f"Method: {method}")
        self.log_console(f"Stealth: {stealth_config['stealth_level']}")
        
        # Create and start worker
        self.worker = ScraperWorker(
            urls=urls,
            query=query,
            config=config
        )
        
        # Connect worker signals
        self.worker.progress_update.connect(self.on_progress_update)
        self.worker.result_ready.connect(self.on_result_ready)
        self.worker.captcha_detected.connect(self.on_captcha_detected)
        self.worker.captcha_solved.connect(self.on_captcha_solved)
        self.worker.blocking_detected.connect(self.on_blocking_detected)
        self.worker.stealth_level_changed.connect(self.on_stealth_changed)
        self.worker.finished.connect(self.on_scraping_finished)
        self.worker.error.connect(self.on_error)
        
        # Start
        self.worker.start()
        
        # Update UI
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.export_csv_btn.setEnabled(False)
        self.export_json_btn.setEnabled(False)
        self.export_excel_btn.setEnabled(False)
        
        # Reset stats
        self.total_scraped = 0
        self.total_cost = 0.0
        self.results = []
        self.results_table.clear_results()
        
        self.statusBar().showMessage("Scraping...")
    
    def stop_scraping(self):
        """Stop scraping process"""
        
        if self.worker:
            self.log_console("Stopping scraper...")
            self.worker.stop()
            self.statusBar().showMessage("Stopping...")
    
    def on_progress_update(self, percent, message):
        """Handle progress updates"""
        
        self.progress_widget.set_progress(percent, message)
        self.statusBar().showMessage(message)
    
    def on_result_ready(self, result):
        """Handle new result"""
        
        # Add to table
        self.results_table.add_result(result)
        
        # Store result
        self.results.append(result)
        
        # Update stats
        self.total_scraped += 1
        cost = result.get('cost', 0.0)
        self.total_cost += cost
        
        self.stats_label.setText(
            f"Total: {self.total_scraped} | Cost: €{self.total_cost:.4f}"
        )
        
        # Log
        source = result.get('source', 'unknown')
        duration = result.get('duration', 0)
        self.log_console(
            f"✅ Result #{self.total_scraped}: {source} "
            f"({duration:.1f}s, €{cost:.4f})"
        )
    
    def on_captcha_detected(self, url, strategy):
        """Handle CAPTCHA detection"""
        
        self.log_console(f"🧩 CAPTCHA detected on {url}")
        self.status_widget.show_blocking_warning("CAPTCHA detected", strategy)
        
        if strategy == 'manual':
            # Show manual solving dialog
            dialog = CaptchaSolverDialog(
                url,
                timeout_seconds=self.captcha_settings.manual_timeout.value(),
                parent=self
            )
            
            # Connect signals
            dialog.solved.connect(self.worker.on_captcha_solved)
            dialog.timeout.connect(self.worker.on_captcha_timeout)
            
            # Show dialog (blocking)
            result = dialog.exec()
            
            if result == dialog.DialogCode.Rejected:
                self.log_console("❌ CAPTCHA solving cancelled")
                self.worker.stop()
        
        elif strategy == 'api':
            self.log_console("🤖 Solving CAPTCHA with API...")
            # API solving happens automatically in worker
        
        else:  # skip
            self.log_console("⏭️ Skipping due to CAPTCHA")
            self.worker.stop()
    
    def on_captcha_solved(self, method):
        """Handle CAPTCHA solved"""
        
        self.log_console(f"✅ CAPTCHA solved using {method}")
        self.status_widget.hide_blocking_warning()
        
        # Show success notification
        self.statusBar().showMessage(f"CAPTCHA solved - continuing...", 3000)
    
    def on_blocking_detected(self, reason, action):
        """Handle blocking detection"""
        
        self.log_console(f"⚠️ BLOCKING: {reason}")
        self.log_console(f"   ACTION: {action}")
        self.status_widget.show_blocking_warning(reason, action)
    
    def on_stealth_changed(self, new_level):
        """Handle stealth level change"""
        
        self.log_console(f"🔼 Stealth increased to: {new_level}")
        self.status_widget.update_stealth_level(new_level)
    
    def on_scraping_finished(self):
        """Handle scraping completion"""
        
        # Update UI
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        if self.results:
            self.export_csv_btn.setEnabled(True)
            self.export_json_btn.setEnabled(True)
            self.export_excel_btn.setEnabled(True)
        
        # Update status
        self.progress_widget.set_complete()
        self.status_widget.hide_blocking_warning()
        
        # Log completion
        self.log_console("")
        self.log_console("="*60)
        self.log_console(f"✅ SCRAPING COMPLETE")
        self.log_console(f"Total items: {self.total_scraped}")
        self.log_console(f"Total cost: €{self.total_cost:.4f}")
        self.log_console("="*60)
        
        self.statusBar().showMessage(
            f"Complete! Scraped {self.total_scraped} items (€{self.total_cost:.4f})"
        )
        
        # Show notification
        if self.total_scraped > 0:
            QMessageBox.information(
                self,
                "Scraping Complete",
                f"Successfully scraped {self.total_scraped} items!\n\n"
                f"Total cost: €{self.total_cost:.4f}\n"
                f"Average cost per item: €{self.total_cost/self.total_scraped:.5f}\n\n"
                f"Results are ready to export."
            )
    
    def on_error(self, error_message):
        """Handle error"""
        
        self.log_console(f"❌ ERROR: {error_message}")
        
        # Reset UI
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_widget.set_error()
        
        # Show error dialog
        QMessageBox.critical(
            self,
            "Scraping Error",
            f"An error occurred:\n\n{error_message}\n\n"
            f"Check the console for details."
        )
        
        self.statusBar().showMessage("Error occurred")
    
    def export_csv(self):
        """Export results to CSV"""
        self._export('csv')
    
    def export_json(self):
        """Export results to JSON"""
        self._export('json')
    
    def export_excel(self):
        """Export results to Excel"""
        self._export('excel')
    
    def _export(self, format_type):
        """Export results to specified format"""
        
        from PyQt6.QtWidgets import QFileDialog
        
        # Generate filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        if format_type == 'csv':
            default_name = f"scrape_results_{timestamp}.csv"
            file_filter = "CSV Files (*.csv)"
        elif format_type == 'json':
            default_name = f"scrape_results_{timestamp}.json"
            file_filter = "JSON Files (*.json)"
        else:  # excel
            default_name = f"scrape_results_{timestamp}.xlsx"
            file_filter = "Excel Files (*.xlsx)"
        
        # Show save dialog
        filename, _ = QFileDialog.getSaveFileName(
            self,
            f"Export {format_type.upper()}",
            str(self.config.EXPORTS_DIR / default_name),
            file_filter
        )
        
        if not filename:
            return
        
        try:
            # Export
            exporter = DataExporter()
            
            if format_type == 'csv':
                exporter.export_csv(self.results, filename)
            elif format_type == 'json':
                exporter.export_json(self.results, filename)
            else:
                exporter.export_excel(self.results, filename)
            
            self.log_console(f"✅ Exported to {filename}")
            
            QMessageBox.information(
                self,
                "Export Successful",
                f"Results exported to:\n{filename}"
            )
            
        except Exception as e:
            self.log_console(f"❌ Export failed: {e}")
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export results:\n{str(e)}"
            )
    
    def log_console(self, message):
        """Log message to console widget"""
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.append(f"[{timestamp}] {message}")
        
        # Auto-scroll to bottom
        scrollbar = self.console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

# 10.2 backend - scarper engine

# backend/scraper_engine.py

"""
Main Scraper Engine - Orchestrates all backend operations
Implements 4-phase pipeline for cost optimization
"""

import time
import logging
from urllib.parse import urlparse

from .scrapers.requests_scraper import RequestsScraper
from .scrapers.selenium_scraper import SeleniumScraper
from .scrapers.playwright_scraper import PlaywrightScraper
from .scrapers.stealth_playwright_scraper import StealthPlaywrightScraper
from .scrapers.adaptive_scraper import AdaptiveScraper

from .llm.claude_client import ClaudeClient
from .extractors.smart_extractor import SmartExtractor
from .storage.cache_manager import CacheManager
from .storage.learned_selectors import LearnedSelectors
from .utils.budget_manager import BudgetManager


class ScraperEngine:
    """
    Main orchestrator for scraping operations
    Coordinates scrapers, LLM, cache, and storage
    """
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self._initialize_scrapers()
        self._initialize_llm()
        self._initialize_storage()
        self._initialize_budget()
    
    def _initialize_scrapers(self):
        """Initialize scraping methods"""
        
        self.scrapers = {
            'requests': RequestsScraper(),
            'selenium': SeleniumScraper(),
            'playwright': PlaywrightScraper(),
            'stealth': StealthPlaywrightScraper(self.config),
            'adaptive': AdaptiveScraper(self.config)
        }
        
        self.logger.info("Initialized scrapers: requests, selenium, playwright, stealth, adaptive")
    
    def _initialize_llm(self):
        """Initialize LLM client"""
        
        api_key = self.config.get('CLAUDE_API_KEY')
        if not api_key:
            raise ValueError("CLAUDE_API_KEY not found in configuration")
        
        self.llm_client = ClaudeClient(
            api_key=api_key,
            model=self.config.get('CLAUDE_MODEL')
        )
        
        self.extractor = SmartExtractor(self.llm_client)
        
        self.logger.info(f"Initialized LLM client: {self.config.get('CLAUDE_MODEL')}")
    
    def _initialize_storage(self):
        """Initialize storage components"""
        
        self.cache = CacheManager(
            cache_file=self.config.get('CACHE_FILE'),
            ttl_days=self.config.get('CACHE_TTL_DAYS', 7),
            enabled=self.config.get('CACHE_ENABLED', True)
        )
        
        self.learned = LearnedSelectors(
            storage_file=self.config.get('LEARNED_FILE')
        )
        
        self.logger.info("Initialized storage: cache, learned selectors")
    
    def _initialize_budget(self):
        """Initialize budget manager"""
        
        daily_limit = self.config.get('DAILY_BUDGET', 5.0)
        self.budget = BudgetManager(daily_limit=daily_limit)
        
        self.logger.info(f"Initialized budget manager: €{daily_limit}/day")
    
    def scrape_single(self, url, query, method='auto'):
        """
        Scrape a single URL
        
        Implements 4-phase pipeline:
        1. Check cache (instant, free)
        2. Use learned selectors (fast, free)
        3. Try simple extraction (fast, free)
        4. Use LLM if needed (slower, costs money)
        
        Args:
            url: URL to scrape
            query: Natural language query
            method: Scraping method (auto, requests, selenium, playwright)
        
        Returns:
            dict: Extracted data with metadata
        """
        
        self.logger.info(f"Starting scrape: {url}")
        self.logger.debug(f"Query: {query}")
        self.logger.debug(f"Method: {method}")
        
        start_time = time.time()
        
        # ============= PHASE 1: CACHE CHECK =============
        self.logger.debug("Phase 1: Checking cache...")
        
        cached_result = self.cache.get(url, query)
        if cached_result:
            elapsed = time.time() - start_time
            self.logger.info(f"✅ Cache hit! ({elapsed:.3f}s, €0.00)")
            
            cached_result['source'] = 'cache'
            cached_result['duration'] = elapsed
            cached_result['cost'] = 0.0
            
            return cached_result
        
        # ============= PHASE 2: GET HTML =============
        self.logger.debug(f"Phase 2: Fetching HTML with {method}...")
        
        try:
            html = self._get_html(url, method)
            self.logger.debug(f"Retrieved {len(html)} characters of HTML")
        except Exception as e:
            self.logger.error(f"Failed to get HTML: {e}")
            raise
        
        # ============= PHASE 3: LEARNED SELECTORS =============
        self.logger.debug("Phase 3: Checking learned selectors...")
        
        domain = self._get_domain(url)
        
        if self.learned.has_selectors(domain):
            self.logger.info("🎓 Found learned selectors for this domain")
            
            try:
                selectors = self.learned.get(domain)
                result = self.extractor.extract_with_selectors(html, selectors)
                
                if self._validate_result(result):
                    elapsed = time.time() - start_time
                    self.logger.info(f"✅ Extracted with learned selectors ({elapsed:.1f}s, €0.00)")
                    
                    result['source'] = 'learned_selectors'
                    result['duration'] = elapsed
                    result['cost'] = 0.0
                    result['url'] = url
                    
                    # Cache this result
                    self.cache.set(url, query, result)
                    
                    return result
                else:
                    self.logger.warning("Learned selectors returned invalid data")
            
            except Exception as e:
                self.logger.warning(f"Learned selectors failed: {e}")
        
        # ============= PHASE 4: SIMPLE EXTRACTION =============
        self.logger.debug("Phase 4: Trying simple extraction...")
        
        try:
            simple_result = self.extractor.try_simple_extraction(html, query)
            
            if simple_result and self._validate_result(simple_result):
                elapsed = time.time() - start_time
                self.logger.info(f"✅ Simple extraction succeeded ({elapsed:.1f}s, €0.00)")
                
                simple_result['source'] = 'simple_extraction'
                simple_result['duration'] = elapsed
                simple_result['cost'] = 0.0
                simple_result['url'] = url
                
                self.cache.set(url, query, simple_result)
                
                return simple_result
        
        except Exception as e:
            self.logger.debug(f"Simple extraction failed: {e}")
        
        # ============= PHASE 5: LLM EXTRACTION =============
        self.logger.debug("Phase 5: Using LLM (last resort)...")
        
        # Check budget
        estimated_cost = 0.003
        if not self.budget.can_make_call(estimated_cost):
            raise Exception(
                f"Daily budget exceeded! "
                f"Used: €{self.budget.spent_today:.2f} / €{self.budget.daily_limit:.2f}"
            )
        
        try:
            # Minimize HTML to reduce costs
            html_snippet = self._minimize_html(html)
            
            # Call LLM
            self.logger.info("🤖 Calling Claude API...")
            llm_result = self.llm_client.extract_data(html_snippet, query)
            
            # Calculate actual cost
            actual_cost = llm_result.get('cost', estimated_cost)
            self.budget.log_call(actual_cost)
            
            elapsed = time.time() - start_time
            self.logger.info(f"✅ LLM extraction complete ({elapsed:.1f}s, €{actual_cost:.4f})")
            
            # Enhance result
            llm_result['source'] = 'llm'
            llm_result['duration'] = elapsed
            llm_result['cost'] = actual_cost
            llm_result['url'] = url
            
            # Cache for future
            self.cache.set(url, query, llm_result)
            
            # Learn selectors if provided
            if 'selectors' in llm_result and llm_result['selectors']:
                self.learned.save(domain, llm_result['selectors'])
                self.logger.info(f"📚 Learned selectors for {domain}")
            
            return llm_result
        
        except Exception as e:
            self.logger.error(f"LLM extraction failed: {e}")
            raise
    
    def _get_html(self, url, method):
        """Get HTML using specified scraping method"""
        
        if method == 'auto':
            method = self._detect_best_method(url)
            self.logger.debug(f"Auto-selected method: {method}")
        
        # Use adaptive scraper for stealth/anti-bot features
        if self.config.get('stealth_level') != 'off':
            scraper = self.scrapers['adaptive']
        else:
            scraper = self.scrapers.get(method)
            if not scraper:
                raise ValueError(f"Unknown scraping method: {method}")
        
        return scraper.scrape(url)
    
    def _minimize_html(self, html, max_chars=5000):
        """Reduce HTML size to minimize LLM costs"""
        
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove unnecessary elements
        for tag in soup(['script', 'style', 'nav', 'header', 
                        'footer', 'iframe', 'noscript', 'svg']):
            tag.decompose()
        
        # Get main content area
        main = (
            soup.find('main') or 
            soup.find('article') or 
            soup.find(class_='content') or
            soup.find(id='content') or
            soup.body
        )
        
        if main:
            text = str(main)[:max_chars]
        else:
            text = str(soup)[:max_chars]
        
        return text
    
    def _validate_result(self, result):
        """Check if extraction result is valid"""
        
        if not result or not isinstance(result, dict):
            return False
        
        # Check if we got actual data
        data = result.get('data', {})
        if not data:
            return False
        
        # Check if fields are not empty
        non_empty = sum(1 for v in data.values() if v)
        return non_empty > 0
    
    def _detect_best_method(self, url):
        """Auto-detect best scraping method for URL"""
        
        import requests
        
        try:
            response = requests.head(url, timeout=3, allow_redirects=True)
            content_type = response.headers.get('content-type', '').lower()
            
            # Heuristics
            if 'application/json' in content_type:
                return 'playwright'  # Likely SPA
            
            # Check URL patterns
            if any(pattern in url for pattern in ['/api/', 'react', 'angular', 'vue']):
                return 'playwright'
            
            # Default to fast method
            return 'requests'
        
        except:
            # If HEAD fails, use most capable method
            return 'playwright'
    
    @staticmethod
    def _get_domain(url):
        """Extract domain from URL"""
        return urlparse(url).netloc

 # LLM Client

 # backend/llm/claude_client.py

"""
Claude API Client
Handles all communication with Anthropic's Claude API
"""

import requests
import json
import time
import logging


class ClaudeClient:
    """
    Wrapper for Anthropic Claude API
    Implements retry logic, error handling, and cost tracking
    """
    
    def __init__(self, api_key, model="claude-sonnet-4-20250514"):
        self.api_key = api_key
        self.model = model
        self.base_url = "https://api.anthropic.com/v1/messages"
        self.max_retries = 3
        self.retry_delay = 2
        self.logger = logging.getLogger(__name__)
    
    def extract_data(self, html, query):
        """
        Extract structured data from HTML using Claude
        
        Args:
            html: HTML content (minimized)
            query: Natural language query
        
        Returns:
            dict: {
                'data': {...extracted data...},
                'selectors': {...css selectors...},
                'confidence': 0.95,
                'cost': 0.003
            }
        """
        
        # Build optimized prompt
        prompt = self._build_extraction_prompt(html, query)
        
        # Call API with retry logic
        response_text = self._call_with_retry(prompt)
        
        # Parse JSON response
        result = self._parse_response(response_text)
        
        # Calculate cost
        cost = self._calculate_cost(prompt, response_text)
        result['cost'] = cost
        
        return result
    
    def _build_extraction_prompt(self, html, query):
        """Build optimized prompt for data extraction"""
        
        return f"""Extract the following information from this HTML: {query}

HTML:
{html}

CRITICAL INSTRUCTIONS:
1. Return ONLY valid JSON, no markdown, no explanations
2. Use this exact structure:
{{
    "data": {{
        "field1": "extracted_value1",
        "field2": "extracted_value2"
    }},
    "selectors": {{
        "field1": "css_selector1",
        "field2": "css_selector2"
    }},
    "confidence": 0.95
}}

3. If a field is not found, use null
4. Include CSS selectors so we can extract without AI next time
5. Confidence: 0-1 score of extraction accuracy
6. DO NOT include any text outside the JSON object"""
    
    def _call_with_retry(self, prompt, max_tokens=2000):
        """
        Call Claude API with exponential backoff retry logic
        """
        
        for attempt in range(self.max_retries):
            try:
                response = requests.post(
                    self.base_url,
                    headers={
                        "Content-Type": "application/json",
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01"
                    },
                    json={
                        "model": self.model,
                        "max_tokens": max_tokens,
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt
                            }
                        ]
                    },
                    timeout=30
                )
                
                # Check for errors
                if response.status_code == 429:
                    # Rate limited
                    retry_after = int(response.headers.get('retry-after', 5))
                    self.logger.warning(f"Rate limited, waiting {retry_after}s...")
                    time.sleep(retry_after)
                    continue
                
                response.raise_for_status()
                
                # Extract text from response
                result = response.json()
                return result['content'][0]['text']
            
            except requests.exceptions.Timeout:
                self.logger.warning(f"API timeout (attempt {attempt + 1}/{self.max_retries})")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise
            
            except requests.exceptions.RequestException as e:
                self.logger.error(f"API request failed: {e}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                raise
        
        raise Exception(f"Failed after {self.max_retries} attempts")
    
    def _parse_response(self, response_text):
        """
        Parse JSON from Claude's response
        Handles markdown code blocks and other formatting
        """
        
        # Clean up response
        text = response_text.strip()
        
        # Remove markdown code blocks
        if text.startswith('```json'):
            text = text[7:]
        elif text.startswith('```'):
            text = text[3:]
        
        if text.endswith('```'):
            text = text[:-3]
        
        text = text.strip()
        
        # Parse JSON
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            self.logger.error(f"Failed to parse JSON: {e}")
            self.logger.error(f"Response text: {text[:500]}")
            
            # Try to extract JSON from mixed content
            import re
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(0))
                except:
                    pass
            
            raise ValueError(f"Could not parse JSON from response: {text[:200]}")
    
    def _calculate_cost(self, prompt, response):
        """
        Calculate API cost based on token usage
        
        Claude Sonnet pricing:
        - Input: $3 per million tokens
        - Output: $15 per million tokens
        
        Rough estimate: 4 characters ≈ 1 token
        """
        
        input_tokens = len(prompt) / 4
        output_tokens = len(response) / 4
        
        input_cost = (input_tokens / 1_000_000) * 3
        output_cost = (output_tokens / 1_000_000) * 15
        
        total_cost = input_cost + output_cost
        
        return round(total_cost, 6)       

# backend/storage/learned_selectors.py

"""
Learned Selectors Storage
Stores CSS selectors learned from LLM analysis per domain
"""

import json
import logging
from pathlib import Path


class LearnedSelectors:
    """Manage learned CSS selectors per domain"""
    
    def __init__(self, storage_file='data/learned_selectors.json'):
        self.storage_file = Path(storage_file)
        self.logger = logging.getLogger(__name__)
        self.selectors = self._load()
        
        self.logger.info(f"Learned selectors initialized: {len(self.selectors)} domains")
    
    def has_selectors(self, domain):
        """Check if we have learned selectors for domain"""
        return domain in self.selectors
    
    def get(self, domain):
        """Get selectors for domain"""
        return self.selectors.get(domain)
    
    def save(self, domain, selectors):
        """
        Save learned selectors for domain
        
        Args:
            domain: Domain name (e.g., 'example.com')
            selectors: Dict of field -> CSS selector mappings
        """
        
        self.selectors[domain] = {
            'selectors': selectors,
            'learned_at': datetime.now().isoformat(),
            'usage_count': self.selectors.get(domain, {}).get('usage_count', 0)
        }
        
        self._save()
        self.logger.info(f"Saved selectors for {domain}")
    
    def increment_usage(self, domain):
        """Increment usage counter for domain"""
        
        if domain in self.selectors:
            self.selectors[domain]['usage_count'] = \
                self.selectors[domain].get('usage_count', 0) + 1
            self._save()
    
    def get_stats(self):
        """Get statistics about learned selectors"""
        
        if not self.selectors:
            return {
                'total_domains': 0,
                'total_savings': 0
            }
        
        total_usage = sum(
            domain_data.get('usage_count', 0)
            for domain_data in self.selectors.values()
        )
        
        # Each usage saves ~$0.003
        total_savings = total_usage * 0.003
        
        return {
            'total_domains': len(self.selectors),
            'total_usage': total_usage,
            'total_savings': round(total_savings, 2)
        }
    
    def _load(self):
        """Load learned selectors from file"""
        
        if not self.storage_file.exists():
            return {}
        
        try:
            with open(self.storage_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            self.logger.error(f"Failed to load learned selectors: {e}")
            return {}
    
    def _save(self):
        """Save learned selectors to file"""
        
        try:
            self.storage_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.storage_file, 'w', encoding='utf-8') as f:
                json.dump(self.selectors, f, indent=2, ensure_ascii=False)
        
        except Exception as e:
            self.logger.error(f"Failed to save learned selectors: {e}")


from datetime import datetime

# backend/storage/cookie_manager.py

"""
Cookie Manager for CAPTCHA Handling
Saves cookies after CAPTCHA solving for reuse
"""

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path


class CookieManager:
    """Manage CAPTCHA cookies for reuse"""
    
    def __init__(self, storage_dir='data/cookies'):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)
        
        self.logger.info(f"Cookie manager initialized: {self.storage_dir}")
    
    def save_cookies(self, domain, cookies):
        """
        Save cookies after CAPTCHA solving
        
        Args:
            domain: Domain name (e.g., 'example.com')
            cookies: List of cookie dicts from Playwright
        """
        
        cookie_file = self._get_cookie_file(domain)
        
        # Add timestamp
        data = {
            'timestamp': datetime.now().isoformat(),
            'domain': domain,
            'cookies': cookies
        }
        
        with open(cookie_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"💾 Saved {len(cookies)} cookies for {domain}")
    
    def load_cookies(self, domain, max_age_hours=24):
        """
        Load previously saved cookies
        
        Args:
            domain: Domain name
            max_age_hours: Maximum age of cookies to accept
        
        Returns:
            list or None: Cookies if valid, None if expired or not found
        """
        
        cookie_file = self._get_cookie_file(domain)
        
        if not cookie_file.exists():
            return None
        
        try:
            with open(cookie_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check age
            timestamp = datetime.fromisoformat(data['timestamp'])
            age = datetime.now() - timestamp
            
            if age > timedelta(hours=max_age_hours):
                self.logger.debug(
                    f"⚠️  Cookies for {domain} are too old "
                    f"({age.total_seconds()/3600:.1f}h)"
                )
                return None
            
            self.logger.info(
                f"✅ Loaded {len(data['cookies'])} cookies for {domain} "
                f"(age: {age.total_seconds()/3600:.1f}h)"
            )
            
            return data['cookies']
        
        except Exception as e:
            self.logger.error(f"❌ Error loading cookies: {e}")
            return None
    
    def has_valid_cookies(self, domain, max_age_hours=24):
        """Check if valid cookies exist for domain"""
        cookies = self.load_cookies(domain, max_age_hours)
        return cookies is not None
    
    def delete_cookies(self, domain):
        """Delete cookies for domain"""
        
        cookie_file = self._get_cookie_file(domain)
        
        if cookie_file.exists():
            cookie_file.unlink()
            self.logger.info(f"🗑️  Deleted cookies for {domain}")
    
    def clear_all(self):
        """Clear all saved cookies"""
        
        count = 0
        for cookie_file in self.storage_dir.glob("*.json"):
            cookie_file.unlink()
            count += 1
        
        self.logger.info(f"🗑️  Cleared {count} cookie files")
    
    def get_all_domains(self):
        """Get list of all domains with saved cookies"""
        
        domains = []
        for cookie_file in self.storage_dir.glob("*.json"):
            domain = cookie_file.stem.replace('_', '.')
            domains.append(domain)
        
        return domains
    
    def _get_cookie_file(self, domain):
        """Get cookie file path for domain"""
        safe_domain = domain.replace('.', '_').replace('/', '_')
        return self.storage_dir / f"{safe_domain}.json"

# utils/logger.py

"""
Logging Configuration
Sets up application logging to file and console
"""

import logging
import sys
from pathlib import Path


def setup_logging(log_file='data/app.log', level=logging.INFO):
    """
    Setup application logging
    
    Args:
        log_file: Path to log file
        level: Logging level
    """
    
    # Create logs directory
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # File handler
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Reduce noise from libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('selenium').setLevel(logging.WARNING)
    logging.getLogger('playwright').setLevel(logging.WARNING)
    
    logging.info("="*60)
    logging.info("Logging initialized")
    logging.info(f"Log file: {log_file}")
    logging.info(f"Level: {logging.getLevelName(level)}")
    logging.info("="*60)

# requirements.txt

# GUI
PyQt6==6.6.1

# Web Scraping - Core
requests==2.31.0
beautifulsoup4==4.12.3
lxml==5.1.0

# Web Scraping - Browsers
selenium==4.16.0
playwright==1.40.0

# Data Processing
pandas==2.1.4
openpyxl==3.1.2

# Utilities
python-dotenv==1.0.0

# Optional: Local LLM (experimental)
# ollama-python==0.1.7

# .gitignore

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# Environment Variables
.env

# Application Data
data/
!data/.gitkeep

# Logs
*.log

# OS
.DS_Store
Thumbs.db

# Playwright
.playwright/

# Temporary files
*.tmp
temp/

# 1. Clone or create project directory
mkdir smart_scraper
cd smart_scraper

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Install Playwright browsers
playwright install chromium

# 5. Configure environment
cp .env.example .env
# Edit .env and add your CLAUDE_API_KEY

# 6. Run the application
python main.py

# Features Overview
# Core Features
✅ Natural Language Queries

"Extract product names and prices"
"Get all email addresses and phone numbers"
"Find article titles, authors, and dates"

✅ Multiple Scraping Methods

Requests (fast, static sites)
Selenium (compatible, older sites)
Playwright (modern, JS-heavy sites)
Auto-detection of best method

✅ 4-Phase Cost Optimization

Cache check (instant, free)
Learned selectors (fast, free)
Simple extraction (fast, free)
LLM analysis (slower, costs money)

✅ Anti-Bot & Stealth Mode

Rate limiting
User agent rotation
Human behavior simulation
Session management
Cloudflare bypass

✅ CAPTCHA Handling

Manual solving (free)
API services (2Captcha, etc.)
Cookie reuse after solving

✅ Data Export

CSV (UTF-8 with BOM)
JSON (pretty-printed)
Excel (auto-sized columns)

# Cost Optimization Strategies
# Summary of All Strategies
python
1. ✅ Cache Everything
   └─ 7-day TTL, MD5 keying
   └─ Biggest saving!

2. ✅ Learn & Reuse Selectors
   └─ Per-domain CSS selector storage
   └─ One LLM call, infinite reuse

3. ✅ Minimize HTML
   └─ Remove scripts, styles, nav
   └─ Max 5000 chars to LLM
   └─ ~60% token reduction

4. ✅ Use Cheaper Models
   └─ Haiku for simple tasks (12x cheaper)
   └─ Sonnet only when needed

5. ✅ Batch Processing
   └─ Process multiple items in one call
   └─ 6x cost reduction

6. ✅ Local Extraction First
   └─ Regex patterns for common data
   └─ BeautifulSoup with common selectors
   └─ Free when successful

7. ✅ Budget Limiting
   └─ Daily spend cap
   └─ Warnings at 80%, 90%
   └─ Prevents surprises

8. ✅ Smart Retry Logic
   └─ Exponential backoff
   └─ Don't waste calls on transient errors

# Anti-Bot & Stealth Implementation
# Stealth Levels

python

OFF:
└─ Basic requests, no protection
└─ Use for: testing, friendly sites

LOW:
├─ Realistic User-Agent
├─ Basic headers
└─ Use for: public data sites

MEDIUM (Default):
├─ All LOW features
├─ Random delays (2-5s)
├─ Human-like scrolling
├─ Session cookies
└─ Use for: 90% of sites

HIGH:
├─ All MEDIUM features
├─ Mouse movement simulation
├─ User agent rotation
├─ Longer delays (5-10s)
├─ Viewport randomization
└─ Use for: protected sites

MAXIMUM:
├─ All HIGH features
├─ Very slow (10-20s delays)
├─ Residential proxies (future)
├─ Advanced fingerprint masking
└─ Use for: heavily protected sites

# Key Anti-Bot Features

1. Rate Limiting
python- Min delay: 2-5 seconds
- Max requests/min: 10
- Per-domain tracking
- Random jitter (±30%)
2. Human Behavior
python- Gradual scrolling
- Random mouse movements
- Realistic timing
- Occasional backtracking
3. Browser Fingerprinting
python- Hide webdriver property
- Mock plugins
- Realistic viewport
- Proper accept headers
4. Session Management
python- Persistent cookies
- Browser context reuse
- Realistic session duration

# CAPTCHA Handling
# Strategies

1. Manual Solving (Default)
Cost: Free
Time: 30-120 seconds
Success Rate: 100% (if user capable)

Process:
1. CAPTCHA detected
2. Pause scraping
3. Open browser window
4. User solves CAPTCHA
5. Save cookies
6. Continue scraping
7. Reuse cookies for rest!
2. API Services
Cost: $0.80-$3 per 1000
Time: 10-30 seconds
Success Rate: 95-99%

Services:
- 2Captcha: $2.99/1k
- Anti-Captcha: $1.50/1k
- CapMonster: $0.80/1k
3. Skip
Stop scraping when CAPTCHA encountered
Use for: optional scraping tasks
Cookie Reuse (Key Feature!)
Scenario: 1000 products, CAPTCHA on site

Without Cookie Reuse:
└─ Solve CAPTCHA 1000 times
└─ Time: 8+ hours
└─ Cost: $3 (if using API)

With Cookie Reuse:
└─ Solve CAPTCHA once
└─ Save cookies (24h lifetime)
└─ Reuse for all 1000 products
└─ Time: 1 minute (CAPTCHA) + 50 min (scraping)
└─ Cost: $0.003 (or free if manual)

# Development Roadmap

### Phase 1: MVP 

 Project structure
 Basic GUI with PyQt6
 Requests scraper
 Claude API integration
 Simple cache
 CSV export

### Phase 2: Core Features 

 Selenium + Playwright scrapers
 Learned selectors
 Budget management
 Progress tracking
 JSON/Excel export

### Phase 3: Anti-Bot 

 Stealth mode
 Rate limiting
 User agent rotation
 Behavior simulation
 Block detection

### Phase 4: CAPTCHA 

 CAPTCHA detection
 Manual solving
 Cookie management
 Cloudflare 
- [x] API solver integration
- [x] Session persistence

### Phase 5: Polish & Testing 
- [ ] Unit tests
- [ ] Integration tests
- [ ] Error handling refinement
- [ ] UI/UX improvements
- [ ] Documentation
- [ ] Performance optimization

### Future Enhancements
- [ ] Proxy support
- [ ] Local LLM integration (Ollama)
- [ ] Advanced scheduling
- [ ] Multi-language support
- [ ] Database storage option
- [ ] REST API mode
- [ ] Cloud deployment
- [ ] Browser extension

---

## Testing Strategy

### Test Sites
```python
# For Testing Different Scenarios

EASY (No Protection):
- https://books.toscrape.com/
- https://quotes.toscrape.com/
- Test: requests scraper, basic extraction

MEDIUM (Some JS):
- https://scrapethissite.com/
- Test: playwright, learned selectors

HARD (Cloudflare):
- https://nowsecure.nl/
- Test: stealth mode, cloudflare handler

CAPTCHA:
- https://www.google.com/recaptcha/api2/demo
- Test: manual solving, cookie reuse

# Unit Tests

# tests/test_scrapers.py

import unittest
from backend.scrapers.requests_scraper import RequestsScraper
from backend.scrapers.playwright_scraper import PlaywrightScraper


class TestScrapers(unittest.TestCase):
    
    def test_requests_scraper(self):
        """Test basic requests scraper"""
        scraper = RequestsScraper()
        html = scraper.scrape('https://example.com')
        self.assertIn('<html', html.lower())
        self.assertGreater(len(html), 100)
    
    def test_playwright_scraper(self):
        """Test Playwright scraper"""
        scraper = PlaywrightScraper()
        html = scraper.scrape('https://example.com')
        self.assertIn('<html', html.lower())
        self.assertGreater(len(html), 100)
    
    def test_method_detection(self):
        """Test auto method detection"""
        from backend.scraper_engine import ScraperEngine
        
        # Mock config
        config = {'CLAUDE_API_KEY': 'test'}
        engine = ScraperEngine(config)
        
        # Static site should use requests
        method = engine._detect_best_method('https://example.com')
        self.assertEqual(method, 'requests')


# tests/test_cache.py

import unittest
from backend.storage.cache_manager import CacheManager


class TestCache(unittest.TestCase):
    
    def setUp(self):
        self.cache = CacheManager(
            cache_file='data/test_cache.json',
            ttl_days=1,
            enabled=True
        )
    
    def test_cache_set_get(self):
        """Test cache set and get"""
        url = 'https://example.com'
        query = 'test query'
        data = {'field': 'value'}
        
        # Set
        self.cache.set(url, query, data)
        
        # Get
        result = self.cache.get(url, query)
        self.assertEqual(result, data)
    
    def test_cache_miss(self):
        """Test cache miss"""
        result = self.cache.get('https://nonexistent.com', 'query')
        self.assertIsNone(result)
    
    def tearDown(self):
        self.cache.clear()


# tests/test_llm.py

import unittest
from unittest.mock import Mock, patch
from backend.llm.claude_client import ClaudeClient


class TestLLM(unittest.TestCase):
    
    def setUp(self):
        self.client = ClaudeClient(api_key='test-key')
    
    def test_prompt_building(self):
        """Test prompt construction"""
        html = '<div>Test</div>'
        query = 'extract test'
        
        prompt = self.client._build_extraction_prompt(html, query)
        
        self.assertIn(query, prompt)
        self.assertIn(html, prompt)
        self.assertIn('JSON', prompt)
    
    def test_json_parsing(self):
        """Test JSON response parsing"""
        
        # Valid JSON
        response = '{"data": {"field": "value"}}'
        result = self.client._parse_response(response)
        self.assertEqual(result['data']['field'], 'value')
        
        # JSON with markdown
        response = '```json\n{"data": {"field": "value"}}\n```'
        result = self.client._parse_response(response)
        self.assertEqual(result['data']['field'], 'value')
    
    def test_cost_calculation(self):
        """Test cost calculation"""
        prompt = 'a' * 1000  # ~250 tokens
        response = 'b' * 1000  # ~250 tokens
        
        cost = self.client._calculate_cost(prompt, response)
        
        # Should be small but non-zero
        self.assertGreater(cost, 0)
        self.assertLess(cost, 0.01)


# Run tests
if __name__ == '__main__':
    unittest.main()

# Deployment
## Packaging

# Using PyInstaller to create standalone executable

# Install PyInstaller
pip install pyinstaller

# Create executable
pyinstaller --name="SmartScraper" \
            --windowed \
            --onefile \
            --icon=icon.ico \
            --add-data "frontend/styles:frontend/styles" \
            main.py

# Executable will be in dist/SmartScraper.exe    

# Troubleshooting Guide
Common Issues
1. "CLAUDE_API_KEY not found"
Solution:
1. Copy .env.example to .env
2. Add your API key from console.anthropic.com
3. Restart application

2. "Module 'playwright' not found"
Solution:
pip install playwright
playwright install chromium

3. "GUI doesn't start"
Solution:
- Check PyQt6 is installed: pip install PyQt6
- Try running with: python -m main
- Check logs in data/app.log

4. "Scraping is very slow"
Possible causes:
- Stealth level too high → Lower to medium
- Rate limiting too aggressive → Increase max_requests
- Site is genuinely slow → Normal
- CAPTCHA present → Check console

5. "Budget exceeded"
Solution:
- Increase daily budget in .env
- Enable caching (should be on by default)
- Check if selectors are being learned
- Verify cache is working (check data/llm_cache.json)

6. "CAPTCHA keeps appearing"
Solutions:
- Enable cookie saving (should be default)
- Check cookie lifetime (increase to 48h)
- Increase stealth level
- Use slower rate limiting
- Consider API solver for automation

7. "LLM returns invalid JSON"
Solution:
- This is handled automatically with retry
- Check logs for details
- May indicate HTML is too complex
- Try minimizing HTML more aggressively 

# License & Legal
# Usage Terms
# MIT License (Recommended)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND.

# Legal Disclaimer
⚠️  IMPORTANT LEGAL NOTICE:

Web scraping legality varies by jurisdiction and website.

YOU are responsible for:
✓ Checking robots.txt
✓ Reading Terms of Service
✓ Respecting rate limits
✓ Not scraping personal data without consent
✓ Not bypassing authentication
✓ Following GDPR/privacy laws

This tool is for:
✓ Publicly available data
✓ Research purposes
✓ Personal use
✓ With permission

NOT for:
✗ Copyright infringement
✗ Competitive intelligence without permission
✗ Personal data harvesting
✗ Bypassing paywalls
✗ Malicious activities

USE AT YOUR OWN RISK

# Getting help

1. Documentation
   └─ This file!
   └─ Code comments
   └─ Docstrings

2. Logs
   └─ Check data/app.log
   └─ Console output in GUI

3. Community
   └─ GitHub Issues (future)
   └─ Discord/Slack (future)

4. Commercial Support
   └─ Available for hire (future)

# Architecture
# #Component interaction
 
┌─────────────────────────────────────────────────────────────┐
│                        USER                                  │
│                          ↕                                   │
│                    [GUI - PyQt6]                             │
│                          ↕                                   │
│                  [Worker Thread]                             │
│                    (QThread)                                 │
│                          ↕                                   │
│                  [Scraper Engine]                            │
│                          ↕                                   │
│    ┌──────────────┬─────────────┬──────────────┐            │
│    ↓              ↓             ↓              ↓            │
│ [Scrapers]   [LLM Client]  [Storage]    [Stealth]          │
│    ↓              ↓             ↓              ↓            │
│ [Websites]  [Claude API]  [Files/JSON]  [Anti-Bot]         │
└─────────────────────────────────────────────────────────────┘

# Data Flow

INPUT: URL + Query
    ↓
[Cache Check] → HIT? → Return (€0.00, 0.001s)
    ↓ MISS
[Learned Selectors Check] → FOUND? → Extract → Return (€0.00, 0.1s)
    ↓ NOT FOUND
[Simple Extraction] → SUCCESS? → Return (€0.00, 0.2s)
    ↓ FAILED
[Fetch HTML]
    ↓
[Minimize HTML]
    ↓
[Call LLM API] (€0.003, 1-2s)
    ↓
[Parse Response]
    ↓
[Learn Selectors] → Save for future
    ↓
[Cache Result] → Save for 7 days
    ↓
OUTPUT: Structured Data

# Checklist 
✅ Project Overview
✅ Technology Stack
✅ Architecture Diagrams
✅ Complete Project Structure
✅ Core Code Implementations
✅ Configuration Files
✅ Installation Instructions
✅ Features Documentation
✅ Cost Optimization Strategies
✅ Anti-Bot Implementation
✅ CAPTCHA Handling
✅ Testing Strategy
✅ Deployment Guide
✅ Troubleshooting
✅ Performance Benchmarks
✅ Code Style Guide
✅ Future Roadmap
✅ Legal Disclaimer
✅ Example Usage