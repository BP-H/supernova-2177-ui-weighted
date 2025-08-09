import './globals.css';

export const metadata = {
  title: 'superNova_2177',
  description: 'Mathematically sucked into a void of innovation',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="bg-nova-dark text-white">{children}</body>
    </html>
  );
}
