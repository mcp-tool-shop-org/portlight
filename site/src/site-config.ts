import type { SiteConfig } from '@mcptoolshop/site-theme';

export const config: SiteConfig = {
  title: 'Portlight',
  description: 'Trade-first maritime strategy CLI — route arbitrage, contracts, infrastructure, finance, and commercial reputation across a living regional economy.',
  logoBadge: 'PL',
  brandName: 'Portlight',
  repoUrl: 'https://github.com/mcp-tool-shop-org/portlight',
  footerText: 'MIT Licensed — built by <a href="https://github.com/mcp-tool-shop-org" style="color:var(--color-muted);text-decoration:underline">mcp-tool-shop-org</a>',

  hero: {
    badge: 'Alpha',
    headline: 'Portlight',
    headlineAccent: 'Trade. Sail. Prosper.',
    description: 'A trade-first maritime strategy CLI where you build a merchant career through route arbitrage, contracts, infrastructure, finance, and commercial reputation across a living regional economy.',
    primaryCta: { href: '#usage', label: 'Get started' },
    secondaryCta: { href: 'handbook/', label: 'Read the Handbook' },
    previews: [
      { label: 'Install', code: 'pip install -e ".[dev]"' },
      { label: 'Play', code: 'portlight new "Captain Hawk" --type merchant' },
      { label: 'Trade', code: 'portlight market && portlight buy grain 10' },
    ],
  },

  sections: [
    {
      kind: 'features',
      id: 'features',
      title: 'Features',
      subtitle: 'What makes Portlight different.',
      features: [
        { title: 'Living Economy', desc: 'Prices react to your trades. Dump grain and the price crashes. 10 ports, 8 goods, 17 routes with scarcity-driven pricing.' },
        { title: 'Contracts & Provenance', desc: '6 contract families with provenance-validated delivery. Cargo is tracked from purchase to destination — no faking it.' },
        { title: 'Infrastructure', desc: 'Warehouses, broker offices, and licenses change how you trade. Real upkeep — assets that aren\'t maintained close.' },
        { title: 'Finance with Teeth', desc: 'Credit accelerates your moves. Insurance protects your cargo. Default on payments and doors close.' },
        { title: 'Career Interpretation', desc: '27 milestones, 7 profile tags, 4 victory paths. The game reads what you built and tells you what kind of trade house you are.' },
        { title: 'Stress-Tested Truth', desc: '609 tests, 14 cross-system invariants, 9 compound stress scenarios. The game never enters an illegal state.' },
      ],
    },
    {
      kind: 'code-cards',
      id: 'usage',
      title: 'Quick Start',
      cards: [
        { title: 'Install', code: 'pip install -e ".[dev]"' },
        { title: 'Start a game', code: 'portlight new "Captain Hawk" --type merchant' },
        { title: 'Trade', code: 'portlight market\nportlight buy grain 10\nportlight sail al_manar\nportlight advance\nportlight sell grain 10' },
        { title: 'Build your career', code: 'portlight milestones\nportlight warehouse lease depot\nportlight contracts\nportlight guide' },
      ],
    },
  ],
};
