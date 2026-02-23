#!/usr/bin/env python3
"""Issue Triage Bot - Analyze and classify GitHub issues from upstream repositories.

This script fetches issues from upstream repositories, classifies them,
and can automatically create tracks for high-priority issues.
"""

import os
import sys
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from collections import defaultdict

import requests
from github import Github, Auth, Issue


class TriageError(Exception):
    """Base exception for triage errors."""
    pass


class IssueClassifier:
    """Classify GitHub issues by type and priority."""

    # Keywords for issue classification
    BUG_KEYWORDS = ['bug', 'error', 'fail', 'crash', 'broken', 'issue', 'fix']
    FEATURE_KEYWORDS = ['feature', 'enhancement', 'add', 'support', 'new']
    DOCS_KEYWORDS = ['docs', 'documentation', 'typo', 'readme']
    QUESTION_KEYWORDS = ['question', 'help', 'how to', 'usage']

    # Priority scoring weights
    LABEL_WEIGHTS = {
        'bug': 30,
        'critical': 50,
        'high-priority': 40,
        'enhancement': 20,
        'good-first-issue': 10,
        'help-wanted': 15,
    }

    def __init__(self):
        """Initialize the classifier."""
        pass

    def classify_type(self, title: str, body: str, labels: list) -> str:
        """Classify issue type based on content.

        Args:
            title: Issue title
            body: Issue body/description
            labels: List of label names

        Returns:
            Issue type: 'bug', 'feature', 'docs', 'question', or 'other'
        """
        text = f"{title} {body}".lower()

        # Check labels first
        label_text = ' '.join(labels).lower()
        if 'bug' in label_text:
            return 'bug'
        if 'enhancement' in label_text or 'feature' in label_text:
            return 'feature'
        if 'documentation' in label_text or 'docs' in label_text:
            return 'docs'
        if 'question' in label_text:
            return 'question'

        # Fall back to keyword matching
        bug_score = sum(1 for kw in self.BUG_KEYWORDS if kw in text)
        feature_score = sum(1 for kw in self.FEATURE_KEYWORDS if kw in text)
        docs_score = sum(1 for kw in self.DOCS_KEYWORDS if kw in text)
        question_score = sum(1 for kw in self.QUESTION_KEYWORDS if kw in text)

        scores = {
            'bug': bug_score,
            'feature': feature_score,
            'docs': docs_score,
            'question': question_score,
        }

        max_type = max(scores, key=scores.get)
        if scores[max_type] > 0:
            return max_type

        return 'other'

    def calculate_priority(self, issue: dict) -> int:
        """Calculate priority score for an issue.

        Args:
            issue: Issue data from GitHub API

        Returns:
            Priority score (higher = more urgent)
        """
        score = 0

        # Label-based scoring
        labels = [label['name'] for label in issue.get('labels', [])]
        for label in labels:
            label_lower = label.lower()
            for key, weight in self.LABEL_WEIGHTS.items():
                if key in label_lower:
                    score += weight

        # Recency bonus (issues from last 7 days)
        created_at = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
        days_old = (datetime.now(timezone.utc) - created_at).days
        if days_old <= 7:
            score += 20
        elif days_old <= 30:
            score += 10

        # Engagement bonus (comments indicate interest)
        comments = issue.get('comments', 0)
        score += min(comments * 2, 20)  # Cap at 20 points

        # Upstream repo bonus
        repo_name = issue.get('repository_url', '').split('/')[-2:]
        repo_name = '/'.join(repo_name) if len(repo_name) == 2 else ''
        if repo_name in ['gemini-cli-extensions/conductor', 'jnorthrup/conductor2']:
            score += 15

        return score

    def get_priority_label(self, score: int) -> str:
        """Convert priority score to label.

        Args:
            score: Priority score

        Returns:
            Priority label: 'P0', 'P1', 'P2', or 'P3'
        """
        if score >= 80:
            return 'P0'  # Critical
        elif score >= 50:
            return 'P1'  # High
        elif score >= 30:
            return 'P2'  # Medium
        else:
            return 'P3'  # Low


