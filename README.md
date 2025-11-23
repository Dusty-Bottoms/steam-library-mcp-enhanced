# Steam Library MCP Server

A Model Context Protocol (MCP) server that provides access to your Steam game library data through Claude Desktop. It includes a helper script to copy your library data locally to a csv file for the MCP server to ingest. 

This repo was developed with Claude Code, and I left Claude's config in here for reference. This was built simply as a learning experience and an example of how to create an MCP server. 

## Features

### Core Library Features
- **Search Games**: Find games by name, genre, developer, publisher, review summary, or maturity rating
- **Filter Games**: Filter by playtime, review summary, or maturity rating  
- **Game Details**: Get comprehensive information about specific games
- **Review Analysis**: Detailed review statistics for games
- **Library Statistics**: Overview of your entire game library
- **Recently Played**: See what you've been playing lately
- **Recommendations**: Get game suggestions based on your playtime patterns

### Achievement Tracking
- **Achievement Data**: Per-game achievement tracking with unlock status
- **Achievement Stats**: Library-wide achievement completion statistics
- **Easy Achievements**: Find games with quick completions
- **Global Stats**: See how rare achievements are globally

### Community & Guides
- **Game Guides**: Search Steam Community guides by category
- **Guide Content**: Retrieve full guide text for detailed strategies
- **Achievement Guides**: Find achievement-specific guides
- **Game News**: Latest patches, updates, and announcements

### Social Features
- **Friends Activity**: See what friends are playing
- **Player Profiles**: View any player's public profile
- **Game Comparison**: Find shared games for multiplayer
- **Player Counts**: Current active players for games
- **Steam Level**: Track your level, XP, and badge progress

### 🆕 Phase 1: Strategic Intelligence (NEW!)
- **Achievement Roadmap**: Intelligent achievement progression planning
  - Prioritizes achievements by efficiency, rarity, and difficulty
  - Provides actionable next steps with guide links
  - Multiple sorting strategies (efficiency, completion, rarity)
  - Estimates time and difficulty for each achievement
  
- **Missable Content Scanner**: Proactive warning system
  - Detects time-sensitive or permanently missable achievements
  - Scans community guides for warning keywords
  - Alerts you before points of no return
  - Prevents accidental achievement locks
  
- **Session Context**: Smart session detection and guidance
  - Automatically detects your current/recent game
  - Provides comprehensive session context
  - Suggests next optimal achievement to pursue
  - Alerts for missable content in current game
  - Shows recent news and community activity

## Example Interactions using Claude Desktop (Click the dropdowns to see responses)

<details>
<summary>Suggest games based on recent play history<br><img src="images/recent_games_question.png"/></summary>
<br>
<img src="images/recent_games_answer.png" />
</details>

<details>
<summary>Suggest games based on review scores and age ratings<br><img src="images/game_suggestion_question.png"/></summary>
<br>
<img src="images/game_suggestion_answer.png" />
</details>

<details>
<summary>Generate a calendar timeline following several rules of games to share over time<br><img src="images/game_sharing_calendar_question.png"/></summary>
<br>
<img src="images/game_sharing_calendar_answer.png" />
</details>

## Prerequisites

