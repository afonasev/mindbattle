export function gameLaunchUrl(origin, muted = false) {
    const url = new URL(origin.endsWith("/") ? origin : `${origin}/`);
    if (muted) url.searchParams.set("muted", "1");
    return url.toString();
}

export function isMutedLaunch(argv = process.argv) {
    return argv.includes("-muted") || argv.includes("--muted");
}
