import type { SiteConfig } from '@mcptoolshop/site-theme';

export const config: SiteConfig = {
  title: 'Portlight',
  description: 'Trade-first maritime strategy game — build a merchant career across five regions through route arbitrage, contracts, infrastructure, finance, and reputation.',
  logoBadge: 'PL',
  brandName: 'Portlight',
  repoUrl: 'https://github.com/mcp-tool-shop-org/portlight',
  footerText: 'MIT Licensed — built by <a href="https://github.com/mcp-tool-shop-org" style="color:var(--color-muted);text-decoration:underline">mcp-tool-shop-org</a>',

  hero: {
    badge: 'v2.0.0',
    headline: 'Portlight',
    headlineAccent: 'Trade. Sail. Prosper.',
    description: 'A trade-first maritime strategy game where you build a merchant career across 20 ports, 5 regions, and 43 routes — with 9 captain types, 4 pirate factions, and 4 victory paths.',
    primaryCta: { href: '#usage', label: 'Get started' },
    secondaryCta: { href: 'handbook/', label: 'Read the Handbook' },
    previews: [
      { label: 'Install', code: 'pip install portlight' },
      { label: 'Play', code: 'portlight new "Captain Hawk" --type merchant' },
      { label: 'Trade', code: 'portlight market && portlight buy grain 10' },
    ],
  },

  sections: [
    {
      kind: 'features',
      id: 'features',
      title: 'Features',
      subtitle: 'A living world of merchant adventure.',
      features: [
        { title: 'Living Economy', desc: 'Prices react to your trades. 20 ports, 18 goods, 43 routes across 5 regions with scarcity-driven pricing. Every port has clear import/export identity.' },
        { title: 'Nine Captains', desc: 'Merchant, Smuggler, Navigator, Privateer, Corsair, Scholar, Merchant Prince, Dockhand, Bounty Hunter. Each starts differently, sees different contracts, and leans toward a different path.' },
        { title: 'Contracts & Provenance', desc: '22 contract templates across 6 families. Trust-gated access. Provenance-validated delivery. Real deadlines with real consequences.' },
        { title: 'Reputation & Heat', desc: 'Four axes — commercial trust, customs heat, regional standing, underworld connections. Honest play opens doors. Risky play pays more but draws attention.' },
        { title: 'Combat & Factions', desc: 'Personal combat with stance triangle, 14 weapons, regional fighting styles. Naval combat. 4 pirate factions controlling different waters.' },
        { title: '1,832 Tests', desc: '14 cross-system invariants, 9 compound stress scenarios, 7-bot balance harness. The game never enters an illegal state.' },
      ],
    },
    {
      kind: 'code-cards',
      id: 'usage',
      title: 'Quick Start',
      cards: [
        { title: 'Install', code: 'pip install portlight\n# or: npx @mcptoolshop/portlight' },
        { title: 'Start a game', code: 'portlight new "Captain Hawk" --type merchant' },
        { title: 'Trade', code: 'portlight market\nportlight buy grain 10\nportlight sail al_manar\nportlight advance\nportlight sell grain 10' },
        { title: 'Build your career', code: 'portlight map\nportlight milestones\nportlight contracts\nportlight print-and-play' },
      ],
    },
  ],
};
