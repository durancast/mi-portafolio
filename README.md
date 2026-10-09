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

La paleta **"Navy y Teal"** está definida en `@theme` dentro de [`src/styles/global.css`](src/styles/global.css) y se extrajo de `public/logo.png`: neutros `zinc-*` en tono navy azulado, **teal** (`accent-*`) como acento de marca (links, foco, glow, selección, badge de la estrella) y blanco frío `zinc-100` para el texto principal.

- **`public/logo.png`** — logotipo original (lienzo 1376×768, RGBA). Única fuente de marca; no se muestra directamente.
- **`public/logo-emblem.png`** — recorte del emblema (494×493) sin márgenes transparentes. Se usa en la card de identidad y como favicon.
- **`public/og.png`** — imagen para redes sociales (`og:image`, 1200×630): navy + emblema + nombre/rol.

Estos assets son estáticos y se regeneran puntualmente con ImageMagick (sin dependencias Python).

## 📌 Pendiente (TODO)

- [ ] **Proyecto estrella**: `codeUrl` ya es real (CookFlow); falta `demoUrl` (hoy "No disponible" → sin botón).
- [ ] **Proyecto secundario**: rellenar `title`, `summary`, `badges` y URLs reales (hoy vacío → la card está oculta y la estrella ocupa todo el ancho).
- [ ] **CV**: reemplazar `public/cv.pdf` (placeholder generado) por el CV real.
- [ ] **Imágenes de proyecto** *(obligatorio para que se vea algo)*: crear `public/projects/`, añadir capturas (recomendado 1600×1000 `.webp` ≤200 KB) y rellenar `image.src` + `image.alt` en cada proyecto del JSON (hoy `null`: las cards no muestran visual).

## 📁 Estructura

```text
src/
├── components/
│   ├── BentoGrid.astro        ← orquestación del grid responsive (5 cards, md dense / lg)
│   ├── Card.astro             ← base de tarjeta: borde, hover, glow que sigue al puntero
│   ├── IdentityCard.astro     ← editorial (nombre + emblema de marca) + action bar de contacto
│   ├── CopyEmailButton.astro  ← copiar al portapapeles (clipboard + fallback, aria-live)
│   ├── ProjectCard.astro      ← variantes star / secondary (visual solo desde image)
│   ├── StackCard.astro        ← chips mono por categoría
│   ├── LocationCard.astro     ← ciudad + modalidad (sin zona horaria)
│   └── StatusDot.astro        ← punto teal pulsante reutilizable
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
