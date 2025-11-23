# Phase 3.5: Video Intelligence Layer - Implementation Plan

**Based on Research Paper Section 5: Visual Intelligence**

**Status**: 📋 Planning  
**Priority**: High (Critical gap in multi-modal intelligence)  
**Estimated Effort**: 8-10 hours  
**Dependencies**: YouTube Data API v3, YouTube MCP Server

---

## Executive Summary

Phase 3.5 bridges the gap between **text-based guides** (Phase 1) and **visual walkthroughs** by integrating YouTube transcript analysis. This transforms the Steam Library MCP Server from a text-only intelligence system into a true **multi-modal gaming co-pilot**.

### The Problem

**Current State:**
- ✅ We can scan Steam Community text guides
- ✅ We can detect missable achievements in written guides
- ❌ We **cannot** analyze YouTube video guides (the dominant format for modern gaming)
- ❌ We **cannot** provide timestamp-specific guidance
- ❌ We miss visual-only instructions that text guides omit

**Research Paper Insight:**
> "For many complex spatial puzzles or boss fights, a text description is inferior to a visual demonstration."

---

## Architecture: Multi-Source Guide Intelligence

### Data Flow

```
User Query: "How do I get the Bolt of Gransax?"
    │
    ▼
┌─────────────────────────────────────────────────────────────┐
│           Steam Library MCP Server (Phase 3.5)               │
│                                                               │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Steam API  │  │  Community   │  │   YouTube    │      │
│  │ (Achievement │  │ Text Guides  │  │Video Guides  │      │
│  │    State)    │  │  (Phase 1)   │  │ (Phase 3.5)  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│          │                │                    │              │
│          ▼                ▼                    ▼              │
│  ┌────────────────────────────────────────────────────────┐ │
│  │         Intelligence Synthesis Engine                   │ │
│  │  • Detect locked achievement                           │ │
│  │  • Check text guides for location                       │ │
│  │  • Search YouTube for video walkthrough                 │ │
│  │  • Extract transcript and find timestamp                │ │
│  │  • Cross-reference text + video for completeness        │ │
│  └────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
    │
    ▼
Response: "Bolt of Gransax is in Leyndell. Text guide says 'giant spear statue.'
Video guide (PowerPyx, 14:35) shows exact climbing path. WARNING: Missable after Maliketh!"
```

---

## New Tools

### 1. `find_achievement_video_guides(game_identifier, achievement_name)`

**Purpose**: Search YouTube for achievement-specific video guides

**Parameters**:
- `game_identifier`: Game name or appid
- `achievement_name`: Specific achievement to find (optional)
- `max_results`: Number of videos to analyze (default: 3)

**Returns**:
```json
{
  "game": "Elden Ring",
  "achievement": "Legendary Armaments",
  "videos": [
    {
      "title": "All 9 Legendary Weapons Locations",
      "channel": "PowerPyx",
      "video_id": "abc123",
      "url": "https://youtube.com/watch?v=abc123",
      "duration": "12:45",
      "relevance_score": 0.95,
      "has_transcript": true,
      "key_timestamps": [
        {
          "time": "2:15",
          "weapon": "Bolt of Gransax",
          "context": "Leyndell capital, giant spear statue"
        },
        {
          "time": "5:30",
          "weapon": "Eclipse Shotel",
          "context": "Castle Sol, behind the boss arena"
        }
      ]
    }
  ]
}
```

**Integration Points**:
- Called by `get_achievement_roadmap()` to enrich with video guides
- Called by `scan_for_missable_content()` to check video warnings
- Called by `get_current_session_context()` for active game guidance

---

### 2. `analyze_video_guide(video_url, keywords)`

**Purpose**: Deep analysis of a specific video guide

**Parameters**:
- `video_url`: Full YouTube URL or video ID
- `keywords`: List of terms to search for in transcript (e.g., ["missable", "before boss"])

