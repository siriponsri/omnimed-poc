'use client';
import { useEffect, useState } from 'react';
import Link from 'next/link';
import { copy, getWorkspace, workspaces, type Locale, type RoleId } from '../lib/workspaces';
import { parseReadiness } from '../lib/readiness';

export default function Home() {
  const [role, setRole] = useState<RoleId>('R-REG');
  const [locale, setLocale] = useState<Locale>('th');
  const [panel, setPanel] = useState<'workspace' | 'system'>('workspace');
  const [health, setHealth] = useState<'idle' | 'checking' | 'ready' | 'unavailable'>('idle');
  const workspace = getWorkspace(role)!;
  const t = copy[locale];
  useEffect(() => { document.documentElement.lang = locale; }, [locale]);
  async function checkHealth() {
    setHealth('checking');
    try {
      const response = await fetch('/api/status', { cache: 'no-store', signal: AbortSignal.timeout(6000) });
      setHealth(parseReadiness(response.ok, await response.json()).status);
    } catch { setHealth('unavailable'); }
  }
  const statusText = health === 'idle' ? t.notChecked : health === 'checking' ? t.checking : health === 'ready' ? t.ready : t.unavailable;
  return <>
    <a className="skip" href="#main">{t.skip}</a>
    <header className="topbar">
      <Link className="brand" href="/" aria-label="OmniMed home"><span className="brand-mark" aria-hidden="true">+</span><strong>OmniMed</strong></Link>
      <span className="site-label">OPD / <span>Solo POC</span></span>
      <span className="top-spacer" />
      <span className="version">v0.1</span>
      <button className="language" onClick={() => setLocale(locale === 'th' ? 'en' : 'th')} aria-label={locale === 'th' ? 'Switch to English' : 'เปลี่ยนเป็นภาษาไทย'}>{locale === 'th' ? 'EN' : 'ไทย'}</button>
    </header>
    <div className="demo-strip"><b>{t.banner}</b><span>{t.bannerDetail}</span></div>
    <div className="app-layout">
      <aside className="sidebar">
        <label className="eyebrow" htmlFor="role">{t.role}</label>
        <select id="role" value={role} onChange={(event) => { const next = getWorkspace(event.target.value); if (next) { setRole(next.id); setPanel('workspace'); } }}>
          {workspaces.map((w) => <option key={w.id} value={w.id}>{w.name[locale]} · {w.id}</option>)}
        </select>
        <p className="preview-note">{t.identity}</p>
        <nav aria-label={t.workspace}>
          <div className="nav-label">{t.workspace}</div>
          <button className={`nav-item ${panel === 'workspace' ? 'selected' : ''}`} aria-current={panel === 'workspace' ? 'page' : undefined} onClick={() => setPanel('workspace')}><span>{workspace.title[locale]}</span><small>{workspace.module}</small></button>
          <button className={`nav-item ${panel === 'system' ? 'selected' : ''}`} aria-current={panel === 'system' ? 'page' : undefined} onClick={() => setPanel('system')}><span>{t.overview}</span><small>M0</small></button>
        </nav>
        <div className="sidebar-foot"><span className="synthetic-mark" aria-hidden="true">◇</span>{t.local}</div>
      </aside>
      <main id="main" tabIndex={-1}>
        <div className="breadcrumb">OPD <span>/</span> {workspace.name[locale]}</div>
        <div className="page-heading"><div><h1>{panel === 'workspace' ? workspace.title[locale] : t.overview}</h1><p>{panel === 'workspace' ? workspace.scope[locale] : t.runtimeHint}</p></div><span className="stage-tag">{panel === 'workspace' ? `${workspace.milestone} · ${t.planned}` : 'M0'}</span></div>
        {panel === 'workspace' ? <>
          {workspace.clinicalHeader && <section className="patient-header" aria-label={t.patient}><span className="patient-symbol" aria-hidden="true">—</span><div><b>{t.patient}</b><p>{t.patientHint}</p></div><span className="patient-id">HN — / VN —</span></section>}
          <div className="worklist-toolbar"><h2>{t.workspace}</h2><button className="primary" disabled aria-describedby="feature-state">{workspace.action[locale]}</button></div>
          <section className="worklist" aria-label={workspace.title[locale]}>
            <div className="table-scroll" tabIndex={0} role="region" aria-label={workspace.title[locale]}><table><caption className="sr-only">{workspace.title[locale]}</caption><thead><tr>{workspace.columns.map((c) => <th key={c.en} scope="col">{c[locale]}</th>)}</tr></thead><tbody><tr><td colSpan={workspace.columns.length}><div className="empty-state"><span className="empty-icon" aria-hidden="true">≡</span><h3>{t.noRecords}</h3><p id="feature-state">{t.emptyHint}</p><span className="empty-label">{t.emptyStatus}</span></div></td></tr></tbody></table></div>
            <div className="worklist-foot"><span>{workspace.module}</span><span>{workspace.id} · {t.planned}</span></div>
          </section>
          <section className="next-flow"><h2>{t.journey}</h2><ol>{(locale === 'th' ? ['ทะเบียน', 'คัดกรอง', 'ห้องตรวจ', 'แล็บ / เภสัชกรรม', 'การเงิน'] : ['Registration', 'Triage', 'Doctor', 'Lab / Pharmacy', 'Finance']).map((label, i) => <li key={label}><span>{String(i + 1).padStart(2, '0')}</span>{label}</li>)}</ol><p>{t.planned} · M1–M5</p></section>
        </> : <section className="system-panel"><h2>{t.runtime}</h2><div className="connection-row"><div><b>{t.backend}</b><p>FastAPI / PostgreSQL</p></div><span className={`connection-state ${health}`} role="status" aria-live="polite">{statusText}</span><button className="secondary" disabled={health === 'checking'} onClick={checkHealth}>{t.refresh}</button></div><p className="system-note">{t.runtimeHint}</p><div className="handoff-note"><h3>{t.guide}</h3><p>{t.guideDetail}</p></div></section>}
        <footer className="main-foot"><span>OmniMed / Foundation</span><span>{t.local}</span></footer>
      </main>
    </div>
  </>;
}
