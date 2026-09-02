#!/usr/bin/env node
"use strict";

// version/tag refer to the GitHub Release binary, not this npm wrapper.
process.env.MCPTOOLSHOP_LAUNCH_CONFIG = JSON.stringify({
  toolName: "portlight",
  owner: "mcp-tool-shop-org",
  repo: "portlight",
  version: "2.1.0",
  tag: "v2.1.0",
});

require("@mcptoolshop/npm-launcher/bin/mcptoolshop-launch.js");
