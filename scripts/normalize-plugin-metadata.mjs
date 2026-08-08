#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const VALID = new Set([
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
const ORDER = [
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
];
const args = process.argv.slice(2);
const write = args.includes("--write");
const repo = path.resolve(valueAfter("--repo") || path.join(import.meta.dirname, ".."));
const mappingPath = valueAfter("--mapping");
const pluginDir = path.join(repo, "plugins");
const mapping = loadMapping(mappingPath);
const files = fs
  .readdirSync(pluginDir)
  .filter((name) => name.endsWith(".js"))
  .sort((a, b) => a.localeCompare(b, "zh-CN"));
const changes = [];
const problems = [];

for (const filename of files) {
  const fullPath = path.join(pluginDir, filename);
  const original = fs.readFileSync(fullPath, "utf8").replace(/^\uFEFF/, "");
  const parsed = splitHeader(original);
  const values = collect(parsed.metadata);
  normalize(values, filename, mapping.get(filename) || []);
  const header = render(values);
  const next = `${header}\n\n${parsed.body.replace(/^\s+/, "")}`.replace(/\s+$/, "") + "\n";
  validate(values, filename, problems);
  if (next !== original) {
    changes.push(filename);
    if (write) fs.writeFileSync(fullPath, next, "utf8");
  }
}

console.log(
  JSON.stringify(
    { mode: write ? "write" : "check", files: files.length, changed: changes.length, problems: problems.length },
    null,
    2,
  ),
);
if (changes.length) console.log(changes.map((name) => `${write ? "UPDATED" : "WOULD_UPDATE"}\t${name}`).join("\n"));
if (problems.length) {
  console.error(problems.map((item) => `ERROR\t${item}`).join("\n"));
  process.exitCode = 1;
}
if (!write && changes.length) process.exitCode = 2;

function valueAfter(flag) {
  const index = args.indexOf(flag);
  return index >= 0 ? args[index + 1] : "";
}

function loadMapping(filename) {
  const result = new Map();
  if (!filename || !fs.existsSync(filename)) return result;
  const data = JSON.parse(fs.readFileSync(filename, "utf8"));
  for (const item of data.resolved || []) {
    if (!item?.target?.endsWith?.(".js") || !item.python) continue;
    if (!result.has(item.target)) result.set(item.target, []);
    result.get(item.target).push(item.python);
  }
  return result;
}

function splitHeader(text) {
  const lines = text.split(/\r?\n/);
  const metadata = [];
  let end = 0;
  for (; end < lines.length; end++) {
    const line = lines[end];
    if (!line.trim() || /^\s*\/\//.test(line)) {
      const match = line.match(/^\s*\/\/\s*\[\s*([A-Za-z_]+)\s*:\s*(.*?)\s*\]\s*(?:\/\/.*)?$/);
      if (match) metadata.push({ key: match[1].toLowerCase(), value: match[2].trim() });
      continue;
    }
    break;
  }
  return { metadata, body: lines.slice(end).join("\n") };
}

function collect(entries) {
  const values = new Map();
  for (const { key, value } of entries) {
    if (!values.has(key)) values.set(key, []);
    values.get(key).push(value);
  }
  return values;
}

function first(values, key, fallback = "") {
  return values.get(key)?.find((value) => value !== "") ?? fallback;
}

function setOne(values, key, value) {
  values.set(key, [String(value)]);
}

function normalize(values, filename, pythonSources) {
  const base = path.basename(filename, ".js");
  setOne(values, "title", first(values, "title", base));
  setOne(values, "name", first(values, "name", base));
  setOne(values, "desc", first(values, "desc", first(values, "description", `${first(values, "title", base)}插件`)));
  setOne(values, "author", first(values, "author", "sillyGirl"));
  setOne(values, "version", normalizeVersion(first(values, "version", "v1.0.0")));
  for (const activation of ["rule", "cron", "on_start", "web"]) {
    values.set(
      activation,
      (values.get(activation) || []).filter((value) => value !== ""),
    );
  }
  const disabled = /^(true|1|yes|on)$/i.test(first(values, "disable", "false"));
  setOne(values, "status", first(values, "status", disabled ? "false" : "true"));
  setOne(values, "admin", first(values, "admin", "false"));
  setOne(values, "public", first(values, "public", "true"));
  setOne(values, "priority", first(values, "priority", "0"));
  values.set("class", (values.get("class") || ["其他"]).filter(Boolean));
  setOne(values, "icon", first(values, "icon", "https://api.iconify.design/lucide:bot.svg"));
  if (values.has("module")) setOne(values, "module", first(values, "module", "true"));
  if (values.has("carry")) setOne(values, "carry", first(values, "carry", "true"));
  const source = pythonSources.length ? pythonSources.map((name) => `backup/${name}`).join(";") : "自定义";
  setOne(values, "origin", first(values, "origin", source));
  setOne(values, "depe", first(values, "depe", "[]"));
  for (const key of [...values.keys()]) if (!VALID.has(key)) values.delete(key);
}

function normalizeVersion(value) {
  const text = String(value || "").trim();
  const match = text.match(/^v?(\d+)\.(\d+)(?:\.(\d+))?(?:-js)?$/i);
  return match ? `v${match[1]}.${match[2]}.${match[3] || "0"}` : text;
}

function render(values) {
  const lines = [];
  for (const key of ORDER) {
    for (const value of values.get(key) || []) lines.push(`// [${key}: ${value}]`);
  }
  return lines.join("\n");
}

function validate(values, filename, errors) {
  for (const required of [
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
  ]) {
    if (!first(values, required)) errors.push(`${filename}: missing ${required}`);
  }
  if (!/^v\d+\.\d+\.\d+$/.test(first(values, "version"))) errors.push(`${filename}: version must use v1.2.3 format`);
  const active = ["rule", "cron", "on_start", "web", "module"].some((key) =>
    (values.get(key) || []).some((value) => value !== "" && !/^false$/i.test(value)),
  );
  if (!active) errors.push(`${filename}: missing rule/cron/on_start/web/module activation`);
}
