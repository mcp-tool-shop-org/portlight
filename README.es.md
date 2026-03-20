<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/portlight/readme.png" width="400" alt="Portlight">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/portlight/actions"><img src="https://github.com/mcp-tool-shop-org/portlight/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="https://github.com/mcp-tool-shop-org/portlight/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue.svg" alt="MIT License"></a>
  <a href="https://mcp-tool-shop-org.github.io/portlight/"><img src="https://img.shields.io/badge/docs-landing_page-blue" alt="Landing Page"></a>
</p>

Una estrategia marítima centrada en el comercio, donde construyes una carrera como comerciante a través de la optimización de rutas, contratos, infraestructura, finanzas y reputación comercial en una economía regional dinámica.

## ¿Por qué Portlight?

La mayoría de los juegos de comercio simplifican el comercio a un número que simplemente aumenta. Portlight trata el comercio como una disciplina comercial:

- **Los precios reaccionan a tus transacciones.** Si vendes grandes cantidades de grano en un puerto, el precio se desploma. Cada venta altera el mercado local.
- **Los puertos tienen identidades económicas reales.** Porto Novo produce grano a bajo costo. Al-Manar consume seda con avidez. Estas características no son aleatorias, sino estructurales.
- **Los viajes implican riesgos.** Tormentas, piratas, inspecciones. Tus provisiones, el casco y la tripulación son importantes.
- **Los contratos requieren pruebas.** Debes entregar los productos correctos en el puerto correcto, con un registro de procedencia verificable. No se permiten falsificaciones.
- **La infraestructura cambia la forma en que operas.** Los almacenes te permiten almacenar mercancías. Los intermediarios mejoran la calidad de los contratos. Las licencias desbloquean acceso premium.
- **El crédito es una herramienta poderosa, pero con riesgos.** El crédito te permite actuar más rápido. Si incumples, perderás acceso a él.
- **El juego evalúa lo que has construido.** Tu historial comercial, infraestructura, reputación y rutas forman un perfil de carrera. El juego te indica qué tipo de empresa comercial eres realmente.

## El Ciclo Principal

1. Analiza el mercado: encuentra qué productos son baratos aquí y caros en otro lugar.
2. Compra mercancías: carga tu bodega.
3. Navega: atraviesa rutas bajo la presión del clima, la tripulación y las provisiones.
4. Vende: obtén ganancias, altera el mercado local.
5. Reinvierta: mejora tu barco, alquila un almacén, abre una oficina de intermediarios.
6. Construye acceso: gana confianza, reduce la atención negativa, desbloquea contratos y licencias.
7. Persigue un destino comercial: cuatro caminos distintos hacia la victoria, basados en lo que realmente has construido.

## Guía de inicio rápido

```bash
# Install
pip install -e ".[dev]"

# Start a new game
portlight new "Captain Hawk" --type merchant

# Look at what's for sale
portlight market

# Buy cheap goods
portlight buy grain 10

# Check available routes
portlight routes

# Sail to where grain sells high
portlight sail al_manar

# Advance through the voyage
portlight advance

# Sell at destination
portlight sell grain 10

# See your trade history
portlight ledger

# Check your career progress
portlight milestones
```

Consulta [docs/START_HERE.md](docs/START_HERE.md) para una primera sesión guiada y [docs/FIRST_VOYAGE.md](docs/FIRST_VOYAGE.md) para una descripción detallada de las primeras etapas del juego.

## Tipos de Capitanes

| Capitán | Identidad | Ventaja | Compromiso |
|---------|----------|------|-----------|
| **Merchant** | Comerciante con licencia, base en el Mediterráneo | Mejores precios, tasas de inspección más bajas, la confianza crece más rápido. | Sin acceso al mercado negro. |
| **Smuggler** | Operador discreto, base en África Occidental. | Acceso al mercado negro, márgenes de lujo, comercio de contrabando. | Mayor atención negativa, más inspecciones. |
| **Navigator** | Explorador de aguas profundas, base en el Mediterráneo. | Barcos más rápidos, mayor alcance, acceso temprano a las Indias Orientales. | Posición comercial inicial más débil. |

## Sistemas

**Economía:** Precios determinados por la escasez en 10 puertos, 8 productos, 17 rutas. Las penalizaciones por sobreproducción castigan la venta masiva. Los shocks del mercado crean oportunidades regionales.

**Viajes:** Viajes de varios días con eventos climáticos, encuentros con piratas e inspecciones. Las provisiones, el casco y la tripulación son recursos reales.

