import type { ReviewEntry } from "./types";

const reviewModules = import.meta.glob("./reviews/*.json", {
  eager: true,
  import: "default"
}) as Readonly<Record<string, ReviewEntry>>;

export const contentReviews: readonly ReviewEntry[] = Object.values(reviewModules);
