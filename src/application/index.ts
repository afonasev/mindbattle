export * from "./contentContext";
export * from "./gameController";
export * from "./soloController";

export interface ApplicationClock {
  now(): number;
}
