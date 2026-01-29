#!/usr/bin/env node

/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import { z } from 'zod';

const server = new McpServer({
  name: 'conductor',
  version: '0.1.0',
});

server.registerTool(
  'ralph_start',
  {
    title: 'Ralph Start Tool',
    description: 'Signals the start of a Ralph loop. This tool is used as a trigger for a `AfterTool` hook.',
    inputSchema: {
      prompt: z.string().describe('The full text of the user\'s request.'),
      maxIterations: z.number().describe('The maximum number of iterations for the loop.'),
      completionWord: z.string().describe('The word that signals completion.'),
    } as any,
  },
  async (args: any) => {
    return {
      content: [
        {
          type: 'text' as const,
          text: 'Ralph Start Tool Triggered.',
        },
      ],
    };
  }
);

server.registerTool(
  'ralph_end',
  {
    title: 'Ralph End Tool',
    description: 'Signals the end of a Ralph loop. This tool is used as a trigger for a `BeforeTool` hook.',
    inputSchema: {
      status: z.enum(['SUCCESS', 'FAILURE', 'STUCK']).describe('The final status of the loop.'),
      message: z.string().describe('A message describing the result or reason for failure.'),
    } as any,
  },
  async (args: any) => {
    return {
      content: [
        {
          type: 'text' as const,
          text: 'Ralph End Tool Triggered.',
        },
      ],
    };
  }
);

async function startServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

startServer();