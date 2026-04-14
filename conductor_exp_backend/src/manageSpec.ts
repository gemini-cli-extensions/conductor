import { writeFileSync, readFileSync } from 'fs';
import { exec } from 'child_process';
import path from 'path';


import { existsSync, mkdirSync } from 'fs';

/**
 * Ensures the project-level specs/ directory exists for permanent, repo-checked-in spec tracking.
 */
function ensureSpecsDir() {
    const specsDir = path.resolve(process.cwd(), 'conductor', 'tracks');
    if (!existsSync(specsDir)) {
        mkdirSync(specsDir, { recursive: true });
        console.error(`Created specs directory at ${specsDir}`);
    }
    return specsDir;
}

/**
 * Initializes a Master Spec at the project root with YAML frontmatter.
 * This is used for greenfield or brownfield project goal scoping.
 */
export async function initMasterSpec(specId: string, goal: string, requirements: string[], verifiers: any[]): Promise<string> {
    const specsDir = ensureSpecsDir();
    const specPath = path.resolve(specsDir, `${specId}.md`);

    const yamlFrontmatter = `---
id: ${specId}
type: master-spec
status: draft
requirements:
${requirements.map(r => `  - "${String(r).replace(/"/g, '\\"')}"`).join('\n')}
verifiers:
${verifiers.map(v => `  - type: ${v.type}\n    cmd: "${v.cmd}"`).join('\n')}
---
# Master Spec: ${specId}

## Goal
${goal}

## Requirements
${requirements.map(r => `- ${r}`).join('\n')}
`;

    writeFileSync(specPath, yamlFrontmatter);
    console.error(`Initialized Master Spec at ${specPath}`);
    return `Master Spec ${specId} successfully initialized at project level.`;
}

/**
 * Creates a Sub-Spec linked back to a parent Master Spec.
 * Automatically adds an inline hyperlink in the parent spec for navigation.
 */
export async function addSubSpec(specId: string, parentId: string, goal: string, requirements: string[], verifiers: any[]): Promise<string> {
    const specsDir = ensureSpecsDir();
    const specPath = path.resolve(specsDir, `${specId}.md`);

    // Verify parent exists before linking to ensure graph integrity
    const parentPath = path.resolve(specsDir, `${parentId}.md`);
    if (!existsSync(parentPath)) {
        throw new Error(`Parent spec ID '${parentId}' not found at '${parentPath}'. Cannot link.`);
    }

    const yamlFrontmatter = `---
id: ${specId}
type: sub-spec
parent: ${parentId}
status: draft
requirements:
${requirements.map(r => `  - "${String(r).replace(/"/g, '\\"')}"`).join('\n')}
verifiers:
${verifiers.map(v => `  - type: ${v.type}\n    cmd: "${v.cmd}"`).join('\n')}
---
# Sub-Spec: ${specId}

## Parent Link
[Parent Spec (${parentId})](file://${parentPath})

## Context / Goal
${goal}

## Requirements
${requirements.map(r => `- ${r}`).join('\n')}
`;

    writeFileSync(specPath, yamlFrontmatter);

    // Now modify parent to add link
    let parentContent = readFileSync(parentPath, 'utf-8');
    
    // Append the link at the end or in a "Sub-specs" section
    if (!parentContent.includes('## Sub-Specs')) {
        parentContent += `\n\n## Sub-Specs\n`;
    }
    parentContent += `- [Sub-Spec ${specId}](file://${specPath})\n`;

    writeFileSync(parentPath, parentContent);

    console.error(`Added Sub-Spec at ${specPath} and linked in ${parentPath}`);
    return `Sub-Spec ${specId} successfully linked to ${parentId}.`;
}

import { readdirSync, readFileSync as readFsFile } from 'fs';
import { getTrackState } from './stateManager.js';

/**
 * Reads all specs in the specs/ folder to build a relational graph of dependencies.
 * This is used by agents before modification to predict cross-cutting impacts.
 */
export async function runImpactAnalysis(): Promise<string> {
    const specsDir = ensureSpecsDir();
    const files = readdirSync(specsDir, { withFileTypes: true })
        .filter(dirent => dirent.isDirectory())
        .map(dirent => path.join(dirent.name, 'spec.md'))
        .filter(relPath => existsSync(path.resolve(specsDir, relPath)));

    let summary = "### Project Spec Hierarchy Graph\n\n";

    for (const file of files) {
        const filePath = path.resolve(specsDir, file);
        const content = readFsFile(filePath, 'utf-8');

        // Extract ID and Title
        const idMatch = content.match(/^id:\s*(.*)$/m);
        const trackId = idMatch ? idMatch[1].trim() : 'Unknown';
        const titleMatch = content.match(/^# (.*)$/m);
        const title = titleMatch ? titleMatch[1] : file;
        
        // Context Awareness: Check centralized state first
        const liveState = getTrackState(trackId);
        
        const typeMatch = content.match(/^type:\s*(.*)$/m);
        const parentMatch = content.match(/^parent:\s*(.*)$/m);
        
        // Status resolution: Priority to Live State > YAML
        let status = 'unknown';
        let statusFlag = '';
        if (liveState) {
            status = liveState.status;
            if (liveState.locked_by) {
                statusFlag = ` (Locked by ${liveState.locked_by})`;
            }
        } else {
            const statusMatch = content.match(/^status:\s*(.*)$/m);
            status = statusMatch ? statusMatch[1].trim() : 'unknown';
        }

        summary += `- **${trackId}** (${typeMatch ? typeMatch[1].trim() : 'unknown'})\n`;
        summary += `  Title: ${title}\n`;
        summary += `  Status: ${status}${statusFlag}\n`;
        if (parentMatch) {
            summary += `  Parent: ${parentMatch[1].trim()}\n`;
        }
        summary += `  Path: ${file}\n\n`;
    }

    if (files.length === 0) {
        return "No specs found in the repository. Initialize using create_master_spec.";
    }

    return summary;
}


