export const metadata = {
  title: 'superNova_2177',
  description: 'Symbolic social — layout test',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body style={{ background: '#0b0c10', color: '#e6edf3', fontFamily: 'ui-sans-serif, system-ui' }}>
        {children}
      </body>
    </html>
  );
}
