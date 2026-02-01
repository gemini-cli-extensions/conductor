import * as fs from 'fs/promises';
import * as path from 'path';

export type SkillCommand = 'setup' | 'newtrack' | 'status' | 'implement' | 'revert';

const COMMAND_ALIASES: Record<string, SkillCommand> = {
    'setup': 'setup',
    'newtrack': 'newtrack',
    'new-track': 'newtrack',
    'new_track': 'newtrack',
    'status': 'status',
    'implement': 'implement',
    'revert': 'revert',
};

const COMMAND_TO_SKILL: Record<SkillCommand, string> = {
    setup: 'conductor-setup',
    newtrack: 'conductor-newtrack',
    status: 'conductor-status',
    implement: 'conductor-implement',
    revert: 'conductor-revert',
};

export function normalizeCommand(command?: string): SkillCommand {
    const normalized = (command || 'status').toLowerCase();
    return COMMAND_ALIASES[normalized] ?? 'status';
}

export function commandToSkillName(command: string): string | null {
    const normalized = normalizeCommand(command);
    return COMMAND_TO_SKILL[normalized] ?? null;
}

export async function readSkillContent(extensionRoot: string, command: string): Promise<string | null> {
    const skillName = commandToSkillName(command);
    if (!skillName) {
        return null;
    }

    const skillPath = path.join(extensionRoot, 'skills', skillName, 'SKILL.md');
    try {
        return await fs.readFile(skillPath, 'utf8');
    } catch {
        return null;
    }
}
