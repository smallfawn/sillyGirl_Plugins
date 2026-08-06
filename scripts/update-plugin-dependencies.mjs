import { builtinModules } from "node:module";
import { readdir, readFile, writeFile } from "node:fs/promises";
import path from "node:path";
import { spawn } from "node:child_process";

const root = process.cwd();
const pluginsDir = path.join(root, "plugins");
const checkOnly = process.argv.includes("--check");
const pluginExts = new Set([".js", ".py"]);
const nodeBuiltins = new Set([
  ...builtinModules,
  ...builtinModules.map((name) => `node:${name}`),
]);

function commandOutput(command, args, options = {}) {
  return new Promise((resolve, reject) => {
    const child = spawn(command, args, {
      cwd: root,
      shell: false,
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

const pythonPackageNames = new Map([
  ["bs4", "beautifulsoup4"], ["Crypto", "pycryptodome"], ["Cryptodome", "pycryptodomex"],
  ["cv2", "opencv-python"], ["dateutil", "python-dateutil"], ["jwt", "pyjwt"],
  ["PIL", "pillow"], ["sklearn", "scikit-learn"], ["yaml", "pyyaml"],
]);

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
  return fallbackNodeDependencies(await readFile(file, "utf8")).sort();
}

async function scanPythonDependencies(file) {
  const scanner = [
    "import ast,json,pathlib,sys",
    "tree=ast.parse(pathlib.Path(sys.argv[1]).read_text(encoding='utf-8'))",
    "names={a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}",
    "names|={n.module.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module}",
    "print(json.dumps(sorted(names-set(sys.stdlib_module_names)-{'sillygirl'})))",
  ].join(";");
  const imports = JSON.parse(await commandOutput(process.env.PYTHON || "python", ["-c", scanner, file]));
  return [...new Set(imports.map((name) => pythonPackageNames.get(name) || normalizePythonPackage(name)).filter(Boolean))].sort();
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

const stale = [];
for (const file of await pluginFiles()) {
  const ext = path.extname(file).toLowerCase();
  const deps = ext === ".py" ? await scanPythonDependencies(file) : await scanNodeDependencies(file);
  const content = await readFile(file, "utf8");
  const updated = updateDepeComment(content, deps);
  if (updated !== content) {
    if (checkOnly) stale.push(path.relative(root, file).replaceAll("\\", "/"));
    else await writeFile(file, updated);
  }
  console.log(`${path.relative(root, file).replaceAll("\\", "/")}: ${JSON.stringify(deps)}`);
}
if (stale.length) {
  throw new Error(`依赖注释需要更新：\n${stale.join("\n")}`);
}
