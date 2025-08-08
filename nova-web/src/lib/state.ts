"use client";

import { useEffect, useState } from "react";

type AppState = {
  species: "human" | "company" | "ai";
  decisionKind: "standard" | "important";
  backendUrl: string;
  useRealBackend: boolean;
};

const DEFAULTS: AppState = {
  species: "human",
  decisionKind: "standard",
  backendUrl: process.env.NEXT_PUBLIC_BACKEND_URL || "",
  useRealBackend: false,
};

const KEY = "sn2177:state";

export function useAppState() {
  const [state, setState] = useState<AppState>(DEFAULTS);

  useEffect(() => {
    try {
      const raw = localStorage.getItem(KEY);
      if (raw) setState({ ...DEFAULTS, ...JSON.parse(raw) });
    } catch {}
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch {}
  }, [state]);

  return {
    state,
    setState,
    set<K extends keyof AppState>(key: K, val: AppState[K]) {
      setState((s) => ({ ...s, [key]: val }));
    },
  };
}
