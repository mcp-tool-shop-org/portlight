<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://pypi.org/project/portlight/"><img src="https://img.shields.io/pypi/v/portlight" alt="PyPI"></a>
  <a href="https://www.npmjs.com/package/@mcptoolshop/portlight"><img src="https://img.shields.io/npm/v/@mcptoolshop/portlight" alt="npm"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/landing-page-blue" alt="Landing Page"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/handbook/"><img src="https://img.shields.io/badge/docs-handbook-blue" alt="Handbook"></a>
</p>

Portlight es un juego de estrategia marítima centrado en el comercio para jugar en la terminal. Controlas a un capitán, una bodega y una reputación en veinte puertos. Los precios cambian cuando vendes. Los contratos requieren pruebas de origen. Los corredores y los almacenes modifican el valor de un viaje. Cuatro caminos hacia la victoria evalúan la carrera que realmente construiste, no la que elegiste el primer día.

Juega en la **TUI** (`portlight tui`) o en la **CLI**. El mismo archivo de guardado. El mismo mundo.

## Instalación

```bash
pip install "portlight[tui]"
```

Python 3.11 o superior. El paquete adicional `tui` incluye Textual. Solo para CLI: `pip install portlight`.

¿No tienes Python? El lanzador de npm descarga el binario de la versión de GitHub:

```bash
npx @mcptoolshop/portlight
```

Kit de juego imprimible en PDF: `pip install "portlight[printandplay]"`.

## Jugar

```bash
portlight tui
```

Si no hay un archivo de guardado, la TUI muestra las ranuras y la opción **Nuevo**. Elige un tipo de capitán. Luego:

| Tecla | Función |
|-----|----------------|
| **D** | Panel de control (aquí se muestran la carrera y los hitos) |
| **M / B / S** | Mercado: comprar, vender |
| **G / A** | Selector de viajes: avanzar un día |
| **H** | Puerto: aprovisionamiento, reparación, contratación; también trabajo, despido, caza. En el mar, H caza. |
| **K** | Contratos. Pulsa **K de nuevo** para aceptar o abandonar. |
| **W** | Infraestructura. Pulsa **W de nuevo** para alquilar, depositar, retirar, abrir un corredor, comprar una licencia o obtener crédito. |
| **P** | Puerto. Pulsa **P de nuevo** para acceder al astillero (comprar casco, mejoras, dique seco). |
| **F** | Flota. Pulsa **F de nuevo** para abordar, atracar, transferir o vender un casco capturado. |
| **V** | Mapa del mundo |
| **?** | Ayuda |

La CLI es el mismo juego con comandos escritos:

```bash
portlight new "Captain Hawk" --type merchant
portlight market
portlight buy grain 10
portlight sail al_manar
portlight advance
portlight sell grain 10
portlight tui
```

`portlight --json status` guarda un diccionario estable (capitán, puerto, carga, mercado, rutas, tripulación) sin ANSI. `portlight saves` muestra las ranuras.