**Returns**:
```json
{
  "video_id": "abc123",
  "title": "Elden Ring - Missable Items Guide",
  "transcript_available": true,
  "transcript_quality": "manual",  // or "auto-generated"
  "duration": "15:42",
  "keyword_matches": [
    {
      "keyword": "missable",
      "occurrences": 7,
      "timestamps": ["1:20", "3:45", "7:10", "9:30", "11:05", "13:20", "14:55"]
    },
    {
      "keyword": "before boss",
      "occurrences": 3,
      "timestamps": ["3:45", "9:30", "13:20"]
    }
  ],
  "context_windows": [
    {
      "timestamp": "3:45",
      "text": "...this item is missable you have to get it before the boss fight or you'll lock yourself out of this area permanently...",
      "relevance": "high"
    }
  ],
  "warnings_detected": [
    "Point of no return detected at 3:45",
    "Limited time content mentioned at 9:30",
    "Permanently missable item at 13:20"
  ]
}
```

---

### 3. `get_video_transcript(video_id)`

**Purpose**: Raw transcript extraction (thin wrapper around YouTube MCP)

**Parameters**:
- `video_id`: YouTube video ID

**Returns**:
```json
{
  "video_id": "abc123",
  "title": "Video Title",
  "transcript": [
    {"start": 0.0, "duration": 3.5, "text": "Hey guys, welcome back"},
    {"start": 3.5, "duration": 4.2, "text": "Today we're going to find the Bolt of Gransax"},
    {"start": 7.7, "duration": 5.8, "text": "This is a missable weapon so pay attention"}
  ],
  "full_text": "Hey guys, welcome back. Today we're going to find the Bolt of Gransax. This is a missable weapon so pay attention...",
  "language": "en",
  "quality": "manual"
}
```

---

## Enhanced Existing Tools

### `get_achievement_roadmap()` Enhancement

**Before (Phase 2.1)**:
```json
{
  "roadmap": [
    {
      "name": "Legendary Armaments",
      "has_guide": true,
      "guide_url": "https://steamcommunity.com/..."
    }
  ]
}
```

**After (Phase 3.5)**:
```json
{
  "roadmap": [
    {
      "name": "Legendary Armaments",
      "text_guides": [
        {
          "type": "steam_community",
          "url": "https://steamcommunity.com/...",
          "title": "All Legendary Weapons"
        }
      ],
      "video_guides": [
        {
          "type": "youtube",
          "url": "https://youtube.com/watch?v=abc123",
          "channel": "PowerPyx",
          "key_timestamps": ["2:15", "5:30", "8:45"],
          "missable_warnings": 2
        }
      ],
      "recommended_guide": "video",  // "text" or "video" based on complexity
      "complexity": "spatial_puzzle"  // video better for spatial tasks
    }
  ]
}
```

---

### `scan_for_missable_content()` Enhancement

**New Data Source**: Video transcripts

**Current (Phase 2.1)**:
- Scans 5 Steam Community text guides
- Uses 11 regex patterns

**Enhanced (Phase 3.5)**:
- Scans 5 Steam Community text guides
- Scans top 3 YouTube video transcripts
- Cross-references both sources
- Confidence scoring: "High" if both text and video warn, "Medium" if only one

**Example Output**:
```json
{
  "missable_warnings": [
    {
      "type": "cross_validated",
      "confidence": "high",
      "achievement": "Bolt of Gransax",
      "text_source": {
        "guide": "Fextralife Wiki",
        "warning": "Must be obtained before defeating Maliketh"
      },
      "video_source": {
        "video": "PowerPyx Walkthrough",
        "timestamp": "14:35",
        "warning": "Cannot return to this area after the boss"
      },
      "urgency": "critical"
    }
  ]
}
```

---

## Implementation Steps

### Step 1: YouTube MCP Server Installation (1 hour)

**Install YouTube transcript MCP**:
```bash
# Option 1: jkawamoto/mcp-youtube-transcript (recommended)
npm install -g @jkawamoto/mcp-youtube-transcript

# Option 2: sinjab/mcp_youtube_extract
pip install mcp-youtube-extract
```

**Configure in OpenCode/Claude Desktop**:
```json
{
  "mcpServers": {
    "youtube-transcript": {
      "command": "npx",
      "args": ["-y", "@jkawamoto/mcp-youtube-transcript"]
    }
  }
}
```

---

### Step 2: YouTube Data API Integration (2 hours)

