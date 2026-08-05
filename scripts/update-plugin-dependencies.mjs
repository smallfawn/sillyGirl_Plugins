import { builtinModules, createRequire } from "node:module";
import { mkdtemp, readdir, readFile, rm, writeFile } from "node:fs/promises";
import os from "node:os";
import path from "node:path";
import { spawn } from "node:child_process";

const require = createRequire(import.meta.url);
const root = process.cwd();
const pluginsDir = path.join(root, "plugins");
const pluginExts = new Set([".js", ".py"]);
const nodeBuiltins = new Set([
  ...builtinModules,
  ...builtinModules.map((name) => `node:${name}`),
]);

function commandOutput(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: root,
      shell: process.platform === "win32",
      ...options,
    });
    let stdout = "";
    let stderr = "";
    child.stdout?.on("data", (chunk) => {
      stdout += chunk;
    });
    child.stderr?.on("data", (chunk) => {
      stderr += chunk;
    });
    child.on("error", reject);
    child.on("close", (code) => {
      if (code === 0) {
        resolve(stdout);
        return;
      }
      reject(new Error(`${command} ${args.join(" ")} failed with code ${code}: ${stderr || stdout}`));
    });
  });
}

async function pluginFiles() {
  const files = await readdir(pluginsDir, { withFileTypes: true });
  return files
    .filter((entry) => entry.isFile() && pluginExts.has(path.extname(entry.name).toLowerCase()))
    .map((entry) => path.join(pluginsDir, entry.name))
    .sort((a, b) => a.localeCompare(b));
}

function normalizeNodePackage(value) {
  const text = String(value || "").trim();
  if (!text || text.startsWith(".") || text.startsWith("/") || text.startsWith("\\")) return "";
  if (nodeBuiltins.has(text) || text === "sillygirl") return "";
  const parts = text.split("/");
  if (text.startsWith("@")) return parts.length >= 2 ? `${parts[0]}/${parts[1]}` : "";
  return parts[0];
}

function normalizePythonPackage(value) {
  let text = String(value || "").trim();
  if (!text || text.startsWith(".") || text.startsWith("-")) return "";
  text = text.split(";")[0].trim();
  for (const sep of ["==", ">=", "<=", "~=", "!=", ">", "<"]) {
    const index = text.indexOf(sep);
    if (index >= 0) {
      text = text.slice(0, index);
      break;
    }
  }
  const extraIndex = text.indexOf("[");
  if (extraIndex >= 0) text = text.slice(0, extraIndex);
  text = text.trim().replaceAll("_", "-").toLowerCase();
  return /^[a-z0-9][a-z0-9.-]*$/.test(text) ? text : "";
}

function fallbackNodeDependencies(content) {
  const deps = new Set();
  const patterns = [
    /\brequire\s*\(\s*["']([^"']+)["']\s*\)/g,
    /\bimport\s+(?:[^"']+\s+from\s+)?["']([^"']+)["']/g,
    /\bimport\s*\(\s*["']([^"']+)["']\s*\)/g,
  ];
  for (const pattern of patterns) {
    let match;
    while ((match = pattern.exec(content))) {
      const name = normalizeNodePackage(match[1]);
      if (name) deps.add(name);
    }
  }
  return [...deps];
}

async function scanNodeDependencies(file) {
  const deps = new Set();
  const content = await readFile(file, "utf8");
  try {
    const madge = require("madge");
    const result = await madge(file, {
      baseDir: root,
      includeNpm: true,
      fileExtensions: ["js", "mjs", "cjs"],
    });
    const graph = await result.obj();
    for (const values of Object.values(graph)) {
      for (const item of values || []) {
        const name = normalizeNodePackage(item);
        if (name) deps.add(name);
      }
    }
  } catch (error) {
    console.warn(`madge 扫描失败，改用基础语法扫描：${path.relative(root, file)} ${error.message}`);
  }
  for (const name of fallbackNodeDependencies(content)) deps.add(name);
  return [...deps].sort();
}

async function scanPythonDependencies(file) {
  const temp = await mkdtemp(path.join(os.tmpdir(), "sillygirl-plugin-pipreqs-"));
  try {
    const target = path.join(temp, path.basename(file));
    await writeFile(target, await readFile(file, "utf8"));
    const savePath = path.join(temp, "requirements.txt");
    await commandOutput("pipreqs", [temp, "--force", "--mode", "no-pin", "--savepath", savePath], { cwd: temp });
    const raw = await readFile(savePath, "utf8").catch(() => "");
    const deps = new Set();
    for (const line of raw.split(/\r?\n/)) {
      const clean = line.trim();
      if (!clean || clean.startsWith("#")) continue;
      const name = normalizePythonPackage(clean);
      if (name && name !== "sillygirl") deps.add(name);
    }
    return [...deps].sort();
  } finally {
    await rm(temp, { recursive: true, force: true });
  }
}

function lineForDepe(deps, style = "js") {
  const prefix = style === "python" ? "#" : "//";
  return `${prefix} [depe: ${JSON.stringify(deps)}]`;
}

function updateDepeComment(content, deps) {
  const lines = content.split(/\r?\n/);
  const style = content.includes("from sillygirl import") || content.includes("import middleware") ? "python" : "js";
  const depeLine = lineForDepe(deps, style);
  const existingIndex = lines.findIndex((line) => /^\s*(?:\/\/|#+)\s*\[\s*depe\s*:/i.test(line));
  if (existingIndex >= 0) {
    lines[existingIndex] = depeLine;
    return lines.join("\n");
  }
  let insertAt = 0;
  while (insertAt < lines.length && /^\s*(?:\/\/|#+)\s*\[\s*[\w+-]+\s*:/i.test(lines[insertAt])) {
    insertAt += 1;
  }
  lines.splice(insertAt, 0, depeLine);
  return lines.join("\n");
}

for (const file of await pluginFiles()) {
  const ext = path.extname(file).toLowerCase();
  const deps = ext === ".py" ? await scanPythonDependencies(file) : await scanNodeDependencies(file);
  const content = await readFile(file, "utf8");
  const updated = updateDepeComment(content, deps);
  if (updated !== content) {
    await writeFile(file, updated);
  }
  console.log(`${path.relative(root, file).replaceAll("\\", "/")}: ${JSON.stringify(deps)}`);
}
