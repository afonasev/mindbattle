export * from "./contentContext";
export * from "./gameController";

export interface ApplicationClock {
  now(): number;
}
