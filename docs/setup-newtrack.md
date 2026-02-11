# Setup & NewTrack UX Guide

This guide documents the canonical setup and newTrack experience across adapters.

## Setup (Greenfield)

1. Run setup:
   - Gemini/Qwen: `/conductor:setup`
   - Claude/Codex/OpenCode: `/conductor-setup` or `$conductor-setup`
2. Conductor creates:
   - `conductor/product.md`, `product-guidelines.md`, `tech-stack.md`
   - `conductor/workflow.md`, `conductor/tracks.md`, `conductor/setup_state.json`
   - `conductor/tracks/<track_id>/{spec.md,plan.md,metadata.json,index.md}`

## Setup (Brownfield)

Conductor detects existing code, scans relevant files, and documents the existing tech stack without proposing changes.

## NewTrack

Example:
```bash
/conductor:newTrack "Add billing dashboard"
```

Expected artifacts:
- `conductor/tracks/<track_id>/spec.md`
- `conductor/tracks/<track_id>/plan.md`
- `conductor/tracks/<track_id>/metadata.json`
- `conductor/tracks/<track_id>/index.md`
- Track entry appended to `conductor/tracks.md`

## Metadata Fields

```json
{
  "track_id": "<track_id>",
  "type": "feature",
  "status": "new",
  "created_at": "YYYY-MM-DDTHH:MM:SSZ",
  "updated_at": "YYYY-MM-DDTHH:MM:SSZ",
  "description": "Add billing dashboard"
}
```

## Adapter Command Mapping

See `docs/skill-command-syntax.md` for the per-tool command syntax.

## Troubleshooting

- **Setup resumes unexpectedly:** Check `conductor/setup_state.json` and reset `last_successful_step` if you need to restart.
- **Track ID collision:** If a short name already exists, choose a different description or resume the existing track.
- **Missing metadata.json:** Ensure the track directory is writable and re-run `/conductor:newTrack`.
- **Files not appearing in UI:** Verify the adapter’s workflow/skill location and rerun sync scripts.
