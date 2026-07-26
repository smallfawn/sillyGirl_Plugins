import { createHash } from "node:crypto";
import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";

const root = process.cwd();
const pluginsDir = path.join(root, "plugins");
const repo = process.env.GITHUB_REPOSITORY || "smallfawn/sillyGirl_Plugins";
const branch = process.env.GITHUB_REF_NAME || "main";
const repoUrl = `https://github.com/${repo}`;
const pluginExts = new Set([".js", ".py"]);

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

function pluginType(file) {
  return path.extname(file).toLowerCase() === ".py" ? "python" : "node";
}

function parseDependencies(value) {
  if (!value) return [];
  try {
    const parsed = JSON.parse(value);
    if (!Array.isArray(parsed)) return [];
    return [...new Set(parsed.map((item) => String(item || "").trim()).filter(Boolean))].sort();
  } catch {
    return [];
  }
}

const files = await readdir(pluginsDir, { withFileTypes: true });
const pluginFiles = files
  .filter((entry) => entry.isFile() && pluginExts.has(path.extname(entry.name).toLowerCase()))
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
    dependencies: parseDependencies(meta.depe),
    type: meta.type || pluginType(pluginFile),
    origin: repoUrl,
  };
}

await writeFile(path.join(root, "publicFileIndex.json"), JSON.stringify(result, null, 2) + "\n");
console.log(`Generated publicFileIndex.json with ${Object.keys(result).length} plugins.`);
