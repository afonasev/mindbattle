const fs = require('node:fs/promises');
const path = require('node:path');
module.exports = async (context) => {
    const root = context.electronPlatformName === 'darwin' ? path.join(context.appOutDir, 'Mindbattle.app') : context.appOutDir;
    const resources = context.electronPlatformName === 'darwin' ? 'Contents/Resources' : 'resources';
    const paths = [];
    async function walk(dir, rel = '') { for (const e of await fs.readdir(dir, { withFileTypes: true })) {
        const name = rel ? `${rel}/${e.name}` : e.name;
        if (e.isDirectory())
            await walk(path.join(dir, e.name), name);
        else
            paths.push(name);
    } }
    await walk(root);
    if (context.electronPlatformName === 'darwin') {
        const base = "Contents/Frameworks/Electron Framework.framework/Versions/A/Resources/v8_context_snapshot.";
        for (const arch of ["x86_64", "arm64"]) {
            const name = base + arch + ".bin";
            if (!paths.includes(name))
                paths.push(name);
        }
    }
    paths.sort();
    await fs.writeFile(path.join(root, resources, 'mindbattle-layout.json'), JSON.stringify({ product: 'tech.afonasev.mindbattle', paths }));
};
