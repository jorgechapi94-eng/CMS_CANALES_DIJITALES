export interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  roles: string[]
  created_at: string | null
  updated_at: string | null
}

export interface LoginCredentials {
  email: string
  password: string
}

export interface AuthResponse {
  access_token: string
  refresh_token: string
  user: User
}

export interface Category {
  id: number
  name: string
  slug: string
}

export interface NewsAuthor {
  id: number
  username: string
}

export interface NewsItem {
  id: number
  title: string
  slug: string
  excerpt: string | null
  content_html?: string
  cover_image_url: string | null
  status: 'draft' | 'published' | 'archived'
  author: NewsAuthor | null
  categories: Category[]
  published_at: string | null
  created_at: string | null
  updated_at: string | null
}

export interface Newspaper {
  id: number
  title: string
  pdf_url: string
  cover_thumbnail_url: string | null
  uploaded_by: { id: number; username: string } | null
  publication_date: string | null
  file_size_bytes: number | null
  created_at: string | null
}

export interface ProgramTeacher {
  id?: number
  full_name: string
  title_degree: string
  email: string
  photo_url: string | null
}

export interface ProgramStudent {
  id?: number
  full_name: string
  enrollment_year: string
}

export interface ProgramProject {
  id?: number
  title: string
  description: string
  link_url: string | null
}

export interface Program {
  id: number
  title: string
  description: string | null
  modality: 'presencial' | 'virtual' | 'hibrido'
  level: 'grado' | 'maestria' | 'doctorado' | 'tecnico'
  is_active: boolean
  teachers_count: number
  students_count: number
  projects_count: number
  teachers?: ProgramTeacher[]
  students?: ProgramStudent[]
  projects?: ProgramProject[]
  created_at: string | null
  updated_at: string | null
}

export interface YouTubeVideo {
  id: string
  title: string
  description: string
  publishedAt: string
  thumbnails: Record<string, { url: string; width: number; height: number }>
  youtubeUrl: string
}

export interface RadioStatus {
  title: string
  artist: string
  listeners: number
  bitrate: number
  genre: string
  fallback?: boolean
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  per_page: number
  pages: number
}

export interface UploadResponse {
  url: string
  originalName: string
  sizeBytes: number
}
