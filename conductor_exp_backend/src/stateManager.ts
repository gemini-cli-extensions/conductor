import { readFileSync, writeFileSync, existsSync, mkdirSync, lstatSync } from 'fs';
import path from 'path';

export interface TrackState {
    status: 'in_progress' | 'in_review';
    mode: 'isolated' | 'standard';
    worktree_path: string;
    locked_at?: string;
    locked_by?: string;
}

export interface ProjectState {
    version: number;
    tracks: {
        [trackId: string]: TrackState;
    };
}

function getTrackerPath(): string {
    const startDir = process.cwd();
    const rootDir = path.parse(startDir).root;
    let currentDir = startDir;

    // Fase 1: Buscar hacia arriba un state.json ya existente
    while (currentDir !== rootDir) {
        const trackerFile = path.resolve(currentDir, '.gemini', 'trackers', 'state.json');
        if (existsSync(trackerFile)) {
            return trackerFile;
        }
        currentDir = path.dirname(currentDir);
    }

    // Fase 2: Si no existe, buscar la raíz real del proyecto (.git como directorio)
    currentDir = startDir;
    while (currentDir !== rootDir) {
        const gitPath = path.resolve(currentDir, '.git');
        if (existsSync(gitPath)) {
            try {
                // En el repo principal .git es DIR. En worktrees es FILE.
                if (lstatSync(gitPath).isDirectory()) {
                    const newTrackerDir = path.resolve(currentDir, '.gemini', 'trackers');
                    if (!existsSync(newTrackerDir)) {
                        mkdirSync(newTrackerDir, { recursive: true });
                    }
                    return path.resolve(newTrackerDir, 'state.json');
                }
            } catch (e) { /* ignorar errores de lstat */ }
        }
        currentDir = path.dirname(currentDir);
    }

    // Fase 3: Heurística final (buscar carpeta 'conductor')
    currentDir = startDir;
    while (currentDir !== rootDir) {
        if (existsSync(path.resolve(currentDir, 'conductor'))) {
            const fbTrackerDir = path.resolve(currentDir, '.gemini', 'trackers');
            if (!existsSync(fbTrackerDir)) mkdirSync(fbTrackerDir, { recursive: true });
            return path.resolve(fbTrackerDir, 'state.json');
        }
        currentDir = path.dirname(currentDir);
    }

    // Fallback absoluto al cwd (comportamiento actual)
    const fallbackDir = path.resolve(process.cwd(), '.gemini', 'trackers');
    if (!existsSync(fallbackDir)) mkdirSync(fallbackDir, { recursive: true });
    return path.resolve(fallbackDir, 'state.json');
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
 * Attempts to lock a track. Fails if already locked by someone else.
 */
export function lockTrack(trackId: string, agentName: string): string {
    const state = readState();
    const existing = state.tracks[trackId];

    if (existing && existing.locked_by) {
        throw new Error(`Track '${trackId}' is already locked by '${existing.locked_by}' (Status: ${existing.status})`);
    }

    // Preserve existing metadata if it exists (e.g., worktree_path)
    state.tracks[trackId] = {
        status: existing?.status || 'in_progress',
        mode: existing?.mode || 'standard',
        worktree_path: existing?.worktree_path || '.',
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
    const existing = state.tracks[trackId];
    
    if (!existing || !existing.locked_by) {
        return lockTrack(trackId, agentName);
    }

    const previousOwner = existing.locked_by;
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
        throw new Error(`Cannot update: Track '${trackId}' is not found in state.`);
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
 * Releases a track lock but keeps the track in the registry (especially for isolated mode).
 */
export function unlockTrack(trackId: string): string {
    const state = readState();
    if (!state.tracks[trackId]) {
        return `Track '${trackId}' was not in state.`;
    }

    delete state.tracks[trackId].locked_at;
    delete state.tracks[trackId].locked_by;
    
    writeState(state);
    return `Track '${trackId}' successfully unlocked (Metadata preserved).`;
}

/**
 * Completely removes a track from the state registry.
 * Use ONLY when the worktree is deleted or the track is merged/discarded.
 */
export function discardTrack(trackId: string): string {
    const state = readState();
    if (state.tracks[trackId]) {
        delete state.tracks[trackId];
        writeState(state);
        return `Track '${trackId}' removed from state registry.`;
    }
    return `Track '${trackId}' was not in registry.`;
}

/**
 * Utility for analyze to get real-time state.
 */
export function getTrackState(trackId: string): TrackState | null {
    const state = readState();
    return state.tracks[trackId] || null;
}
