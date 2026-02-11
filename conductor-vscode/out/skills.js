"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.readSkillContent = exports.commandToSkillName = exports.normalizeCommand = void 0;
const fs = __importStar(require("fs/promises"));
const path = __importStar(require("path"));
const COMMAND_ALIASES = {
    'setup': 'setup',
    'newtrack': 'newtrack',
    'new-track': 'newtrack',
    'new_track': 'newtrack',
    'status': 'status',
    'implement': 'implement',
    'revert': 'revert',
};
const COMMAND_TO_SKILL = {
    setup: 'conductor-setup',
    newtrack: 'conductor-newtrack',
    status: 'conductor-status',
    implement: 'conductor-implement',
    revert: 'conductor-revert',
};
function normalizeCommand(command) {
    const normalized = (command || 'status').toLowerCase();
    return COMMAND_ALIASES[normalized] ?? 'status';
}
exports.normalizeCommand = normalizeCommand;
function commandToSkillName(command) {
    const normalized = normalizeCommand(command);
    return COMMAND_TO_SKILL[normalized] ?? null;
}
exports.commandToSkillName = commandToSkillName;
async function readSkillContent(extensionRoot, command) {
    const skillName = commandToSkillName(command);
    if (!skillName) {
        return null;
    }
    const skillPath = path.join(extensionRoot, 'skills', skillName, 'SKILL.md');
    try {
        return await fs.readFile(skillPath, 'utf8');
    }
    catch {
        return null;
    }
}
exports.readSkillContent = readSkillContent;
//# sourceMappingURL=skills.js.map
