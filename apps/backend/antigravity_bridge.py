#!/usr/bin/env python3
"""
Antigravity Context Bridge

Reads project context from Antigravity-Manager's project registry
and injects it into Auto-Claude spec creation.

Usage:
    python antigravity_bridge.py --project flow-daw-2030
"""

from __future__ import annotations
import json
import os
import sys
from pathlib import Path
from typing import Optional, Dict

# Antigravity stores project data in localStorage (browser storage)
# For now, we read from a JSON export or the default projects
ANTIGRAVITY_PROJECTS_PATH = Path.home() / ".antigravity" / "projects.json"

# Default projects from Antigravity-Manager (fallback)
DEFAULT_PROJECTS = {
    "flow-daw-2030": {
        "name": "Flow DAW 2030",
        "path": "/Volumes/PRIME APP SSD/Projects/flow-daw-2030",
        "type": "tauri",
        "aiContext": "Professional DAW with AURA AI. Tauri v2 + React. Key components: ArrangeWindow, FloatingHUD, MasterChain, SpectralEditor."
    },
    "mixxos-prime-fabric": {
        "name": "MixxOS Prime Fabric",
        "path": "/Volumes/PRIME APP SSD/Projects/MixxOS---Prime-Fabric-Prototype",
        "type": "web",
        "aiContext": "MixxOS desktop environment prototype with district system, tower portals, and glassmorphic design."
    },
    "raven-mix-ai": {
        "name": "Raven Mix AI",
        "path": "/Volumes/PRIME APP SSD/Projects/raven-mix-ai",
        "type": "web",
        "aiContext": "AI-powered mixing assistant with HybridDAW integration and intelligent stem processing."
    },
    "mixxverse-creative-engine": {
        "name": "Mixxverse Creative Engine V2",
        "path": "/Volumes/PRIME APP SSD/Projects/mixxverse-creative-engine-v2",
        "type": "web",
        "aiContext": "Creative content engine for the Mixxverse ecosystem with AI-driven generation tools."
    },
    "antigravity-manager": {
        "name": "Antigravity Manager",
        "path": "/Volumes/PRIME APP SSD/Projects/Antigravity-Manager",
        "type": "tauri",
        "aiContext": "AI account orchestration and API gateway. Manages Gemini/Claude/OpenAI proxy with smart routing."
    },
    "cognee": {
        "name": "Cognee",
        "path": "/Volumes/PRIME APP SSD/Projects/cognee",
        "type": "other",
        "aiContext": "Knowledge graph and memory system for AI applications."
    },
    "auto-claude": {
        "name": "Auto-Claude",
        "path": "/Volumes/PRIME APP SSD/Projects/Auto-Claude",
        "type": "other",
        "aiContext": "Autonomous multi-agent coding framework. Python backend + Electron frontend. Planner→Coder→QA pipeline with Git worktree isolation."
    }
}


def load_projects() -> dict:
    """Load projects from Antigravity export file or use defaults."""
    if ANTIGRAVITY_PROJECTS_PATH.exists():
        with open(ANTIGRAVITY_PROJECTS_PATH) as f:
            return json.load(f)
    return DEFAULT_PROJECTS


def get_project_context(project_id: str) -> Optional[dict]:
    """Get project context by ID."""
    projects = load_projects()
    return projects.get(project_id)


def inject_context_to_spec(project_id: str, task_description: str) -> str:
    """
    Inject project context into a task description for Auto-Claude.
    
    Returns an enhanced task description with project context prepended.
    """
    project = get_project_context(project_id)
    if not project:
        print(f"Warning: Project '{project_id}' not found in Antigravity registry")
        return task_description
    
    context = project.get("aiContext", "")
    project_name = project.get("name", project_id)
    project_type = project.get("type", "unknown")
    
    enhanced = f"""# Project Context (from Antigravity)
**Project:** {project_name}
**Type:** {project_type}
**Context:** {context}

# Task
{task_description}
"""
    return enhanced


def list_projects() -> None:
    """Print all registered projects."""
    projects = load_projects()
    print("\n📁 Antigravity Registered Projects:\n")
    for pid, project in projects.items():
        name = project.get("name", pid)
        ptype = project.get("type", "?")
        context = project.get("aiContext", "No context")[:60]
        print(f"  • {pid}")
        print(f"    Name: {name}")
        print(f"    Type: {ptype}")
        print(f"    Context: {context}...")
        print()


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Antigravity Context Bridge for Auto-Claude")
    parser.add_argument("--project", "-p", help="Project ID to get context for")
    parser.add_argument("--task", "-t", help="Task description to enhance with context")
    parser.add_argument("--list", "-l", action="store_true", help="List all projects")
    
    args = parser.parse_args()
    
    if args.list:
        list_projects()
    elif args.project and args.task:
        enhanced = inject_context_to_spec(args.project, args.task)
        print(enhanced)
    elif args.project:
        project = get_project_context(args.project)
        if project:
            print(json.dumps(project, indent=2))
        else:
            print(f"Project '{args.project}' not found")
            sys.exit(1)
    else:
        parser.print_help()
