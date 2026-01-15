# Conductor AIC Extension - Testing Guide

This guide explains how to install the updated Conductor extension, verify the new AIC features (universal indexing, ignore patterns), and understand the token savings.

## 1. Installation

Since this update is currently in a Pull Request (or your fork), you should install it directly from the source to test.

### Option A: Install from your Fork (Recommended)
This ensures you are testing the exact code we just pushed.

1.  **Uninstall existing version (if any):**
    ```bash
    gemini extensions uninstall conductor
    ```

2.  **Install from the fork:**
    ```bash
    gemini extensions install https://github.com/nan-bit/conductor-aic --branch main
    ```

### Option B: Install from Local Directory
If you want to test changes before pushing.

1.  Navigate to the parent directory of this repo.
2.  Run:
    ```bash
    gemini extensions install ./conductor-aic
    ```

## 2. Running Conductor

1.  **Navigate to a project directory** (e.g., the repo you want to work on).
2.  **Initialize Conductor:**
    ```bash
    /conductor:setup
    ```
3.  **Observe the Indexing:**
    During the setup, the agent will announce it is performing "semantic indexing".
    *   **Verify Fix:** Watch the output. It should now index **all text files** (not just Python) but **exclude** `node_modules` and other ignored directories (thanks to the `.gitignore` fix).

## 3. Verifying AIC & Token Savings

The core value of AIC is reducing context size by providing "Rich Skeletons" (summaries) of files instead of raw content.

### How to See it in Action:

1.  **Start a Task:**
    ```bash
    /conductor:newTrack "Update the README to include installation instructions"
    /conductor:implement
    ```

2.  **Watch the Agent's Tool Use:**
    *   As the agent explores the codebase, look for calls to `aic_get_file_context`.
    *   **The Saving:** Instead of calling `read_file` (which loads 100% of the text), it calls `aic_get_file_context`.
    *   **Example:** For a 500-line Python file, `aic_get_file_context` might only return ~50 lines of class/function signatures. This is a **~90% token reduction** for that file interaction.

3.  **Check Session Stats:**
    You can view the total token usage for your current session:
    ```bash
    /stats model
    ```
    *Compare this against a session where you manually `read_file` many large files to see the difference.*

## 4. Updating

If you push more changes to the repo, you can update the extension locally:

```bash
gemini extensions update conductor
```

## 5. Troubleshooting

*   **"Indexed only 1 file":** If this happens, check your `.gitignore`. We now respect it strictly.
*   **"Tool not found":** Ensure you uninstalled the old version and installed the new one. The tool names changed from `index_repo` to `aic_index`.
