<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="600" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/portlight/"><img src="https://img.shields.io/pypi/v/portlight" alt="PyPI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-handbook-blue" alt="Handbook"></a>
</p>

Juego de estrategia marítima centrado en el comercio. Construye una carrera como comerciante en cinco regiones a través de la optimización de rutas, contratos, infraestructura, finanzas y reputación, todo desde la terminal.

## Instalación

```bash
pip install portlight
```

¿No tienes Python? Utiliza el envoltorio npm en su lugar:

```bash
npx @mcptoolshop/portlight
```

## ¿Por qué Portlight?

La mayoría de los juegos de comercio simplifican el comercio a un número que simplemente aumenta. Portlight trata el comercio como una disciplina comercial:

- **Los precios reaccionan a tus transacciones.** Si vendes grano en un puerto, el precio se desploma. Cada venta altera el mercado local.
- **Los puertos tienen identidades económicas reales.** Porto Novo produce grano a bajo costo. Silk Haven exporta seda en grandes cantidades. Estas son características estructurales, no aleatorias.
- **Los viajes implican riesgos.** Tormentas, piratas, inspecciones, peligros estacionales. Tus provisiones, el casco y la tripulación son importantes.
- **Los contratos requieren pruebas.** Entrega los productos correctos al puerto correcto antes de la fecha límite. Se rastrea el origen de los productos.
- **La infraestructura cambia la forma en que operas.** Los almacenes almacenan la carga. Los corredores mejoran los contratos. Las licencias desbloquean acceso premium.
- **La reputación abre y cierra puertas.** Confianza comercial, escrutinio aduanero, posición regional y conexiones con el hampa: cuatro factores que influyen en lo que puedes hacer y dónde.
- **El juego analiza lo que has construido.** Tu historial comercial, infraestructura, reputación y rutas forman un perfil de carrera. Hay cuatro caminos distintos hacia la victoria, basados en el tipo de comerciante en el que te has convertido.

## El Mundo

Cinco regiones. Veinte puertos. Cuarenta y tres rutas. Una economía dinámica.

| Región | Puertos | Personaje |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Mercados de grano, madera y especias. Aguas de inicio seguras. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Hierro, armas, comercio militar. Inspecciones estrictas. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Algodón, ron, perlas. Provisiones más baratas. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Seda, especias, porcelana, té. Márgenes más altos. Riesgo de monzones. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Perlas, medicinas. Aguas remotas para la fase final del juego. |

Hay 134 personajes no jugables (PNJ) nombrados en cada puerto. Cuatro facciones piratas que controlan diferentes áreas. Clima estacional que altera el peligro y la demanda. Una capa cultural con festivales, supersticiones y moral de la tripulación.

## Nueve Capitanes

| Capitán | Hogar | Ventaja | Compromiso |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Mejores precios, la confianza crece rápidamente. | Penalizaciones por "calor" duplicadas. |
| **Smuggler** | Corsair's Rest | Mercado negro, comercio de contrabando. | Mayor "calor", más inspecciones. |
| **Navigator** | Monsoon Reach | Barcos más rápidos, mayor alcance. | Posición inicial más débil. |
| **Privateer** | Ironhaven | Combate naval, ventaja en abordajes. | Mala reputación comercial. |
| **Corsair** | Corsair's Rest | Combate equilibrado + comercio. | Maestro de nada. |
| **Scholar** | Jade Port | Ventaja de información, mejores contratos. | Poco capital, frágil. |
| **Merchant Prince** | Porto Novo | Alto capital inicial, acceso premium. | Tarifas más altas, objetivo de piratas. |
| **Dockhand** | Crosswind Isle | Tripulación más barata, ingeniosa. | Capital inicial más bajo. |
| **Bounty Hunter** | Stormwall | Dominio del combate, posición de facción. | Precios bajos, desconfianza. |

Cada capitán comienza en un puerto diferente, ve contratos diferentes y tiende hacia un camino diferente hacia la victoria. El juego no te limita; observa lo que haces y te dice lo que has construido.

## Ciclo Principal

```
Inspect market → Buy cargo → Sail → Sell → Reinvest → Build access → Pursue destiny
```

