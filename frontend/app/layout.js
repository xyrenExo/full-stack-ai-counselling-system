export const metadata = {
  title: 'AI Counselling System',
  description: 'Your safe space for emotional support'
}

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
}