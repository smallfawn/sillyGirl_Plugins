#!/usr/bin/env node
import { readdir, readFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const pluginsDir = path.join(root, "plugins");
const indexPath = path.join(root, "publicFileIndex.json");
const validKeys = new Set([
  "title",
  "name",
  "desc",
  "author",
  "version",
  "rule",
  "cron",
  "on_start",
  "web",
  "status",
  "admin",
  "public",
  "priority",
  "class",
  "icon",
  "module",
  "carry",
  "origin",
  "depe",
]);
const required = [
  "title",
  "name",
  "desc",
  "author",
  "version",
  "status",
  "admin",
  "public",
  "priority",
  "class",
  "icon",
  "origin",
  "depe",
];
const booleanKeys = ["status", "admin", "public", "on_start", "web", "module", "carry"];
const activationKeys = ["rule", "cron", "on_start", "web"];
const errors = [];
const removedSenderMethods = new Map([
  ["getContext", "getMsg"],
  ["getMessageId", "getMsgId"],
  ["getContent", "getMsg"],
  ["setContent", "setMsg"],
]);

function parseMetadata(content, filename) {
  const meta = new Map();
  for (const line of content.split(/\r?\n/)) {
    const match = line.match(/^[ \t]*\/\/[ \t]*\[[ \t]*([A-Za-z_]+)[ \t]*:[ \t]*(.*?)[ \t]*\][ \t]*(?:\/\/.*)?$/);
    if (!match) continue;
    const key = match[1].toLowerCase();
    if (!validKeys.has(key)) errors.push(`${filename}: unknown metadata key ${key}`);
    if (!meta.has(key)) meta.set(key, []);
    meta.get(key).push(match[2].trim());
  }
  return meta;
}

function one(meta, key) {
  return meta.get(key)?.[0] ?? "";
}

function bool(meta, key) {
  return one(meta, key).toLowerCase() === "true";
}

function parseDepe(meta, filename) {
  try {
    const value = JSON.parse(one(meta, "depe"));
    if (!Array.isArray(value) || value.some((item) => typeof item !== "string" || !item.trim())) {
      throw new Error("must be a non-empty-string array");
    }
    if (new Set(value).size !== value.length) throw new Error("contains duplicates");
    return value;
  } catch (error) {
    errors.push(`${filename}: invalid depe (${error.message})`);
    return [];
  }
}

const entries = await readdir(pluginsDir, { withFileTypes: true });
const cjsFiles = entries.filter((entry) => entry.isFile() && entry.name.endsWith(".cjs"));
for (const entry of cjsFiles) errors.push(`${entry.name}: .cjs modules are unsupported; use flat .js modules`);
const files = entries
  .filter((entry) => entry.isFile() && entry.name.endsWith(".js"))
  .map((entry) => entry.name)
  .sort((a, b) => a.localeCompare(b));
const plugins = new Map();

for (const filename of files) {
  const content = await readFile(path.join(pluginsDir, filename), "utf8");
  const meta = parseMetadata(content, filename);
  for (const [removed, replacement] of removedSenderMethods) {
    if (new RegExp("\\." + removed + "\\s*\\(").test(content)) {
      errors.push(filename + ": removed Sender API " + removed + "(); use " + replacement + "()");
    }
  }
  if (/\benable\s*:\s*plugin\.Form\.boolean\s*\(/.test(content)) {
    errors.push(`${filename}: generic plugin.Form enable is removed; use [status] metadata`);
  }
  const basename = path.basename(filename, ".js");
  for (const key of required) if (!one(meta, key)) errors.push(`${filename}: missing ${key}`);
  if (one(meta, "name") !== basename) errors.push(`${filename}: name must equal ${basename}`);
  if (!/^v\d+\.\d+\.\d+$/.test(one(meta, "version"))) errors.push(`${filename}: version must use v1.2.3 format`);
  for (const key of booleanKeys) {
    if (meta.has(key) && !/^(true|false)$/i.test(one(meta, key)))
      errors.push(`${filename}: ${key} must be true or false`);
    if ((meta.get(key)?.length || 0) > 1) errors.push(`${filename}: duplicate singleton key ${key}`);
  }
  for (const key of required.filter((key) => key !== "class")) {
    if ((meta.get(key)?.length || 0) > 1) errors.push(`${filename}: duplicate singleton key ${key}`);
  }
  if (!/^-?\d+$/.test(one(meta, "priority"))) errors.push(`${filename}: priority must be an integer`);
  const isModule = bool(meta, "module");
  const active = activationKeys.some((key) => (meta.get(key) || []).some((value) => value && value !== "false"));
  if (isModule && active) errors.push(`${filename}: module must not declare rule/cron/on_start/web activation`);
  if (!isModule && !active) errors.push(`${filename}: missing rule/cron/on_start/web activation`);
  const depe = parseDepe(meta, filename);
  plugins.set(filename, { filename, meta, depe, isModule });
}

for (const plugin of plugins.values()) {
  for (const dependency of plugin.depe.filter((item) => item.startsWith("."))) {
    if (!/^\.\/[A-Za-z0-9_-]+\.js$/.test(dependency)) {
      errors.push(`${plugin.filename}: invalid module dependency ${dependency}`);
      continue;
    }
    const targetName = dependency.slice(2);
    const target = plugins.get(targetName);
    if (!target) errors.push(`${plugin.filename}: missing module dependency ${targetName}`);
    else if (!target.isModule) errors.push(`${plugin.filename}: dependency ${targetName} is not [module: true]`);
  }
}

const visiting = new Set();
const visited = new Set();
function visit(filename, chain = []) {
  if (visiting.has(filename)) {
    errors.push(`module dependency cycle: ${[...chain, filename].join(" -> ")}`);
    return;
  }
  if (visited.has(filename)) return;
  visiting.add(filename);
  const plugin = plugins.get(filename);
  for (const dependency of plugin?.depe.filter((item) => item.startsWith(".")) || []) {
    const target = dependency.slice(2);
    if (plugins.has(target)) visit(target, [...chain, filename]);
  }
  visiting.delete(filename);
  visited.add(filename);
}
for (const filename of files) visit(filename);

const index = JSON.parse(await readFile(indexPath, "utf8"));
const indexEntries = Object.values(index);
if (indexEntries.length !== files.length)
  errors.push(`index count ${indexEntries.length} != plugin count ${files.length}`);
const indexedPaths = new Set(indexEntries.map((entry) => entry.path));
for (const filename of files)
  if (!indexedPaths.has(`plugins/${filename}`)) errors.push(`${filename}: missing from publicFileIndex.json`);
for (const entry of indexEntries) {
  const filename = String(entry.path || "").replace(/^plugins\//, "");
  const plugin = plugins.get(filename);
  if (!plugin) {
    errors.push(`${entry.path}: stale index entry`);
    continue;
  }
  if (Boolean(entry.module) !== plugin.isModule) errors.push(`${filename}: index module flag mismatch`);
  for (const key of ["status", "public", "admin", "on_start", "web", "carry"]) {
    if (Boolean(entry[key]) !== bool(plugin.meta, key)) errors.push(`${filename}: index ${key} flag mismatch`);
  }
  const npm = plugin.depe.filter((item) => !item.startsWith("."));
  const modules = plugin.depe.filter((item) => item.startsWith("."));
  if (JSON.stringify(entry.dependencies || []) !== JSON.stringify(npm))
    errors.push(`${filename}: index dependencies mismatch`);
  if (JSON.stringify(entry.module_dependencies || []) !== JSON.stringify(modules))
    errors.push(`${filename}: index module_dependencies mismatch`);
}

const summary = {
  plugins: files.length,
  modules: [...plugins.values()].filter((plugin) => plugin.isModule).length,
  npm_dependency_edges: [...plugins.values()].flatMap((plugin) => plugin.depe.filter((item) => !item.startsWith(".")))
    .length,
  module_dependency_edges: [...plugins.values()].flatMap((plugin) => plugin.depe.filter((item) => item.startsWith(".")))
    .length,
  errors: errors.length,
};
console.log(JSON.stringify(summary, null, 2));
if (errors.length) {
  console.error(errors.map((error) => `ERROR\t${error}`).join("\n"));
  process.exitCode = 1;
}