class IssueTriageBot:
    """Main triage bot orchestrator."""

    def __init__(self, token: Optional[str] = None):
        """Initialize triage bot.

        Args:
            token: GitHub token (falls back to GITHUB_TOKEN env var)
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise TriageError("GitHub token required. Set GITHUB_TOKEN environment variable.")

        self.auth = Auth.Token(self.token)
        self.gh = Github(auth=self.auth)
        self.classifier = IssueClassifier()
        self.api_base = "https://api.github.com"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }

    def fetch_issues(self, repo_name: str, state: str = 'open') -> list:
        """Fetch issues from a repository.

        Args:
            repo_name: Repository name (owner/repo)
            state: Issue state ('open', 'closed', 'all')

        Returns:
            List of issue data
        """
        print(f"[FETCH] Fetching issues from {repo_name}...")
        url = f"{self.api_base}/repos/{repo_name}/issues"
        params = {'state': state, 'per_page': 100}

        issues = []
        while url:
            response = requests.get(url, headers=self.headers, params=params, timeout=30)
            response.raise_for_status()
            issues.extend(response.json())

            # Handle pagination
            if 'next' in response.links:
                url = response.links['next']['url']
                params = {}  # Params are in the URL
            else:
                url = None

        # Filter out pull requests
        issues = [i for i in issues if 'pull_request' not in i]
        print(f"[INFO] Found {len(issues)} issues")
        return issues

    def triage_issue(self, issue: dict) -> dict:
        """Triage a single issue.

        Args:
            issue: Issue data from GitHub API

        Returns:
            Triage result with classification and priority
        """
        labels = [label['name'] for label in issue.get('labels', [])]
        issue_type = self.classifier.classify_type(
            issue['title'],
            issue.get('body', ''),
            labels
        )
        priority_score = self.classifier.calculate_priority(issue)
        priority_label = self.classifier.get_priority_label(priority_score)

        return {
            'number': issue['number'],
            'title': issue['title'],
            'url': issue['html_url'],
            'type': issue_type,
            'priority': priority_label,
            'priority_score': priority_score,
            'labels': labels,
            'created_at': issue['created_at'],
            'state': issue['state'],
        }

    def generate_track_from_issue(self, triaged: dict) -> dict:
        """Generate a track structure from an issue.

        Args:
            triaged: Triaged issue data

        Returns:
            Track structure (spec, plan, metadata)
        """
        # Generate track ID
        timestamp = datetime.now().strftime("%Y%m%d")
        track_id = f"issue_{triaged['number']}_{timestamp}"

        # Create spec
        spec = f"""# Specification: {triaged['title']}

**Source Issue:** {triaged['url']}
**Upstream Issue:** #{triaged['number']}
**Priority:** {triaged['priority']}

## Overview
<!-- Brief description of the issue and proposed solution -->

## Requirements
<!-- Functional and non-functional requirements -->

## Acceptance Criteria
<!-- Clear criteria for when this track is complete -->

## References
- Upstream Issue: {triaged['url']}
- Related Labels: {', '.join(triaged['labels'])}
"""

        # Create plan
        plan = f"""# Implementation Plan: {triaged['title']}

**Track ID:** {track_id}
**Priority:** {triaged['priority']}
**Source:** Upstream Issue #{triaged['number']}

## Phase 1: Analysis

- [ ] Review upstream issue discussion
- [ ] Identify root cause or feature requirements
- [ ] Document implementation approach

## Phase 2: Implementation

- [ ] Implement solution
- [ ] Add tests if applicable
- [ ] Update documentation

## Phase 3: Verification

