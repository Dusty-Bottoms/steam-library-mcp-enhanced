#!/usr/bin/env python3
"""Test script for Phase 1 strategic intelligence tools"""

import os
import sys
from dotenv import load_dotenv

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
load_dotenv()

# Import the server module
import mcp_server

def test_achievement_roadmap():
    """Test get_achievement_roadmap with Brotato"""
    print("\n" + "="*80)
    print("TEST 1: Achievement Roadmap for Brotato")
    print("="*80)
    
    try:
        result = mcp_server.get_achievement_roadmap("Brotato", sort_by="efficiency")
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✓ Game: {result.get('game', 'Unknown')}")
        print(f"✓ Total Achievements: {result.get('total_achievements', 0)}")
        print(f"✓ Unlocked: {result.get('unlocked', 0)}")
        print(f"✓ Completion: {result.get('completion_percentage', 0)}%")
        print(f"✓ Remaining: {result.get('total_remaining', 0)}")
        print(f"✓ Sort Strategy: {result.get('sort_strategy', 'unknown')}")
        
        roadmap = result.get('roadmap', [])
        if roadmap:
            print(f"\n✓ Top 3 Recommended Achievements:")
            for i, ach in enumerate(roadmap[:3], 1):
                print(f"\n  {i}. {ach.get('name', 'Unknown')}")
                print(f"     Priority Score: {ach.get('priority_score', 0)}")
                print(f"     Rarity: {ach.get('rarity', 0)}%")
                print(f"     Difficulty: {ach.get('estimated_difficulty', 'unknown')}")
                print(f"     Has Guide: {ach.get('has_guide', False)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_scan_missable():
    """Test scan_for_missable_content"""
    print("\n" + "="*80)
    print("TEST 2: Scan for Missable Content (Brotato - should have none)")
    print("="*80)
    
    try:
        result = mcp_server.scan_for_missable_content("Brotato")
        
        if 'error' in result:
            print(f"❌ Error: {result['error']}")
            return False
        
        print(f"✓ Game: {result.get('game', 'Unknown')}")
        print(f"✓ Missable Count: {result.get('missable_count', 0)}")
        
        if result.get('message'):
            print(f"✓ Message: {result['message']}")
        
        if result.get('recommendation'):
            print(f"⚠️  Recommendation: {result['recommendation']}")
        
        guide_warnings = result.get('guide_warnings', [])
        if guide_warnings:
            print(f"\n⚠️  Guide Warnings ({len(guide_warnings)}):")
            for w in guide_warnings[:2]:
                print(f"  - {w.get('guide_title', 'Unknown')}")
        
        ach_warnings = result.get('achievement_warnings', [])
        if ach_warnings:
            print(f"\n⚠️  Achievement Warnings ({len(ach_warnings)}):")
            for w in ach_warnings[:2]:
                print(f"  - {w.get('achievement_name', 'Unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_session_context():
    """Test get_current_session_context"""
    print("\n" + "="*80)
    print("TEST 3: Current Session Context")
    print("="*80)
    
    try:
        result = mcp_server.get_current_session_context()
        
        if result.get('status') == 'no_recent_activity':
            print(f"ℹ️  {result.get('message', 'No recent activity')}")
            return True
        
        print(f"✓ Game: {result.get('game', 'Unknown')}")
        print(f"✓ Session Status: {result.get('session_status', 'unknown')}")
        print(f"✓ Recent Playtime: {result.get('playtime_recent_2weeks', 0)} hours")
        print(f"✓ Total Playtime: {result.get('playtime_total', 0)} hours")
        
        ach_progress = result.get('achievement_progress', {})
        if 'error' not in ach_progress:
            print(f"\n✓ Achievement Progress:")
            print(f"  - Completion: {ach_progress.get('completion_percentage', 0)}%")
            print(f"  - Unlocked: {ach_progress.get('unlocked', 0)}/{ach_progress.get('total', 0)}")
        
        missable = result.get('missable_alerts', {})
        if missable.get('has_warnings'):
            print(f"\n⚠️  Missable Alerts: {missable.get('count', 0)} warnings found")
        else:
            print(f"\n✓ No missable content warnings")
        
        suggestion = result.get('suggested_next_achievement', {})
        if 'error' not in suggestion:
            print(f"\n✓ Suggested Next Achievement:")
            print(f"  - {suggestion.get('name', 'Unknown')}")
            print(f"  - Priority: {suggestion.get('priority_score', 0)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("\n" + "="*80)
    print("PHASE 1 STRATEGIC INTELLIGENCE TOOLS - TEST SUITE")
    print("="*80)
    
    results = []
    
    # Test 1: Achievement Roadmap
    results.append(("Achievement Roadmap", test_achievement_roadmap()))
    
    # Test 2: Missable Content Scanner
    results.append(("Missable Content Scanner", test_scan_missable()))
    
    # Test 3: Session Context
    results.append(("Session Context", test_session_context()))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    sys.exit(0 if passed == total else 1)