**Get API Key**:
1. Go to Google Cloud Console
2. Enable YouTube Data API v3
3. Create API key
4. Add to `.env`: `YOUTUBE_API_KEY=your_key_here`

**Create YouTube client wrapper** in `mcp_server.py`:
```python
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

def search_youtube_guides(game_name: str, query: str, max_results: int = 3):
    """Search YouTube for game guides"""
    youtube = googleapiclient.discovery.build(
        'youtube', 'v3', developerKey=YOUTUBE_API_KEY
    )
    
    search_query = f"{game_name} {query} guide"
    request = youtube.search().list(
        q=search_query,
        part='snippet',
        type='video',
        maxResults=max_results,
        order='relevance'
    )
    
    response = request.execute()
    return response['items']

def get_video_transcript(video_id: str) -> List[Dict]:
    """Fetch transcript for YouTube video"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        return transcript
    except Exception as e:
        # Try auto-generated captions
        try:
            transcript = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=['en']
            )
            return transcript
        except:
            return None
```

---

### Step 3: Transcript Analysis Engine (3 hours)

**Create transcript analyzer**:
```python
def analyze_transcript_for_keywords(
    transcript: List[Dict],
    keywords: List[str],
    context_window: int = 50
) -> Dict[str, Any]:
    """
    Analyze transcript for specific keywords
    Returns timestamps and context windows
    """
    full_text = " ".join([entry['text'] for entry in transcript])
    
    matches = {}
    for keyword in keywords:
        pattern = re.compile(rf'\b{keyword}\b', re.IGNORECASE)
        
        # Find all occurrences
        keyword_matches = []
        for entry in transcript:
            if pattern.search(entry['text']):
                timestamp = format_timestamp(entry['start'])
                context = extract_context(full_text, entry['text'], context_window)
                keyword_matches.append({
                    'timestamp': timestamp,
                    'context': context,
                    'relevance': calculate_relevance(context, keyword)
                })
        
        matches[keyword] = keyword_matches
    
    return matches

def format_timestamp(seconds: float) -> str:
    """Convert seconds to MM:SS format"""
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes}:{secs:02d}"

def extract_context(full_text: str, match_text: str, window: int) -> str:
    """Extract context window around match"""
    start = full_text.find(match_text)
    if start == -1:
        return ""
    
    context_start = max(0, start - window)
    context_end = min(len(full_text), start + len(match_text) + window)
    
    return full_text[context_start:context_end].strip()
```

---

### Step 4: Tool Implementation (2 hours)

**Implement new MCP tools**:
```python
@mcp.tool
def find_achievement_video_guides(
    game_identifier: Annotated[str, "Game name or appid"],
    achievement_name: Annotated[str, "Specific achievement name (optional)"] = None,
    max_results: Annotated[int, "Number of videos to analyze"] = 3
) -> Dict[str, Any]:
    """Search YouTube for achievement-specific video guides with transcript analysis"""
    
    # Get game name
    game_name = resolve_game_name(game_identifier)
    
    # Build search query
    search_query = achievement_name if achievement_name else "all achievements"
    
    # Search YouTube
    videos = search_youtube_guides(game_name, search_query, max_results)
    
    # Analyze each video
    analyzed_videos = []
    for video in videos:
        video_id = video['id']['videoId']
        
        # Get transcript
        transcript = get_video_transcript(video_id)
        if not transcript:
            continue
        
        # Analyze for achievement keywords
        keywords = [achievement_name] if achievement_name else ['achievement', 'unlock', 'trophy']
        analysis = analyze_transcript_for_keywords(transcript, keywords)
        
        analyzed_videos.append({
            'title': video['snippet']['title'],
            'channel': video['snippet']['channelTitle'],
            'video_id': video_id,
            'url': f"https://youtube.com/watch?v={video_id}",
            'has_transcript': True,
            'key_timestamps': extract_key_timestamps(analysis),
            'relevance_score': calculate_video_relevance(analysis, achievement_name)
        })
    
    return {
        'game': game_name,
        'achievement': achievement_name,
        'videos': analyzed_videos
    }

@mcp.tool
def analyze_video_guide(
    video_url: Annotated[str, "YouTube video URL or ID"],
    keywords: Annotated[List[str], "Keywords to search for"] = None
) -> Dict[str, Any]:
    """Deep analysis of a specific YouTube guide video"""
    
    # Extract video ID
    video_id = extract_video_id(video_url)
    
    # Get transcript
    transcript = get_video_transcript(video_id)
    if not transcript:
        return {'error': 'Transcript not available'}
    
    # Default keywords for missable detection
    if not keywords:
        keywords = [
            'missable', 'point of no return', 'before boss',
            'limited time', 'one chance', 'permanently'
        ]
    
    # Analyze
    analysis = analyze_transcript_for_keywords(transcript, keywords, context_window=100)
    
    # Detect warnings
    warnings = detect_warnings(analysis, transcript)
    
    return {
        'video_id': video_id,
        'transcript_available': True,
        'keyword_matches': analysis,
        'warnings_detected': warnings,
        'context_windows': extract_high_relevance_contexts(analysis)
    }
```