Sesión de inicio guiada: [docs/START_HERE.md](docs/START_HERE.md). Manual: [https://mcp-tool-shop-org.github.io/portlight/handbook/](https://mcp-tool-shop-org.github.io/portlight/handbook/).

## ¿Por qué Portlight?

La mayoría de los juegos de comercio simplifican el comercio en un número que aumenta. Portlight trata el comercio como una disciplina comercial:

- **Los precios reaccionan a tus operaciones comerciales.** Vende grano y el precio local se desplomará.
- **Los puertos tienen identidades económicas.** Porto Novo cultiva grano. Silk Haven exporta seda. Esa es la estructura, no el ruido.
- **Los viajes conllevan riesgos.** Tormentas, piratas, inspecciones, estaciones. Las provisiones, el casco y la tripulación son costes reales.
- **Los contratos requieren pruebas.** Productos correctos, puerto correcto, origen rastreado, plazos reales.
- **La infraestructura cambia los tiempos.** Los almacenes preparan la carga. Los corredores mejoran la oferta. Las licencias abren el acceso premium. Las cinco regiones activas tienen oficinas de corredores y una carta regional.
- **La reputación se basa en cuatro ejes.** Confianza comercial, control de aduanas, posición regional, inframundo. Estos abren y cierran puertas de forma independiente.
- **El juego lee lo que has construido.** Los hitos y los cuatro caminos hacia la victoria evalúan las pruebas, no una opción del menú.

## El mundo

Cinco regiones. Veinte puertos. Cuarenta y tres rutas.

| Región | Puertos | Personaje |
|--------|-------|-----------|
| **Mediterranean** | Porto Novo, Al-Manar, Silva Bay, Corsair's Rest | Grano, madera, especias. Aguas de inicio seguras. |
| **North Atlantic** | Ironhaven, Stormwall, Thornport | Hierro, armas, comercio de guarnición. Inspecciones estrictas. |
| **West Africa** | Sun Harbor, Palm Cove, Iron Point, Pearl Shallows | Algodón, ron, perlas. Provisiones baratas. |
| **East Indies** | Jade Port, Monsoon Reach, Silk Haven, Crosswind Isle, Dragon's Gate, Spice Narrows | Seda, especias, porcelana, té. Márgenes más altos. Riesgo de monzón. |
| **South Seas** | Ember Isle, Typhoon Anchorage, Coral Throne | Perlas, medicinas. Aguas de juego final remotas. |

Dieciocho productos (incluidos cueros y contrabando). Ciento treinta y cuatro personajes no jugables con nombre. Cuatro facciones piratas con ocho capitanes con nombre activos. Clima estacional. Festivales, supersticiones, moral de la tripulación.

## Nueve capitanes

| Capitán | Hogar | Ventaja | Compromiso |
|---------|------|------|-----------|
| **Merchant** | Porto Novo | Mejores precios, la confianza crece rápidamente | Las penalizaciones de calor se duplican |
| **Smuggler** | Palm Cove | Mercado negro, contrabando | Mayor calor, más inspecciones |
| **Navigator** | Silva Bay | Barcos más rápidos, mayor alcance | Posición inicial más débil |
| **Privateer** | Stormwall | Combate naval, abordaje | Mala reputación como comerciante |
| **Corsair** | Corsair's Rest | Combate + comercio | No es un experto en nada |
| **Scholar** | Monsoon Reach | Información, mejores contratos | Bajo capital, frágil |
| **Merchant Prince** | Al-Manar | Alto capital inicial | Mayores tarifas, objetivo de los piratas |
| **Dockhand** | Crosswind Isle | Tripulación barata | Menor capital inicial |
| **Bounty Hunter** | Crosswind Isle | Combate, posición de la facción | Malos precios, desconfianza |

`portlight new "Name"` sin `--type` abre la lista. Bounty Hunter no es una etiqueta de sabor: `portlight bounty accept <id>` y luego `portlight bounty hunt <id>` obliga a que el capitán tenga un nombre. Los ID fantasma han desaparecido; la lista solo muestra los `PIRATE_CAPTAINS` activos.

## Sistemas

**Economía:** Precios de escasez, penalizaciones por exceso de oferta, fluctuaciones del mercado, identidad regional de importación/exportación.

**Viajes:** Viajes de varios días. Clima, piratas, inspecciones. Los duelos con piratas con nombre prefieren un objetivo activo cuando este se encuentra en las aguas.

**Contratos:** Siete familias, veinticuatro plantillas. Puertas de confianza y posición. Entrega con pruebas de origen.

**Reputación:** Posición regional, confianza comercial, control de aduanas, conexiones con el inframundo.

**Combate** — Triángulo de postura personal (estocada / tajo / parada), combate cuerpo a cuerpo y a distancia, estilos de lucha (TUI **Y** activa la habilidad especial del estilo). Naval: fuego de costado, combate cercano, evasión, ataque lateral, huida. Captura de premios con el casco real de una flota.

**Infraestructura** — Tres niveles de almacenes. Oficinas de corredores: local + establecidas en las cinco regiones. Siete licencias (cinco licencias regionales, incluidas el Atlántico Norte y los Mares del Sur, más dos globales). Costos de mantenimiento reales.

**Finanzas** — Seguro de casco, carga y garantía de contrato. Tres niveles de crédito con intereses y penalizaciones por impago.

**Flota** — Múltiples cascos, atraque/abordaje en el mismo puerto, transferencia de carga, dieciocho mejoras.

**Carrera** — Veintisiete hitos, siete etiquetas de perfil, cuatro caminos hacia la victoria. El panel muestra el libro mayor; al avanzar el día, se celebran los logros recién completados.

## Caminos hacia la victoria

- **Casa de Comercio Legal** — Alta confianza, contratos premium, reputación intachable, amplia infraestructura.
- **Red de la Sombra** — Márgenes de lujo bajo presión, sobrevivió a las confiscaciones, sigue a la cabeza.
- **Alcance Oceánico** — Posición en las Indias Orientales, infraestructura distante, dominio de las rutas de larga distancia.
- **Imperio Comercial** — Almacenes, corredores, licencias y apalancamiento financiero en múltiples regiones.

## Para imprimir y jugar

```bash
pip install "portlight[printandplay]"
portlight print-and-play
```

PDF del tamaño de un kit (formato vertical después del tablero horizontal, escala plateada 0–100). Manual de reglas: [docs/PRINT_AND_PLAY_RULES.md](docs/PRINT_AND_PLAY_RULES.md).

## Grupos de comandos

Ejecutar `portlight guide` en el juego, o [docs/COMMANDS.md](docs/COMMANDS.md).

| Grupo | Comandos |
|-------|----------|
| Interfaz | `tui`, `saves`, `--json` |
| Comercio | `market`, `buy`, `sell`, `cargo` |
| Navegación | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire`, `fire`, `crew`, `hunt`, `work` |
| Combate | `duel`, `fight`, `encounter`, `naval`, `capture`, `spare`, `take-all`, `bounty` (`list` / `accept` / `hunt` / `claim`) |
| Equipo | `inventory`, `equip`, `merchant`, `sell-gear`, `armory`, `train`, `equip-style`, `maintain`, `smith`, `field-repair`, `injuries`, `learn-skill` |
| Flota | `shipyard`, `drydock`, `fleet`, `dock`, `board`, `transfer`, `rename`, `upgrade` |
| Contratos | `contracts`, `accept`, `obligations`, `abandon` |
| Compañeros | `recruit`, `dismiss-companion`, `party` |
| Infraestructura | `warehouse`, `office`, `license` |
| Finanzas | `insure`, `credit` |
| Carrera | `captain`, `reputation`, `milestones`, `status`, `ledger` |
| Mundo | `map` |
| Sistema | `save`, `load`, `guide`, `print-and-play` |

## Calidad

- 1.853 pruebas
- 14 invariantes entre sistemas bajo 9 escenarios de estrés compuestos
- Herramienta de equilibrio: 7 bots de política, 7 paquetes de escenarios
- Formato de guardado v12 con una cadena de migración completa
- Ruff-clean. Python 3.11 / 3.12 / 3.13

## Seguridad

Juego solo local. Sin red durante el juego. Guarda en `saves/` e informa a `artifacts/` en formato JSON. Sin secretos, sin telemetría, sin permisos elevados. Consulte [SECURITY.md](SECURITY.md).

## Desarrollo

```bash
pip install -e ".[dev]"
pytest
ruff check src/ tests/
```

`verify.sh` ejecuta pruebas, Ruff, la creación de un paquete y una importación de prueba del artefacto creado.

## Licencia

MIT

---

Creado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
