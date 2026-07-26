import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const pluginsDir = path.join(root, "plugins");
const repo = process.env.GITHUB_REPOSITORY || "smallfawn/sillyGirl_Plugins";
const branch = process.env.GITHUB_REF_NAME || "main";
const repoUrl = `https://github.com/${repo}`;

function parseMeta(content) {
  const meta = {};
  const block = content.match(/\/\*\*([\s\S]*?)\*\//)?.[1] || "";
  for (const line of block.split(/\r?\n/)) {
    const match = line.match(/^\s*\*\s*@([\w+-]+)\s+(.+?)\s*$/);
    if (match) meta[match[1]] = match[2];
  }
  return meta;
}

function pluginId(seed) {
  const hash = createHash("md5").update(seed).digest("hex");
  return `${hash.slice(0, 8)}-${hash.slice(8, 12)}-${hash.slice(12, 16)}-${hash.slice(16, 20)}-${hash.slice(20)}`;
}

const builtinModules = new Set([
  "assert", "async_hooks", "buffer", "child_process", "cluster", "console", "constants", "crypto", "dgram",
  "diagnostics_channel", "dns", "domain", "events", "fs", "http", "http2", "https", "inspector", "module",
  "net", "os", "path", "perf_hooks", "process", "punycode", "querystring", "readline", "repl", "stream",
  "string_decoder", "timers", "tls", "trace_events", "tty", "url", "util", "v8", "vm", "wasi",
  "worker_threads", "zlib",
]);

function normalizeDependencyName(value) {
  value = String(value || "").trim();
  if (!value || value.startsWith(".") || value.startsWith("/") || value.startsWith("node:")) return "";
  if (value === "sillygirl" || builtinModules.has(value)) return "";
  const parts = value.split("/");
  if (value.startsWith("@")) return parts.length >= 2 ? `${parts[0]}/${parts[1]}` : "";
  return parts[0];
}

function parseDependencies(content) {
  const deps = new Set();
  const re = /\brequire\s*\(\s*["']([^"']+)["']\s*\)/g;
  let match;
  while ((match = re.exec(content))) {
    const name = normalizeDependencyName(match[1]);
    if (name) deps.add(name);
  }
  return Object.fromEntries([...deps].sort().map((name) => [name, "latest"]));
}

const files = await readdir(pluginsDir, { withFileTypes: true });
const pluginFiles = files
  .filter((entry) => entry.isFile() && entry.name.toLowerCase().endsWith(".js"))
  .map((entry) => path.join(pluginsDir, entry.name))
  .sort((a, b) => a.localeCompare(b));

const result = {};
for (const pluginFile of pluginFiles) {
  const relativePath = path.relative(root, pluginFile).replaceAll("\\", "/");
  const content = await readFile(pluginFile, "utf8");
  const meta = parseMeta(content);
  const pluginName = path.basename(pluginFile, path.extname(pluginFile));
  const author = meta.author || repo.split("/")[0];
  const id = pluginId(`${repo}@${branch}/${relativePath}`);
  const rawBase = `https://raw.githubusercontent.com/${repo}/${branch}`;
  result[id] = {
    id,
    title: meta.title || pluginName,
    author,
    version: meta.version || "v1.0.0",
    desc: meta.desc || "",
    class: meta.class || "",
    rule: meta.rule || "",
    public: meta.public === "true",
    admin: meta.admin === "true",
    path: relativePath,
    raw: `${rawBase}/${relativePath}`,
    dependencies: parseDependencies(content),
    type: "node",
    origin: repoUrl,
  };
}

await writeFile(path.join(root, "publicFileIndex.json"), JSON.stringify(result, null, 2) + "\n");
console.log(`Generated publicFileIndex.json with ${Object.keys(result).length} plugins.`);