---

### Step 5: Integration with Existing Tools (1 hour)

**Enhance `get_achievement_roadmap()`**:
```python
# In get_achievement_roadmap(), after guide_map processing:

# PHASE 3.5: Add video guides
video_guides = {}
try:
    video_results = find_achievement_video_guides(game_identifier, max_results=2)
    if video_results and 'videos' in video_results:
        for video in video_results['videos']:
            video_guides[video['video_id']] = video
except Exception:
    pass  # Continue without video guides

# Enrich achievements with video data
for ach in locked_achievements:
    # ... existing enrichment ...
    
    # Add video guide if available
    if video_guides:
        ach['video_guides'] = list(video_guides.values())
        ach['recommended_guide_type'] = 'video' if is_spatial_task(ach['description']) else 'text'
```

**Enhance `scan_for_missable_content()`**:
```python
# After text guide scan, add video scan:

# PHASE 3.5: Scan video guides for missable warnings
video_warnings = []
try:
    video_results = find_achievement_video_guides(game_identifier, max_results=3)
    if video_results and 'videos' in video_results:
        for video in video_results['videos']:
            analysis = analyze_video_guide(
                video['url'],
                keywords=['missable', 'point of no return', 'before boss']
            )
            
            if analysis.get('warnings_detected'):
                video_warnings.append({
                    'source': 'youtube',
                    'video_title': video['title'],
                    'video_url': video['url'],
                    'warnings': analysis['warnings_detected'],
                    'timestamps': extract_warning_timestamps(analysis)
                })
except Exception:
    pass

# Cross-validate text and video warnings
cross_validated = cross_validate_warnings(missable_warnings, video_warnings)
```

---

### Step 6: Testing & Validation (1 hour)

**Test cases**:
```python
# Test 1: Video guide search
result = find_achievement_video_guides("Elden Ring", "Legendary Armaments")
assert len(result['videos']) > 0
assert 'key_timestamps' in result['videos'][0]

# Test 2: Transcript analysis
analysis = analyze_video_guide(
    "https://youtube.com/watch?v=abc123",
    keywords=['missable', 'before boss']
)
assert 'keyword_matches' in analysis
assert 'warnings_detected' in analysis

# Test 3: Integration with roadmap
roadmap = get_achievement_roadmap("Elden Ring")
assert 'video_guides' in roadmap['roadmap'][0]
```

---

## Performance Considerations

### Caching Strategy

**YouTube API calls are expensive** (quota limits):
- Cache video search results: 60 min TTL
- Cache transcripts: 24 hour TTL (rarely change)
- Use existing `guide_cache` tier

**Implementation**:
```python
# In search_youtube_guides():
cache_key = f"yt_search:{game_name}:{query}"
cached = guide_cache.get(cache_key)
if cached:
    return cached

# ... API call ...

guide_cache.set(cache_key, results)
```

### Rate Limiting

**YouTube Data API quotas**:
- 10,000 units/day (free tier)
- Search: 100 units per request
- Limit to 3 videos per query to stay under quota

---

## Research Paper Alignment

### Scenario A: The Completionist (Enhanced)

