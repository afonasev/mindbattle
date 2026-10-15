// Run the actual project validator against a proposed topic, without app/audio startup.
const fs = require('node:fs');
const path = require('node:path');
const ts = require('typescript');
require.extensions['.ts'] = (module, filename) => {
  const source = fs.readFileSync(filename, 'utf8');
  const result = ts.transpileModule(source, { compilerOptions: {
    module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022,
    esModuleInterop: true, resolveJsonModule: true,
  }});
  module._compile(result.outputText, filename);
};
const { validateTopicPack } = require(path.resolve(__dirname, '../../../../src/content/validator.ts'));
const topic = JSON.parse(fs.readFileSync(0, 'utf8'));
process.stdout.write(JSON.stringify(validateTopicPack(topic)) + '\n');
