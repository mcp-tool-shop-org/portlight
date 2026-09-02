const { test } = require("node:test");
const assert = require("node:assert/strict");
const pkg = require("../package.json");

test("npm wrapper version is semver", () => {
  assert.match(pkg.version, /^\d+\.\d+\.\d+$/);
});

test("launcher pin matches package version", () => {
  const fs = require("fs");
  const path = require("path");
  const src = fs.readFileSync(path.join(__dirname, "..", "bin", "portlight.js"), "utf8");
  assert.match(src, new RegExp(`version: "${pkg.version}"`));
  assert.match(src, new RegExp(`tag: "v${pkg.version}"`));
});
