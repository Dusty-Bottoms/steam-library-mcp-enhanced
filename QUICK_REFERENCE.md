# Phase 1 Tools - Quick Reference

## 🎯 get_achievement_roadmap()

**Use when**: You want an optimized achievement completion plan

**Syntax**:
```
get_achievement_roadmap(game_identifier, sort_by="efficiency")
```

**Parameters**:
- `game_identifier`: Game name or appid
- `sort_by`: `"efficiency"` | `"completion"` | `"rarity"` | `"missable"`

**Returns**: Top 10 prioritized achievements with:
- Priority score (0-1)
- Rarity percentage
- Difficulty estimate
- Guide availability
- Time estimate
- Next steps

**Example Usage**:
```
"Create an achievement roadmap for Celeste"
"Give me the easiest achievements for Hollow Knight"
"Show me rare achievements for Brotato I should prioritize"
```

**Best for**:
- Completionists wanting optimal paths
- Players stuck on what to do next
- Achievement hunters maximizing value

---

## ⚠️ scan_for_missable_content()

**Use when**: You want to avoid permanently missing achievements

**Syntax**:
```
scan_for_missable_content(game_identifier)
```

**Parameters**:
- `game_identifier`: Game name or appid

**Returns**: 
- Missable achievement count
- Guide warnings with context
- Achievement description warnings
- Urgency assessment

**Example Usage**:
```
"Are there missable achievements in The Witcher 3?"
"Scan Hollow Knight for time-sensitive content"
"Check if I can miss anything in Persona 5"
```

**Best for**:
- Story-driven games with choices
- Games with multiple endings
- First playthroughs of narrative games

**Detection Patterns**:
- "missable", "point of no return"
- "before chapter X", "limited time"
- "one chance", "can't go back"
- "permanently locked", "story choice"

---

## 🎮 get_current_session_context()

**Use when**: You want comprehensive info about your active game

**Syntax**:
```
get_current_session_context()
```

**Parameters**: None (auto-detects from recent play)

**Returns**:
- Current/recent game name
- Playtime statistics
- Achievement progress percentage
- Missable content alerts
- Suggested next achievement
- Recent news/updates
- Current player count

**Example Usage**:
```
"What should I focus on right now?"
"Give me context for my current game"
"What's my progress in the game I'm playing?"
```

**Best for**:
- Quick session briefs
- "What next?" guidance
- Progress tracking
- Staying informed

---

## 📊 Priority Score Algorithm

**How achievements are scored** (0.0 - 1.0):

```
Priority = (Rarity × 0.3) + (Difficulty × 0.4) + (Guide × 0.3)

If missable: Priority × 3
```

**Factors**:
- **Rarity** (30%): Rarer = higher score (inverted)
- **Difficulty** (40%): Easier = higher score
  - Easy: 1.0
  - Medium: 0.7
  - Hard: 0.4
  - Very Hard: 0.2
- **Guide Availability** (30%): Has guide = +0.2 bonus
- **Missable Multiplier**: 3x if time-sensitive

**Why this works**:
- Prioritizes achievable challenges (40% difficulty weight)
- Values rare achievements (30% rarity weight)
- Reduces frustration (30% guide weight)
- Urgently flags missables (3x multiplier)

---

## 🔄 Sorting Strategies

### `efficiency` (Default)
**Best for**: Balanced players  
**Prioritizes**: High value/effort ratio  
**Logic**: Rare + easy + has guide = top priority

### `completion`
**Best for**: 100% completionists  
**Prioritizes**: Easiest first  
**Logic**: High rarity% (common achievements) first

### `rarity`
**Best for**: Achievement collectors  
**Prioritizes**: Rarest first  
**Logic**: Low rarity% (rare achievements) first

### `missable`
**Best for**: First playthroughs  
**Prioritizes**: Time-sensitive first  
**Logic**: Same as efficiency (will improve in Phase 2)

---

## 💡 Pro Tips

### Achievement Roadmaps
- Use `efficiency` for general gameplay
- Switch to `completion` when going for 100%
- Use `rarity` to show off rare achievements
- Check guides for complex achievements

### Missable Content
- **Always scan story-driven games first**
- Pay attention to "before chapter X" warnings
- Bookmark missable guides for reference
- Check before major story decisions

### Session Context
- Use at start of each gaming session
- Great for "what was I doing?" moments
- Helps maintain momentum in games
- Combines everything you need to know

---

## 🎮 Real-World Scenarios

### Scenario 1: New Game
```
1. "Scan [game] for missable achievements"
2. Bookmark any warnings
3. "Create achievement roadmap for [game] sorted by completion"
4. Play naturally, checking roadmap periodically
```

### Scenario 2: Stuck on Progress
```
1. "What should I focus on right now?"
2. Review suggested achievement
3. "Show me achievement guides for [game]"
4. Follow guide for suggested achievement
```

### Scenario 3: Achievement Hunting
```
1. "Create achievement roadmap for [game] sorted by efficiency"
2. Focus on top 3 priority achievements
3. Complete, then refresh roadmap
4. Repeat until 100%
```

### Scenario 4: Completionist Run
```
1. "Scan [game] for missable achievements"
2. Handle missables first
3. "Create achievement roadmap sorted by completion"
4. Work through easiest to hardest
```

---

## ⚡ Performance Notes

**Response Times** (approximate):
- `get_achievement_roadmap()`: 600-1000ms
- `scan_for_missable_content()`: 400-1400ms  
- `get_current_session_context()`: 2000-3000ms

**API Calls per Tool**:
- Roadmap: 3-4 calls
- Missable scan: 2-7 calls (depends on guides)
- Session context: 6-8 calls

**Tip**: Session context is slower but most comprehensive. Use when you have time for a full brief.

---

## 🐛 Troubleshooting

**"No achievements found"**
- Check game name spelling
- Try appid instead of name
- Game might not have achievements

**"No missable content detected"**
- Game might not have missables (roguelikes, etc.)
- No community guides available yet
- Detection is probabilistic, not perfect

**"No recent activity"**
- Haven't played any games in 2 weeks
- Steam privacy settings block data
- CSV data needs refresh

**Slow responses**
- Normal for context (6-8 API calls)
- Steam API might be slow
- Phase 2 will add caching

---

## 📚 Related Tools

**Achievement Tools**:
- `get_game_achievements()` - Raw achievement data
- `get_achievement_stats()` - Library-wide stats
- `find_easy_achievements()` - Games with ≤20 achievements
- `get_global_achievement_stats()` - Rarity percentages

**Guide Tools**:
- `search_game_guides()` - Browse all guides
- `get_guide_content()` - Read full guide
- `find_achievement_guides()` - Achievement-specific

**These Phase 1 tools synthesize the above into actionable intelligence**

---

## 🔮 Coming in Phase 2

- **Caching**: 15-min TTL = 5x faster responses
- **Parallel API calls**: Cut session context time in half
- **Rate limiting**: Better handling of API limits
- **Enhanced missable detection**: ML-based pattern recognition
- **Dependency chains**: "Unlock X before Y"
- **Difficulty ML model**: Better time/difficulty estimates

---

## 📖 Full Documentation

- `PHASE1_SUMMARY.md` - Complete implementation details
- `README.md` - General usage and setup
- `mcp_server.py` - Source code (lines 986-1406)
