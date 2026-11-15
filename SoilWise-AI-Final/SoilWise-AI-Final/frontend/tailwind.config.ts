import type { Config } from "tailwindcss";
const config: Config = { content: ["./app/**/*.{js,ts,jsx,tsx}"], theme: { extend: { colors: { soil: "#6b4f35", leaf: "#2f855a" } } }, plugins: [] };
export default config;
