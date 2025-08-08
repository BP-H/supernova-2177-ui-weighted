export const metadata = {
  title: "superNova_2177",
  description: "Prototype feed — symbolic only",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-[#0b0b0e] text-white antialiased">{children}</body>
    </html>
  );
}