**Capitanes:** Tres arquetipos distintos con diferencias de precios del 8 al 20%, posiciones de inicio únicas y diferentes perfiles de acceso.

**Contratos:** Seis familias de contratos bloqueadas por la confianza y la reputación. Entrega con validación de procedencia. Plazos reales con consecuencias reales.

**Reputación:** Posición regional, reputación específica de cada puerto, atención de las aduanas y confianza comercial. Un modelo de acceso de múltiples ejes que abre y cierra puertas.

**Infraestructura:** Almacenes (3 niveles), oficinas de intermediarios (2 niveles en 3 regiones) y 5 licencias comprables. Cada una cambia el tiempo, la escala o el acceso al comercio.

**Seguro:** Pólizas de seguro de casco, carga y garantía de contrato. Cargos por atención negativa. Resolución de reclamaciones con condiciones de denegación.

**Crédito:** Tres niveles de crédito con acumulación de intereses, plazos de pago y consecuencias por incumplimiento. Una herramienta poderosa con riesgos reales.

**Carrera** — 27 hitos en 6 categorías. Interpretación del perfil de carrera (etiquetas primarias/secundarias/emergentes). Cuatro caminos hacia la victoria: Casa Comercial Legítima, Red de la Sombra, Alcance Oceánico e Imperio Comercial.

## Caminos hacia la Victoria

- **Casa Comercial Legítima** — Legitimidad disciplinada. Alta confianza, contratos premium, reputación intachable, amplia infraestructura.
- **Red de la Sombra** — Comercio discreto y rentable. Márgenes de lujo bajo escrutinio, gestión de riesgos, operaciones resilientes.
- **Alcance Oceánico** — Poder comercial de largo alcance. Acceso a las Indias Orientales, infraestructura distante, dominio de rutas premium.
- **Imperio Comercial** — Operación integrada en múltiples regiones. Infraestructura en cada región, diversificación de ingresos, apalancamiento financiero.

Consulte [docs/CAREER_PATHS.md](docs/CAREER_PATHS.md) para obtener descripciones detalladas dirigidas al jugador.

## Referencia de Comandos

Ejecute `portlight guide` dentro del juego para obtener una referencia de comandos agrupada, o consulte [docs/COMMANDS.md](docs/COMMANDS.md).

| Grupo | Comandos |
|-------|----------|
| Comercio | `market`, `buy`, `sell`, `cargo` |
| Navegación | `routes`, `sail`, `advance`, `port`, `provision`, `repair`, `hire` |
| Contratos | `contracts`, `accept`, `obligations`, `abandon` |
| Infraestructura | `warehouse`, `office`, `license` |
| Finanzas | `insure`, `credit` |
| Carrera | `captain`, `reputation`, `milestones`, `status`, `ledger`, `shipyard` |
| Sistema | `save`, `load`, `guide` |

## Estado Alpha

Portlight está en estado alpha. Los sistemas principales están completos y han sido sometidos a pruebas de estrés, pero el equilibrio se está ajustando activamente.

**Lo que está funcionando correctamente:**
- Todos los sistemas son funcionales de extremo a extremo.
- 609 pruebas en 24 archivos.
- 14 invariantes entre sistemas aplicadas bajo 9 escenarios de estrés compuestos.
- Sistema de equilibrio con 7 bots de política en 7 paquetes de escenarios.

**Lo que se está ajustando:**
- Escalado de contrabandistas (actualmente con un rendimiento inferior en la progresión de la nave).
- Concentración de rutas en el Mediterráneo (Porto Novo / Silva Bay dominan el tráfico).
- Tasas de finalización de contratos (fallas en la lógica de entrega en ejecuciones automatizadas).
- Adopción de seguros (actualmente cercana a cero en pruebas simuladas).

Consulte [docs/ALPHA_STATUS.md](docs/ALPHA_STATUS.md) para obtener detalles y [docs/KNOWN_ISSUES.md](docs/KNOWN_ISSUES.md) para obtener información específica.

## Seguridad y Datos

Portlight es un juego de **línea de comandos que solo funciona localmente**. No realiza ninguna conexión de red durante el juego. Datos accedidos: archivos de guardado locales (`saves/`) y archivos de informe (`artifacts/`), todos en formato JSON en el sistema de archivos local. No hay secretos, credenciales, telemetría ni servicios remotos. No se requieren permisos elevados. Consulte [SECURITY.md](SECURITY.md) para obtener la política completa.

## Desarrollo

```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Run balance simulation
python tools/run_balance.py

# Run stress tests
python tools/run_stress.py

# Lint
ruff check src/ tests/
```

## Licencia

MIT

---

Desarrollado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
