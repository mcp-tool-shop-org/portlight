import type { SiteConfig } from '@mcptoolshop/site-theme';

export const config: SiteConfig = {
  title: 'Portlight',
  description: 'Trade-first maritime strategy game for the terminal. TUI and CLI. Twenty ports, four victory paths.',
  logoBadge: 'PL',
  brandName: 'Portlight',
  repoUrl: 'https://github.com/mcp-tool-shop-org/portlight',
  footerText: 'MIT Licensed — built by <a href="https://mcp-tool-shop.github.io/" style="color:var(--color-muted);text-decoration:underline">MCP Tool Shop</a>',

  hero: {
    badge: 'v2.1.0',
    headline: 'Portlight',
    headlineAccent: 'Trade. Sail. Build a career.',
    description: 'A terminal merchant game where prices move when you sell, contracts want proof, and four victory paths score the career you actually built. Play the TUI or the CLI. Same save.',
    primaryCta: { href: '#usage', label: 'Get started' },
    secondaryCta: { href: 'handbook/', label: 'Read the Handbook' },
    previews: [
      { label: 'Install', code: 'pip install "portlight[tui]"' },
      { label: 'Play', code: 'portlight tui' },
      { label: 'Or CLI', code: 'portlight new "Captain Hawk" --type merchant' },
    ],
  },

  sections: [
    {
      kind: 'features',
      id: 'features',
      title: 'Features',
      subtitle: 'A living merchant world in the terminal.',
      features: [
        { title: 'TUI and CLI', desc: 'Full play in the Textual TUI: harbor, contracts, infra, shipyard, fleet, campaign. CLI for scripts and --json. Same save file.' },
        { title: 'Living economy', desc: '20 ports, 18 goods, 43 routes across 5 regions. Dump grain and the price crashes. Every port has a real import/export identity.' },
        { title: 'Nine captains', desc: 'Merchant through Bounty Hunter. Each starts in a different port, sees different contracts, and leans toward a different victory path.' },
        { title: 'Infrastructure that matters', desc: 'Warehouses, brokers in all five regions, seven licenses. Upkeep is real. W twice in the TUI to lease, deposit, or open an office.' },
        { title: 'Combat with consequences', desc: 'Stance triangle, naval flee/capture, prize hulls you can actually board. Bounty hunt spawns the named captain you accepted.' },
        { title: '1,853 tests', desc: '14 cross-system invariants, 9 compound stress scenarios, 7-bot balance harness. Save format v12 with a full migration chain.' },
      ],
    },
    {
      kind: 'code-cards',
      id: 'usage',
      title: 'Quick Start',
      cards: [
        { title: 'Install', code: 'pip install "portlight[tui]"\n# or: npx @mcptoolshop/portlight' },
        { title: 'TUI', code: 'portlight tui\n# New game if no save. H harbor, K contracts, W infra.' },
        { title: 'CLI trade', code: 'portlight new "Captain Hawk" --type merchant\nportlight buy grain 10\nportlight sail al_manar\nportlight advance\nportlight sell grain 10' },
        { title: 'Career', code: 'portlight map\nportlight milestones\nportlight bounty accept scarlet_ana\nportlight bounty hunt scarlet_ana' },
      ],
    },
  ],
};
