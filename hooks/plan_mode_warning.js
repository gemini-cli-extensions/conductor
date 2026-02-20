#!/usr/bin/env node

/**
 * @license
 * Copyright 2026 Google LLC
 * SPDX-License-Identifier: Apache-2.0
 */

async function main() {
  console.log(
    JSON.stringify({
      systemMessage:
        '⚠️ Conductor manages its own planning lifecycle. For the best Conductor experience, please disable Gemini CLI\'s built-in Plan Mode while using Conductor.'
    }),
  );
}

main();