- Python 3.8 or higher
- A Steam account with a public game library
- Steam API key (get one from https://steamcommunity.com/dev/apikey)
- Your Steam ID

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Fetch Your Steam Library Data

First, create a `.env` file with your Steam credentials:

```bash
# .env
STEAM_ID=your_steam_id_here
STEAM_API_KEY=your_steam_api_key_here
```

Then run the data fetcher:

```bash
python steam_library_fetcher.py
```

This will create a `steam_library.csv` file with all your game data.

### 3. Configure Claude Desktop

Copy the example configuration file and update the paths:

```bash
cp claude_desktop_config.example.json claude_desktop_config.json
```

Edit `claude_desktop_config.json` and update the paths to match your system:

```json
{
  "mcpServers": {
    "Steam Library": {
      "command": "/path/to/your/python",
      "args": ["/path/to/your/simple-steam-mcp/mcp_server.py"],
      "env": {}
    }
  }
}
```

Then copy it to Claude Desktop's configuration location:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux**: `~/.config/claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\claude\claude_desktop_config.json`

### 4. Test the Server

You can test the server directly:

```bash
python mcp_server.py
```

### 5. Restart Claude Desktop

After updating the configuration file, restart Claude Desktop to load the MCP server.

## Usage Examples

### Basic Library Queries
- "What are my top 10 most played games?"
- "Show me all my puzzle games" 
- "Find games with 'Very Positive' reviews that I haven't played yet"
- "What are some good games I should try based on what I've played?"
- "Show me details for Half-Life 2"
- "What games have I played recently?"
- "Give me statistics about my Steam library"

### Achievement Tracking
- "Show me all achievements for Brotato"
- "What's my achievement completion rate across all games?"
- "Find games with easy achievements I can complete quickly"
- "What's my rarest achievement unlock?"

### 🆕 Strategic Intelligence (Phase 1)
- **Smart Roadmaps**: "Create an achievement roadmap for Celeste sorted by efficiency"
- **Missable Detection**: "Are there any missable achievements in The Witcher 3?"
- **Session Context**: "What should I focus on in my current game?"
- **Proactive Guidance**: "What's the optimal next achievement for me to pursue?"
- **Risk Assessment**: "Scan Hollow Knight for time-sensitive content"

### Community & Social
- "Find achievement guides for Portal 2"
- "What are my friends currently playing?"
- "Which of my games can I play with [friend's name]?"
- "How many people are playing Baldur's Gate 3 right now?"

## Available Tools (23 Total)

### Library Management (7 tools)
1. **search_games**: Search by name, genre, developer, publisher, review summary, or maturity rating
2. **filter_games**: Filter by playtime thresholds, review summary, or maturity rating
3. **get_game_details**: Get comprehensive info about a specific game
4. **get_game_reviews**: Get detailed review statistics
5. **get_library_stats**: Overview statistics of your library
6. **get_recently_played**: Games played in the last 2 weeks
7. **get_recommendations**: Personalized suggestions based on your playtime

### Achievement Tracking (4 tools)
8. **get_game_achievements**: Per-game achievement tracking with unlock status
9. **get_achievement_stats**: Library-wide completion statistics
10. **find_easy_achievements**: Games with quick completions (≤20 achievements)
11. **get_global_achievement_stats**: Global rarity percentages

### Community Guides (3 tools)
12. **search_game_guides**: Find guides by category (Achievements, Gameplay, etc.)
13. **get_guide_content**: Retrieve full guide text
14. **find_achievement_guides**: Achievement-specific guide shortcut

### News & Social (6 tools)
15. **get_game_news**: Latest patches/updates/announcements
16. **get_friends_activity**: What friends are playing
17. **get_player_profile**: Any player's public profile
18. **compare_games_with_friend**: Find shared games for multiplayer
19. **get_game_player_count**: Current player count
20. **get_steam_level_progress**: Level, XP, badge progress

### 🆕 Strategic Intelligence - Phase 1 (3 tools)
21. **get_achievement_roadmap**: Intelligent achievement progression planning
    - Combines achievement data + rarity + guides
    - Multiple sorting strategies (efficiency, completion, rarity, missable)
    - Priority scoring algorithm
    - Actionable next steps with time estimates
    
22. **scan_for_missable_content**: Proactive missable achievement detection
    - Keyword pattern matching in guides
    - Achievement description analysis
    - Warning context extraction
    - Urgency assessment
    
23. **get_current_session_context**: Smart session detection and guidance
    - Detects active/recent game automatically
    - Comprehensive context (achievements, missables, news, players)
    - Suggests optimal next achievement
    - Proactive alerts and recommendations

## Data Source

The server reads from `steam_library.csv` which should contain columns:
- appid, name, maturity_rating, review_summary, review_score, total_reviews
- positive_reviews, negative_reviews, genres, categories, developers, publishers
- release_date, playtime_forever, playtime_2weeks, rtime_last_played

## Troubleshooting

1. **Server not connecting**: Check that the path in your Claude Desktop config is correct
2. **CSV not found**: Ensure `steam_library.csv` is in the same directory as the server script
3. **Permission errors**: Make sure Python has read access to the CSV file
4. **Port conflicts**: The server uses port 8000 by default - ensure it's available

## Technical Details

- Built using the official MCP Python SDK (FastMCP)
- Pandas for efficient CSV data processing
- Runs via STDIO transport for Claude Desktop integration
- 23 total tools across 5 functional categories

### Phase 1 Architecture: From Reactive to Proactive

The Phase 1 enhancements transform the server from a **data provider** into a **strategic advisor** by adding an intelligence layer that synthesizes multiple data sources:

**Data Flow**:
```
User Query
    ↓
CSV Lookup (instant) → Game metadata
    ↓
Steam API Calls (200ms each)
    ├→ Achievement schema & progress
    ├→ Global rarity percentages
    └→ Community guide content
    ↓
Intelligence Layer (NEW)
    ├→ Priority scoring algorithm
    ├→ Missable content detection
    └→ Context-aware recommendations
```

**Key Design Decisions**:
- **Resilient synthesis**: Each data source is optional; tools return partial results if APIs fail
- **Smart caching**: Guide content cached in-memory (planned for Phase 2)
- **Priority algorithm**: Balances rarity (30%), difficulty (40%), and guide availability (30%)
- **Missable detection**: Regex pattern matching with 11 keyword patterns
- **Session detection**: Uses 2-week playtime as proxy for active session

**Future Phases** (from research paper):
- **Phase 2**: ✅ COMPLETE - Performance optimizations (caching, parallel execution)
- **Phase 3.5**: 📋 PLANNED - Video intelligence layer (YouTube transcript analysis)
- **Phase 4**: Save file analysis for game state understanding  
- **Phase 5**: Full multi-modal intelligence (screenshots, real-time screen capture)
- **Phase 6**: Predictive modeling for player behavior

### Phase 3.5: Video Intelligence Layer (Next Up!)

**Purpose**: Bridge text guides and visual walkthroughs via YouTube MCP integration

**New Capabilities**:
- Search YouTube for achievement-specific video guides
- Extract and analyze video transcripts for missable warnings
- Provide timestamp-specific guidance ("solution at 14:35")
- Cross-validate text and video sources for higher confidence
- Auto-recommend video vs. text based on task complexity (spatial puzzles = video)

**Research Paper Reference**: Section 5 - "Visual Intelligence: Video Walkthroughs and Transcript Extraction"

See `PHASE3.5_PLAN.md` for detailed implementation guide.