# Content Automation

AI-powered content generation system with automatic web research.

## Table of Contents

1. [Requirements](#requirements)
2. [Installation](#installation)
3. [API Keys Configuration](#api-keys-configuration)
4. [Usage](#usage)
5. [Project Structure](#project-structure)
6. [How It Works](#how-it-works)
7. [Troubleshooting](#troubleshooting)

---

## Requirements

### Required Software

| Software | Min Version | Description |
|----------|-------------|-------------|
| Python | 3.8+ | Programming language |
| Git | 2.0+ | Version control |
| pip | 21.0+ | Python package manager |

### Verify Installation

```bash
# Verify Python
python --version

# Verify pip
pip --version

# Verify Git
git --version
```

---

## Installation

### Step 1: Clone the Repository

```bash
git clone https://github.com/Bobiptus/ai-content-generator.git
cd ai-content-generator
```

### Step 2: Create Virtual Environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate
```

**Windows (CMD):**
```cmd
python -m venv venv
venv\Scripts\activate
```

**Linux / MacOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Update pip (Recommended)

```bash
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Verify Installation

```bash
# Verify that libraries are installed
pip list
```

You should see:
- google-generativeai
- python-dotenv
- requests
- beautifulsoup4
- groq
- tavily
- httpx

---

## API Keys Configuration

### Important

**Each user must create their own `.env` file with their personal API keys.** The `.env` file contains private keys and **should NOT** be shared.

### Step 1: Copy Example File

**Windows:**
```bash
copy .env.example .env
```

**Linux / MacOS:**
```bash
cp .env.example .env
```

### Step 2: Get API Keys

#### GROQ_API_KEY (Required)

Groq offers free access to high-quality LLM models.

1. Go to https://console.groq.com
2. Create an account or sign in
3. Go to "API Keys"
4. Create a new API Key
5. Copy the key and paste it into `.env`

**Location in .env:**
```
GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxx
```

#### TAVILY_API_KEY (Required for web research)

Tavily offers 1000 searches/month free.

1. Go to https://tavily.com
2. Create an account or sign in
3. Go to your profile or API section
4. Copy your API Key
5. Paste it into `.env`

**Location in .env:**
```
TAVILY_API_KEY=tvly-xxxxxxxxxxxxxxxx
```

#### GOOGLE_API_KEY (Optional)

Only needed if you want to use Google Gemini as an alternative provider.

1. Go to https://aistudio.google.com/app/apikey
2. Create a new API Key
3. Copy and paste into `.env`

**Location in .env:**
```
GOOGLE_API_KEY=AIzaxxxxxxxxxxxxxxxx
```

### Step 3: Final .env Structure

Your `.env` file should look like this:

```env
GROQ_API_KEY=your_groq_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
GOOGLE_API_KEY=your_google_api_key_here  # Optional
```

---

## Usage

### Run the Program

```bash
python generate_article.py
```

### User Interface

The program will guide you step by step:

```
======================================================================
📰 AI-POWERED COMPLETE ARTICLE GENERATOR
======================================================================

🔧 Initializing system...
✅ Using Groq API (Llama 3.3 70B)
✅ System ready (with web research)

📝 Article configuration:
----------------------------------------------------------------------
Article topic: [ENTER YOUR TOPIC]
```

### Options During Execution

1. **Article topic:** Enter the topic you want to generate content about

2. **Web research:**
   - `1` = Yes (recommended - uses updated information from the web)
   - `2` = No (uses only the LLM model's knowledge)

3. **Article tone:**
   - `1` = Professional (formal and technical language)
   - `2` = Casual (friendly and conversational language)
   - `3` = Technical (specialized terminology)

### Output

Generated articles are automatically saved to:
- `outputs/article_[topic]_[date].md` (Markdown)
- `outputs/article_[topic]_[date].txt` (Plain text)

---

## Project Structure

```
ai-content-generator/
├── .env                    # Environment variables (DO NOT upload to git)
├── .env.example            # Configuration template
├── .gitignore             # Ignored files by git
├── README.md              # This file
├── requirements.txt        # Python dependencies
├── generate_article.py    # Main script
├── main.py                # Alternative script (basic outline)
├── src/
│   ├── agents/
│   │   ├── research_agent.py      # Web search agent
│   │   └── content_generator.py  # Article generator
│   ├── services/
│   │   └── cache_service.py      # Cache with 24h TTL
│   └── utils/
│       └── __init__.py
└── outputs/                       # Generated articles
    ├── article_[topic]_[date].md
    └── article_[topic]_[date].txt
```

---

## How It Works

### Execution Flow

```
┌─────────────────┐
│ User            │
│ (enters topic) │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ ContentGenerator│
└────────┬────────┘
         │
         ▼ (if research enabled)
┌─────────────────┐     ┌──────────────────┐
│ ResearchAgent   │────▶│ Tavily API       │
│ (web search)   │     │ (web summaries)  │
└────────┬────────┘     └──────────────────┘
         │
         ▼ (results + cache)
┌─────────────────┐
│ LLM (Groq)     │
│ + information   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Outline         │
│ + Introduction  │
│ + Sections      │
│ + Conclusion    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ .md file        │
│ + .txt          │
└─────────────────┘
```

### Components

#### 1. ResearchAgent
- Performs web searches using Tavily
- Extracts relevant information about the topic
- Saves results in cache for 24 hours
- Avoids repeated searches for the same topic

#### 2. ContentGenerator
- Generates structured article outline
- Writes engaging introduction
- Develops each section with substantial content
- Creates conclusion with call to action

#### 3. CacheService
- Stores search results
- TTL (Time To Live) of 24 hours
- Avoids unnecessary API consumption
- Improves execution speed

### Supported LLM Providers

| Provider | Model | Status | Notes |
|----------|-------|--------|-------|
| Groq | Llama 3.3 70B | ✅ Default | Fast and free |
| Google | Gemini 2.5 Flash | ✅ Optional | Requires API key |

---

## Troubleshooting

### Error: "No module named 'dotenv'"

**Cause:** Dependencies were not installed correctly.

**Solution:**
```bash
pip install python-dotenv
```

### Error: "GROQ_API_KEY not found"

**Cause:** Missing API key in the `.env` file.

**Solution:**
1. Verify that the `.env` file exists
2. Make sure the `GROQ_API_KEY=...` line is present
3. Verify that the API key is correct

### Error: "Tavily not installed"

**Cause:** The tavily library is not installed.

**Solution:**
```bash
pip install tavily>=1.0.0
```

### Error: "Rate limit exceeded"

**Cause:** You have exceeded the API limits.

**Solution:**
- Wait 1 minute for Groq
- For Tavily: wait until next month (1000 searches/month free)

### Error: "venv\Scripts\Activate not recognized"

**Cause:** You are using PowerShell with restricted execution policy.

**Solution:**
```powershell
# Option 1: Switch to CMD
cmd /k venv\Scripts\activate.bat

# Option 2: Enable scripts in PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### The program doesn't respond

**Cause:** Content generation can take 30-90 seconds.

**Solution:**
- Be patient, it's normal
- Verify your internet connection

### Verify API Configuration

You can test that APIs are configured correctly:

```bash
# Test Groq
python -c "from groq import Groq; print('Groq OK')"

# Test Tavily
python -c "from tavily import TavilyClient; print('Tavily OK')"
```

---

## Project Update

To get the latest version:

```bash
git pull origin main
```

---

## License

MIT

---

## Contributions

Contributions are welcome. Please fork the repository and submit a pull request.

---

## Support

If you have problems:
1. Review the [Troubleshooting](#troubleshooting) section
2. Search in GitHub issues
3. Create a new issue if you can't find a solution
