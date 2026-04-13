import { readFileSync, writeFileSync, existsSync, mkdirSync } from 'fs';
import path from 'path';

export interface TrackState {
    status: 'in_progress' | 'in_review';
    mode: 'isolated' | 'standard';
    worktree_path: string;
    locked_at: string;
    locked_by: string;
}

export interface ProjectState {
    version: number;
    tracks: {
        [trackId: string]: TrackState;
    };
}

function getTrackerPath() {
    const trackerDir = path.resolve(process.cwd(), '.gemini', 'trackers');
    if (!existsSync(trackerDir)) {
        mkdirSync(trackerDir, { recursive: true });
    }
    return path.resolve(trackerDir, 'state.json');
}

function readState(): ProjectState {
    const statePath = getTrackerPath();
    if (!existsSync(statePath)) {
        return { version: 1, tracks: {} };
    }
    try {
        const content = readFileSync(statePath, 'utf-8');
        return JSON.parse(content);
    } catch (error) {
        console.error(`Error reading state.json: ${error}`);
        return { version: 1, tracks: {} };
    }
}

function writeState(state: ProjectState) {
    const statePath = getTrackerPath();
    writeFileSync(statePath, JSON.stringify(state, null, 2), 'utf-8');
}

/**
 * Attempts to lock a track. Fails if already locked.
 */
export function lockTrack(trackId: string, agentName: string): string {
    const state = readState();
    if (state.tracks[trackId]) {
        throw new Error(`Track '${trackId}' is already locked by '${state.tracks[trackId].locked_by}' (Status: ${state.tracks[trackId].status})`);
    }

    state.tracks[trackId] = {
        status: 'in_progress', // Default starting status
        mode: 'standard',      // Default until updated
        worktree_path: '.',    // Default until updated
        locked_at: new Date().toISOString(),
        locked_by: agentName
    };

    writeState(state);
    return `Track '${trackId}' successfully locked by '${agentName}'.`;
}

/**
 * Takes over an existing lock or creates a new one if it doesn't exist.
 * Used when transitioning between lifecycle stages (e.g., implement -> review).
 */
export function takeoverLock(trackId: string, agentName: string): string {
    const state = readState();
    
    if (!state.tracks[trackId]) {
        // If not locked, just lock it normally
        return lockTrack(trackId, agentName);
    }

    const previousOwner = state.tracks[trackId].locked_by;
    state.tracks[trackId].locked_by = agentName;
    state.tracks[trackId].locked_at = new Date().toISOString();
    
    writeState(state);
    return `Track '${trackId}' lock taken over from '${previousOwner}' by '${agentName}'.`;
}

/**
 * Updates an existing lock with specific implementation details.
 */
export function updateTrackState(trackId: string, status: 'in_progress' | 'in_review', mode: 'isolated' | 'standard', worktreePath: string): string {
    const state = readState();
    if (!state.tracks[trackId]) {
        throw new Error(`Cannot update: Track '${trackId}' is not locked.`);
    }

    state.tracks[trackId] = {
        ...state.tracks[trackId],
        status,
        mode,
        worktree_path: worktreePath
    };

    writeState(state);
    return `Track '${trackId}' state updated to '${status}' (${mode} mode).`;
}

/**
 * Releases a track lock.
 */
export function unlockTrack(trackId: string): string {
    const state = readState();
    if (!state.tracks[trackId]) {
        return `Track '${trackId}' was not locked.`;
    }

    delete state.tracks[trackId];
    writeState(state);
    return `Track '${trackId}' successfully unlocked.`;
}

/**
 * Utility for analyze to get real-time state.
 */
export function getTrackState(trackId: string): TrackState | null {
    const state = readState();
    return state.tracks[trackId] || null;
}