**Original Workflow (Research Paper)**:
1. ✅ State Verification (steam-mcp)
2. ✅ Knowledge Retrieval (mediawiki-mcp)
3. ✅ Gap Analysis
4. ✅ Contextual Warning
5. **➡️ Visual Guide (youtube-mcp)** ← **THIS IS PHASE 3.5**

**Our Implementation**:
```python
# Step 5 from research paper, now integrated:
video_guides = find_achievement_video_guides("Elden Ring", "Bolt of Gransax")
best_video = video_guides['videos'][0]

response = {
    'text_guide': 'Leyndell capital, giant spear statue',
    'video_guide': best_video['url'],
    'timestamp': best_video['key_timestamps'][0]['time'],  # e.g., "3:45"
    'missable_warning': 'Must obtain before defeating Maliketh'
}
```

### Multi-Modal Intelligence Vision

**Research Paper Quote**:
> "For many complex spatial puzzles or boss fights, a text description is inferior to a visual demonstration."

**Our Solution**:
- Automatically detect spatial tasks: "climb", "jump", "rotate", "navigate"
- Recommend video over text for these tasks
- Provide **both** text and video options for user preference

---

## Dependencies & Prerequisites

### External Services
1. ✅ YouTube Data API v3 (key required)
2. ✅ YouTube MCP Server (`@jkawamoto/mcp-youtube-transcript`)
3. ✅ Python libraries: `youtube-transcript-api`, `google-api-python-client`

### Internal Requirements
1. ✅ Phase 2.1 caching infrastructure (for performance)
2. ✅ Phase 1 guide scanning (for cross-validation)
3. ⏳ Enhanced pattern matching (for video-specific warnings)

---

## Success Metrics

### Quantitative
- ✅ Video guide retrieval: <2 seconds per query
- ✅ Transcript analysis: <1 second per video
- ✅ Cache hit rate: >60% for popular games
- ✅ Missable detection accuracy: >85% (cross-validated)

### Qualitative
- ✅ User prefers video timestamp over text description for spatial tasks
- ✅ Missable warnings more trustworthy (text + video validation)
- ✅ Completionist workflow faster (no manual YouTube searching)

---

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|-----------|
| **YouTube API quota exceeded** | High | Cache aggressively, limit to 3 videos/query |
| **Auto-generated captions low quality** | Medium | Prefer manual captions, flag auto-gen as "lower confidence" |
| **Video deleted/private** | Low | Cache transcript, handle 404 gracefully |
| **Game-specific jargon misheard** | Medium | Build correction dictionary ("Estus" not "S test") |

---

## Timeline

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| **Step 1**: MCP Server Setup | 1 hour | YouTube MCP configured |
| **Step 2**: API Integration | 2 hours | Search + transcript functions |
| **Step 3**: Analysis Engine | 3 hours | Keyword matching, timestamp extraction |
| **Step 4**: Tool Implementation | 2 hours | 3 new MCP tools |
| **Step 5**: Integration | 1 hour | Enhanced existing tools |
| **Step 6**: Testing | 1 hour | Test suite + validation |
| **Total** | **10 hours** | **Phase 3.5 Complete** |

---

## Next Steps After Phase 3.5

### Phase 4: Full Multi-Modal Intelligence

**Research Paper Vision**:
- Screenshot analysis (OCR for HUD elements)
- Real-time screen capture for live coaching
- Voice command integration
- Predictive modeling

**Dependencies**: Vision models, screen capture MCP, real-time processing

---

## Conclusion

Phase 3.5 fills the critical gap between **text guides** and **visual walkthroughs** identified in the research paper. By integrating YouTube transcript analysis, we transform the Steam Library MCP Server into a true **multi-modal gaming co-pilot** that can:

✅ Search video guides automatically  
✅ Extract key timestamps for specific achievements  
✅ Cross-validate missable warnings (text + video)  
✅ Recommend video vs. text based on task complexity  
✅ Provide timestamped visual guidance  

This brings us **80% toward the "Digital Omniscience" vision** outlined in the research paper.

---

**Ready to implement?** All architectural decisions are based on the research paper's recommendations and align with the proven MCP ecosystem patterns.
