import type { Metadata } from 'next';
import '@fontsource/sarabun/thai-400.css';
import '@fontsource/sarabun/thai-600.css';
import '@fontsource/sarabun/latin-400.css';
import '@fontsource/sarabun/latin-600.css';
import './globals.css';
export const metadata: Metadata = { title: 'OmniMed · OPD POC', description: 'OmniMed local OPD foundation. Synthetic demonstration only.' };
export default function RootLayout({ children }: Readonly<{ children: React.ReactNode }>) { return <html lang="th"><body>{children}</body></html>; }
