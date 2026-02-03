import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import { getVcs } from "./vcs/index.js";
import { CommitParams } from "./vcs/types.js";

const server = new McpServer({
  name: "conductor-vcs",
  version: "1.0.0",
});

// Helper to get VCS instance and handle errors
function withVcs<T>(repoPath: string, operation: (vcs: any) => T): T {
  try {
    const vcs = getVcs(repoPath);
    return operation(vcs);
  } catch (error: any) {
    throw new Error(`VCS Error: ${error.message}`);
  }
}

server.tool(
  "vcs_get_status",
  {
    repo_path: z.string().describe("Path to the repository root"),
  },
  async ({ repo_path }) => {
    return withVcs(repo_path, (vcs) => {
      const status = vcs.get_status(repo_path);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(status, null, 2),
          },
        ],
      };
    });
  }
);

server.tool(
  "vcs_create_commit",
  {
    repo_path: z.string().describe("Path to the repository root"),
    message: z.string().describe("Commit message"),
    files: z.array(z.string()).optional().describe("List of files to commit. If omitted, behavior depends on VCS (Git: stages modified, JJ: snapshot)"),
  },
  async ({ repo_path, message, files }) => {
    return withVcs(repo_path, (vcs) => {
      const params: CommitParams = { path: repo_path, message, files };
      const result = vcs.create_commit(params);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(result, null, 2),
          },
        ],
      };
    });
  }
);

server.tool(
  "vcs_get_log",
  {
    repo_path: z.string().describe("Path to the repository root"),
    limit: z.number().default(10).describe("Number of commits to retrieve"),
    revision_range: z.string().optional().describe("Optional revision range (e.g. 'HEAD~5..HEAD' or 'main')"),
  },
  async ({ repo_path, limit, revision_range }) => {
    return withVcs(repo_path, (vcs) => {
      const logs = vcs.get_log(repo_path, limit, revision_range);
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(logs, null, 2),
          },
        ],
      };
    });
  }
);

server.tool(
  "vcs_get_diff",
  {
    repo_path: z.string().describe("Path to the repository root"),
    file_path: z.string().optional().describe("Specific file to diff"),
    revision_range: z.string().optional().describe("Revision range for diff"),
  },
  async ({ repo_path, file_path, revision_range }) => {
    return withVcs(repo_path, (vcs) => {
      const diff = vcs.get_diff(repo_path, revision_range, file_path);
      return {
        content: [
          {
            type: "text",
            text: diff || "No diff found or binary file.",
          },
        ],
      };
    });
  }
);

server.tool(
  "vcs_read_file",
  {
    repo_path: z.string().describe("Path to the repository root"),
    file_path: z.string().describe("Path to the file"),
    revision: z.string().default("HEAD").describe("Revision to read from (default: HEAD)"),
  },
  async ({ repo_path, file_path, revision }) => {
    return withVcs(repo_path, (vcs) => {
      const content = vcs.get_file_content(repo_path, revision, file_path);
      return {
        content: [
          {
            type: "text",
            text: content,
          },
        ],
      };
    });
  }
);

server.tool(
    "vcs_list_conflicts",
    {
      repo_path: z.string().describe("Path to the repository root"),
    },
    async ({ repo_path }) => {
      return withVcs(repo_path, (vcs) => {
        const conflicts = vcs.list_conflicts(repo_path);
        return {
          content: [
            {
              type: "text",
              text: JSON.stringify(conflicts, null, 2),
            },
          ],
        };
      });
    }
  );

server.tool(
  "vcs_resolve_conflict",
  {
    repo_path: z.string().describe("Path to the repository root"),
    files: z.array(z.string()).describe("List of files to mark as resolved"),
  },
  async ({ repo_path, files }) => {
    return withVcs(repo_path, (vcs) => {
      vcs.resolve_conflict({ path: repo_path, files });
      return {
        content: [
          {
            type: "text",
            text: `Marked ${files.length} files as resolved.`,
          },
        ],
      };
    });
  }
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("Conductor VCS MCP Server running on stdio");
}

main().catch((error) => {
  console.error("Fatal error in main():", error);
  process.exit(1);
});
