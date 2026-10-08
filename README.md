# Alejandro Duran — Portafolio

Portafolio personal estilo *bento grid* (carta de presentación B2B) construido con **Astro** (SSG), **Tailwind CSS v4** y **pnpm**.

**Stack**: Astro 7 · Tailwind v4 (CSS-first) · lucide-astro · Geist + JetBrains Mono (Fontsource, autoalojadas).

## 🛠 Comandos

| Commando | Acción |
| :--- | :--- |
| `pnpm install` | Instala dependencias |
| `pnpm dev` | Dev server en `localhost:4321` (`pnpm astro dev --background` en modo background) |
| `pnpm build` | Build de producción en `./dist/` |
| `pnpm preview` | Preview del build |
| `pnpm check` | `astro check` (tipos + validación del JSON de contenido) |

## ✍️ Editar el contenido

**Toda la información vive en [`src/data/portfolio.json`](src/data/portfolio.json).** No hace falta tocar ningún componente:

- `profile` — nombre, rol, estado, email, pitch, ubicación, redes y CV (el email y el CV alimentan la action bar de la card de identidad).
- `projects.star` / `projects.secondary` — títulos, resúmenes, badges, enlaces y `label` (texto del badge mono sobre el título; por defecto "Caso de estudio").
  - Si `title` está vacío, la card **se oculta** y la estrella pasa a ocupar todo el ancho del grid; al rellenarlo, vuelven ambas.
  - `demoUrl` / `codeUrl`: los botones "Live Demo" y "Código" solo se renderizan si la URL empieza por `http(s)://` (usa `""` o "No disponible" para ocultarlos).
  - `badges`: las entradas vacías se omiten (no se pintan píldoras sin texto).
  - `image` — **única fuente del visual**: `{"src": "/projects/mi-app.webp", "alt": "Descripción"}` (archivo dentro de `public/`). Si es `null` o falta, la card no muestra ningún visual. Si `demoUrl` es una URL real, la captura clica hacia la demo.
- `stack` — categorías y chips del bloque de capacidades.

`src/data/portfolio.ts` es solo la capa tipada: define las interfaces y valida el JSON con `satisfies`. Si falta o sobra un campo, **`pnpm check` falla**.

### Imágenes estáticas

La paleta **"Sangre y Hueso"** (estilo *The Witcher 3*) está definida en `@theme` dentro de [`src/styles/global.css`](src/styles/global.css): neutros `zinc-*` reescalados a marrones cálidos, **carmesí** (`accent-*`) como acento primario de marca (links, foco, glow, selección, badge de la estrella), **ámbar** (`gold-*`) como lumbre secundaria (medallón, auras, botón Live Demo) y **hueso** (`bone-*`) para el texto principal en vez de blanco puro. La textura "gastada" viene de `bg-noise` + `bg-vignette` (capa de fondo) y `card-surface` (degradado tipo cuero envejecido en las tarjetas).

`public/avatar.png` (medallón de la card de identidad) y `public/og.png` (foto de redes, 1200×630) se generan con [`scripts/generate-images.py`](scripts/generate-images.py) (requiere `pillow`):

```bash
python3 scripts/generate-images.py
```

## 📌 Pendiente (TODO)

- [ ] **Proyecto estrella**: `codeUrl` ya es real (CookFlow); falta `demoUrl` (hoy "No disponible" → sin botón).
- [ ] **Proyecto secundario**: rellenar `title`, `summary`, `badges` y URLs reales (hoy vacío → la card está oculta y la estrella ocupa todo el ancho).
- [ ] **CV**: reemplazar `public/cv.pdf` (placeholder generado) por el CV real.
- [ ] **Imágenes de proyecto** *(obligatorio para que se vea algo)*: crear `public/projects/`, añadir capturas (recomendado 1600×1000 `.webp` ≤200 KB) y rellenar `image.src` + `image.alt` en cada proyecto del JSON (hoy `null`: las cards no muestran visual).
- [ ] **Foto**: reemplazar `public/avatar.png` (placeholder "AD") por una foto real o un render 3D tipo emoji (PNG cuadrado, el CSS lo recorta en círculo). Al hacerlo, quitar `alt=""` y `aria-hidden="true"` de la `<img>` de `IdentityCard.astro` y poner un alt descriptivo (p. ej. `alt="Foto de Alejandro Duran"`).

## 📁 Estructura

```text
src/
├── components/
│   ├── BentoGrid.astro        ← orquestación del grid responsive (5 cards, md dense / lg)
│   ├── Card.astro             ← base de tarjeta: borde, hover, glow que sigue al puntero
│   ├── IdentityCard.astro     ← editorial (nombre + medallón) + action bar de contacto (email/CV/redes)
│   ├── CopyEmailButton.astro  ← copiar al portapapeles (clipboard + fallback, aria-live)
│   ├── ProjectCard.astro      ← variantes star / secondary (visual solo desde image)
│   ├── StackCard.astro        ← chips mono por categoría
│   ├── LocationCard.astro     ← ciudad + modalidad (sin zona horaria)
│   └── StatusDot.astro        ← punto verde pulsante reutilizable
├── data/
│   ├── portfolio.json         ← FUENTE DE VERDAD del contenido
│   └── portfolio.ts           ← interfaces + validación `satisfies`
├── layouts/BaseLayout.astro   ← SEO (canonical/OG/JSON-LD), fuentes, fondo
├── pages/index.astro
└── styles/global.css          ← @theme, utilidades (btn/chip/card-hover), keyframes
```

## 👀 Referencias

- [Documentación de Astro](https://docs.astro.build)
- [Tailwind CSS v4](https://tailwindcss.com/docs)