- [ ] Test implementation
- [ ] Verify against acceptance criteria
- [ ] Close upstream issue reference
"""

        # Create metadata
        metadata = {
            "track_id": track_id,
            "type": "feature" if triaged['type'] == 'feature' else "fix",
            "status": "new",
            "priority": triaged['priority'],
            "depends_on": [],
            "created_at": datetime.now(timezone.utc).isoformat(),
            "description": triaged['title'],
            "upstream_issue": triaged['url'],
        }

        return {
            'track_id': track_id,
            'spec': spec,
            'plan': plan,
            'metadata': metadata,
        }

    def triage_all(self, repos: list[str], output_file: Path) -> dict:
        """Triage issues from multiple repositories.

        Args:
            repos: List of repository names
            output_file: Path to save triage results

        Returns:
            Summary of triage results
        """
        results = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'repos': {},
            'summary': defaultdict(int),
        }

        all_triaged = []

        for repo in repos:
            print(f"\n{'='*60}")
            print(f"[TRIAGE] Processing {repo}")
            print(f"{'='*60}")

            try:
                issues = self.fetch_issues(repo)
                repo_results = []

                for issue in issues:
                    triaged = self.triage_issue(issue)
                    repo_results.append(triaged)
                    all_triaged.append(triaged)

                    # Update summary
                    results['summary'][triaged['type']] += 1
                    results['summary'][f"priority_{triaged['priority']}"] += 1

                results['repos'][repo] = {
                    'count': len(repo_results),
                    'issues': repo_results,
                }

            except Exception as e:
                print(f"[ERROR] Failed to triage {repo}: {e}")
                results['repos'][repo] = {'error': str(e)}

        # Save results
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2, default=str)

        # Print summary
        print("\n" + "="*60)
        print("Triage Summary")
        print("="*60)
        print(f"Total issues: {len(all_triaged)}")
        print("\nBy Type:")
        for issue_type, count in sorted(results['summary'].items()):
            if not issue_type.startswith('priority_'):
                print(f"  {issue_type}: {count}")
        print("\nBy Priority:")
        for priority in ['P0', 'P1', 'P2', 'P3']:
            count = results['summary'].get(f'priority_{priority}', 0)
            print(f"  {priority}: {count}")

        # Highlight high-priority issues
        high_priority = [i for i in all_triaged if i['priority'] in ['P0', 'P1']]
        if high_priority:
            print("\nHigh Priority Issues (P0/P1):")
            for issue in high_priority[:10]:  # Show top 10
                print(f"  [{issue['priority']}] #{issue['number']}: {issue['title']}")
                print(f"       {issue['url']}")

        return results


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Triage GitHub issues from upstream repositories")
    parser.add_argument(
        "--repo",
        action="append",
        default=[
            "gemini-cli-extensions/conductor",
            "jnorthrup/conductor2",
        ],
        help="Repositories to triage issues from",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(".github/issue_triage_results.json"),
        help="Path to save triage results",
    )
    parser.add_argument(
        "--create-tracks",
        action="store_true",
        help="Create track folders for high-priority issues",
    )
    parser.add_argument(
        "--min-priority",
        default="P2",
        choices=['P0', 'P1', 'P2', 'P3'],
        help="Minimum priority for track creation (default: P2)",
    )

    args = parser.parse_args()

    print("="*60)
    print("Issue Triage Bot")
    print("="*60)
    print(f"Repos: {', '.join(args.repo)}")
    print(f"Output: {args.output}")
    print(f"Create tracks: {args.create_tracks}")
    print(f"Min priority for tracks: {args.min_priority}")
    print("="*60)

    try:
        bot = IssueTriageBot()
        results = bot.triage_all(args.repo, args.output)

        # Optionally create tracks for high-priority issues
        if args.create_tracks:
            priority_order = {'P0': 0, 'P1': 1, 'P2': 2, 'P3': 3}
            min_priority_level = priority_order[args.min_priority]

            for issue in results['repos'].get('gemini-cli-extensions/conductor', {}).get('issues', []):
                if priority_order.get(issue['priority'], 4) <= min_priority_level:
                    print(f"\n[TRACK] Creating track for issue #{issue['number']}...")
                    # In production, would create track files here
                    track = bot.generate_track_from_issue(issue)
                    print(f"      Track ID: {track['track_id']}")
                    print(f"      Priority: {issue['priority']}")

        return 0

    except TriageError as e:
        print(f"[FATAL] {e}")
        return 1
    except Exception as e:
        print(f"[ERROR] Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
