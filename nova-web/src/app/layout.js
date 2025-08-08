import "./globals.css";
import Shell from "@/components/Shell";

export const metadata = {
  title: "superNova_2177",
  description: "Prototype UI — symbolic only",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <Shell>{children}</Shell>
      </body>
    </html>
  );
}
