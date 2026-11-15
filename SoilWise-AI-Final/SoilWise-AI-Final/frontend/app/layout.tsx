import "./globals.css";
import type { Metadata } from "next";
import { PwaRegister } from "./pwa-register";
export const metadata: Metadata = {
  title: "SoilWise — Soil health, made simple",
  description: "Soil analysis and crop advisory for farmers.",
  manifest: "/manifest.json",
  themeColor: "#2f855a"
};
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body><PwaRegister />{children}</body></html>;
}
