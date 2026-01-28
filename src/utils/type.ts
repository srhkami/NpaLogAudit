export type Response<T> = {
  message: string,
  data: T,
}

export type AppConfig = {
  'theme': 'dark'| 'light',
  'readme': string,
}


export type VersionCheckData = {
  app_version: string,
  whats_new: string,
  download_link: string,
}

export type TVersionObject = {
  version: string,
  date: string,
  logs: Array<{ color: 'new' | 'info' | 'fix', text: string }>,
}
