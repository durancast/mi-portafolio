/**
 * Capa tipada sobre el contenido.
 *
 * La fuente de verdad es `portfolio.json` (contenido editable sin tocar código).
 * Este archivo define las interfaces y las valida con `satisfies`: si falta o
 * sobra un campo en el JSON, `pnpm check` falla.
 *
 * NOTA: JSON no admite comentarios → los TODO pendientes están en el README
 * sección "Pendiente".
 */
import raw from "./portfolio.json";

export interface Profile {
  name: string;
  role: string;
  status: string;
  email: string;
  pitch: string;
  location: {
    city: string;
    modality: string;
  };
  links: {
    github: string;
    linkedin: string;
  };
  cvUrl: string;
}

export interface Project {
  /** Identificador único usado para los `id` de encabezados (accesibilidad). */
  id: string;
  /** Texto del badge mono sobre el título (p. ej. "Caso de estudio"). */
  label: string;
  title: string;
  summary: string;
  badges: string[];
  demoUrl: string;
  codeUrl: string;
  /**
   * Captura real del proyecto (archivo en /public). ÚNICA fuente del visual:
   * `null` o ausente → la card no muestra ningún visual.
   * Si `src` existe, `alt` es obligatorio (la imagen es contenido, no decoración).
   */
  image?: {
    /** Ruta pública, p. ej. "/projects/reservas.webp". */
    src: string;
    /** Descripción para lectores de pantalla. */
    alt: string;
  } | null;
}

export interface StackGroup {
  category: string;
  items: string[];
}

export interface PortfolioData {
  profile: Profile;
  projects: {
    star: Project;
    secondary: Project;
  };
  stack: StackGroup[];
}

const data = raw satisfies PortfolioData;

export const profile: Profile = data.profile;
export const starProject: Project = data.projects.star;
export const secondaryProject: Project = data.projects.secondary;
export const stack: StackGroup[] = data.stack;