## Comienzo rápido

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight routes
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight milestones
```

Consulte [docs/START_HERE.md](docs/START_HERE.md) para una primera sesión guiada.

## Sistemas

**Economía** — Precios determinados por la escasez en 20 puertos, 18 productos, 43 rutas. Las penalizaciones por inundaciones castigan el vertido. Los shocks del mercado crean oportunidades. Los modificadores regionales de demanda significan que cada puerto tiene una identidad clara de importación/exportación.

**Viajes** — Viajes de varios días con clima, encuentros con piratas e inspecciones. Las provisiones se consumen diariamente. El casco sufre daños. La moral de la tripulación varía. Las zonas de peligro estacionales cambian las rutas seguras.

**Contratos** — Seis familias, cada una con sus propios requisitos de confianza y reputación. Adquisiciones, alivio de escasez, productos de lujo discretos, flete de retorno, rutas fijas y comisiones de facciones. Plazos reales, consecuencias reales.

**Reputación** — Cuatro ejes: reputación regional, confianza comercial, atención de las aduanas y conexiones con el hampa. Una alta confianza desbloquea contratos premium. Una alta atención provoca inspecciones y denegaciones de acceso a puertos. Diferentes capitanes adoptan diferentes modelos económicos.

**Combate** — Combate personal completo (triángulo de postura: empuje/tajo/parada) con 7 armas de combate cuerpo a cuerpo, 7 armas de largo alcance y estilos de lucha regionales. Combate naval con abordajes y cañones. Corto, brutal y con consecuencias.

**Facciones Piratas** — Crimson Tide (Mediterráneo), Iron Wolves (Atlántico Norte), Deep Reef Brotherhood (Océano Pacífico Sur), Monsoon Syndicate (Indias Orientales). Cada una con su territorio, productos preferidos, capitanes nombrados y actitud hacia usted.

**Infraestructura** — Almacenes (3 niveles), oficinas de intermediarios, 5 licencias comprables. Costos reales de mantenimiento. Cada uno afecta el tiempo, la escala o el acceso al comercio.

**Finanzas** — Seguros (casco, carga, garantía de contrato) y crédito (3 niveles con intereses). Apalancamiento con riesgos.

**Compañeros** — Cinco roles de oficiales (infante de marina, navegante, cirujano, contrabandista, encargado). Compañeros con nombre, personalidad, moral y desencadenantes de partida.

**Carrera** — 27 hitos en 6 familias. 13 etiquetas de perfil de carrera. Cuatro caminos hacia la victoria: Casa comercial legítima, Red de sombras, Alcance oceánico, Imperio comercial.

## Caminos hacia la Victoria

- **Casa comercial legítima** — Legitimidad disciplinada. Alta confianza, contratos premium, reputación impecable, infraestructura amplia.
- **Red de sombras** — Comercio rentable bajo escrutinio. Márgenes de lujo, gestión de la atención, operaciones resilientes.
- **Alcance oceánico** — Poder comercial de larga distancia. Acceso a las Indias Orientales, infraestructura distante, dominio de rutas.
- **Imperio comercial** — Operación integrada en múltiples regiones. Infraestructura en todas partes, diversificación de ingresos, apalancamiento financiero.

## Juego de mesa para imprimir y jugar

Genere una adaptación completa del juego de mesa: cartas, tablero, reglamento, pistas de puntuación:

```bash
pip install portlight[printandplay]
portlight print-and-play
```

Una aventura comercial competitiva para 2-4 jugadores (aproximadamente 90 minutos) con capitanes asimétricos, carreras de contratos y tensión entre reputación y atención. Consulte [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md) para el reglamento completo.

## Referencia de comandos

Ejecute `portlight guide` para obtener una referencia agrupada, o consulte [docs/COMMANDS.md](docs/COMMANDS.md).

| Grupo | Comandos |
|-------|----------|
| Comercio | `market`, `buy`, `sell`, `cargo` |
| Navegación | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| Contratos | `contracts`, `accept`, `obligations`, `abandon` |
| Infraestructura | `warehouse`, `office`, `license` |
| Finanzas | `insure`, `credit` |
| Carrera | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| Mundo | `map`, `port` |
| Interfaz | `tui`, `captain-select` |
| Sistema | `save`, `load`, `guide`, `print-and-play` |

## Calidad

- 1832 pruebas en más de 72 archivos
- 14 invariantes de sistema que se aplican bajo 9 escenarios de estrés compuestos
- Sistema de equilibrio: 7 bots de políticas en 7 paquetes de escenarios
- Formato de guardado v12 con una cadena de migración completa
- Código limpio, Python 3.11/3.12/3.13

## Seguridad

Juego de línea de comandos que solo funciona localmente. No requiere conexión a la red durante el juego. Guarda los datos en las carpetas `saves/` y `artifacts/` como archivos JSON en el sistema de archivos local. No contiene información confidencial, ni telemetría, ni requiere permisos elevados. Consulte el archivo [SECURITY.md](SECURITY.md).

## Desarrollo

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

## Licencia

MIT

---

Desarrollado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
