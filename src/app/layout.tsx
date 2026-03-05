import type { Metadata } from 'next'
import './globals.css'

export const metadata: Metadata = {
  title: 'Pineapple Bytes - Client Overview Dashboard',
  description: 'Restaurant client monitoring and operational health dashboard',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  )
}
