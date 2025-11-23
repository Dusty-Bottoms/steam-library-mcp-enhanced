# Research Paper: YouTube MCP Integration Reference

## Section 5: Visual Intelligence: Video Walkthroughs and Transcript Extraction

**Key Points from Research Paper:**

### 5.1 Transcript Extraction Mechanics
- Servers: `jkawamoto/mcp-youtube-transcript` and `sinjab/mcp_youtube_extract`
- Uses libraries like `youtube-transcript-api` or `yt-dlp`
- Extracts hidden caption tracks (XML/SRT data) from video IDs
- Quality depends on manual vs. auto-generated captions

### 5.2 Strategic Application: Timestamped Guidance

**Primary Utility**: Temporal Navigation

**Workflow Example:**
1. User Query: "How do I solve the mirror puzzle in Uncharted?"
2. Agent Search: Finds relevant YouTube video
3. MCP Call: `get_transcript(video_url)`
4. Analysis: Agent scans transcript for keywords like "mirror," "light beam," "puzzle"
5. Result: "The mirror puzzle solution starts at timestamp 14:20. The guide suggests rotating the central pillar twice."

**Integration with Steam Library Server:**

The research paper describes this as part of the **"Completionist" workflow**:

### Scenario A: The Completionist (Elden Ring)

**Step 5: Visual Guide (youtube-mcp)**
- Agent searches YouTube for "Bolt of Gransax location"
- Fetches transcript
- Tells user: "Go to the Leyndell giant spear statue. The path is shown at timestamp 3:45."

This integrates with:
- **Steam MCP**: State verification (what's unlocked)
- **MediaWiki MCP**: Knowledge retrieval (what's needed)
- **YouTube MCP**: Visual guidance (how to get it)

---

## Implementation Priority

According to the research paper, this should be **Phase 3.5** or **Phase 4**:

**Phase 4: Multi-Modal Intelligence**
- Screenshot analysis
- **Video processing**
- Voice commands
- Predictive modeling
- Advanced AI integration

---

## Technical Integration Points

### Current Gap in Steam Library Server

**What We Have:**
- Steam achievement tracking ✅
- Community text guide scanning (MediaWiki-style) ✅
- Guide URL linking ✅

**What We're Missing:**
- YouTube video search integration ❌
- Transcript extraction and analysis ❌
- Timestamp-based guidance ❌
- Cross-reference between text guides and video guides ❌

### Proposed Enhancement: Phase 3.5

**New Tool**: `find_achievement_video_guides(game_identifier, achievement_name)`

**Workflow:**
1. Search YouTube for "{game_name} {achievement_name} guide"
2. Extract transcripts from top 3-5 results
3. Scan transcripts for achievement-specific keywords
4. Identify key timestamps
5. Return structured guidance with video URLs and timestamps

**Integration with Existing Tools:**
- `get_achievement_roadmap()` could include video guide links
- `scan_for_missable_content()` could analyze video transcripts for "missable" warnings
- `get_current_session_context()` could suggest relevant video guides

---

## YouTube MCP Servers Referenced

1. **jkawamoto/mcp-youtube-transcript**
   - Primary transcript extraction
   - Clean API for video ID → transcript

2. **sinjab/mcp_youtube_extract**
   - Alternative implementation
   - May have different caption quality handling

---

## Next Steps for Integration

### Phase 3.5: Video Intelligence Layer (Planned)

**Components:**
1. YouTube MCP client integration
2. Transcript search and analysis
3. Timestamp extraction
4. Cross-reference with text guides
5. Visual cue detection in narration

**Estimated Effort**: 8-10 hours

**Dependencies:**
- YouTube Data API v3 key
- MCP YouTube server installation
- Transcript analysis algorithms

